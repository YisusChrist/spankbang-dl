import time
import tkinter as tk
from datetime import date
from pathlib import Path
from threading import Thread
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING, Optional
from urllib.parse import ParseResult, urlparse

import requests
from core_helpers.logs import logger

if TYPE_CHECKING:
    from . import VideoDownloaderUI

from ..consts import AUTHOR, DEFAULT_CHUNK_SIZE, KB, MB
from ..consts import __version__ as VERSION
from ..scraper import extract_video_info, fetch_web_content
from ..translations import get_translations
from ..utils import format_file_size


def _create_pop_up_window(gui: "VideoDownloaderUI", title: str, message: str) -> None:
    """
    Create a pop-up window with the given title and message.

    Args:
        gui (VideoDownloaderUI): The GUI instance.
        title (str): The title of the pop-up window.
        message (str): The message to display in the pop-up window.
    """
    # Create a top-level overlay window rather than using system messagebox
    help_win = tk.Toplevel(gui.win)
    help_win.title(title)
    help_win.geometry("450x250")
    help_win.minsize(650, 200)

    # Configure the inner frame wrapper to scale cleanly on resize mechanics
    frame = ttk.Frame(help_win, padding="15")
    frame.pack(expand=True, fill="both")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # Message widget scales text wrapping seamlessly when width parameters shift
    msg = tk.Message(frame, text=message, justify="left", aspect=200, width=600)
    msg.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

    close_btn = ttk.Button(frame, text="OK", command=help_win.destroy)
    close_btn.grid(row=1, column=0, pady=5)


def start_download_thread(gui: VideoDownloaderUI) -> None:
    """
    Callback function to handle the download button click event.

    Retrieves the video URL from the input field, fetches the web content,
    extracts video information, and downloads the video while displaying
    progress in the GUI.
    """
    logger.debug("Download button clicked")

    if gui.downloading:
        gui.log_message(gui.translations["already_downloading_message"])
        logger.warning("Download already in progress!")
        return

    url: str = gui.a_url.get()
    if not url:
        messagebox.showwarning(
            gui.translations["warning_title"],
            gui.translations["empty_url_message"],
        )
        logger.warning("No URL provided for download!")
        return

    gui.log_message(f"Starting download from: {url}")

    r: requests.Response | None = handle_web_content_fetch(gui, url)
    if r is None:
        return

    video: str | None = extract_and_display_video_info(gui, url, r.text)
    if not video:
        return

    resp: requests.Response | None = handle_web_content_fetch(gui, video, stream=True)
    if resp is None:
        return

    try:
        thread = Thread(
            target=download_video_and_display_progress,
            args=(gui, resp),
            daemon=True,
        )
        thread.start()
    except Exception as e:
        gui.log_message(gui.translations["download_failed_message"].format(str(e)))
        logger.error("Error downloading video from %s", url, exc_info=True)
        gui.downloading = False
        raise


def handle_web_content_fetch(
    gui: VideoDownloaderUI, url: str, stream: bool = False
) -> Optional[requests.Response]:
    """
    Fetch web content from the given URL and handle exceptions.

    Args:
        url (str): The URL to fetch web content from.
        stream (bool): Whether to stream the response content. Defaults to False.

    Returns:
        requests.Response | None: The response object if successful, None
        otherwise.
    """
    logger.debug("Fetching and handling web content for URL: %s", url)

    try:
        response: requests.Response = fetch_web_content(url, stream=stream)
        logger.info(
            "Web content fetched successfully for %s: %s", url, response.status_code
        )
        return response
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            error_message = e.response.status_code
        else:
            error_message = str(e)
        gui.log_message(gui.translations["failure_message"].format(error_message))
        logger.error(
            "Failed to fetch content from %s: %s", url, error_message, exc_info=True
        )
        return None


def extract_and_display_video_info(
    gui: VideoDownloaderUI, url: str, html: str
) -> Optional[str]:
    """
    Extract and display video information.

    Args:
        url (str): The URL of the video page.
        html (str): The HTML content of the page.

    Returns:
        str: The video source URL if found, otherwise an empty string.
    """
    logger.debug("Extracting and displaying video information for URL: %s", url)

    try:
        title, video = extract_video_info(html)
    except ValueError as e:
        gui.log_message(gui.translations["video_not_found"].format(str(e)))
        logger.error("Video information not found in the web content", exc_info=True)
        return ""

    # Display the translated messages and labels
    gui.log_message(gui.translations["download_video_message"].format(url))
    gui.log_message(gui.translations["video_title"].format(title))
    gui.log_message(gui.translations["video_url"].format(video))
    logger.debug("Extracted video info: Title: %r, URL: %s", title, video)

    return video


def download_video_and_display_progress(
    gui: VideoDownloaderUI, resp: requests.Response
) -> None:
    """gui
    Download the video and display the download progress.

    Args:
        resp (requests.Response): The response object containing the video data.
    """
    logger.debug("Starting video download for URL: %s", resp.url)

    content_size = int(resp.headers["Content-Length"])
    parsed_url: ParseResult = urlparse(resp.url)
    if not parsed_url.path:
        gui.win.after(
            0,
            lambda: gui.log_message(
                gui.translations["invalid_url_message"].format(resp.url)
            ),
        )
        logger.error("Invalid URL: %s", resp.url)
        return

    content_size_text: str = format_file_size(content_size)
    gui.win.after(
        0,
        lambda: gui.log_message(
            gui.translations["total_size_message"].format(content_size_text)
        ),
    )
    logger.debug("Total size of the video: %s", content_size_text)

    # Extract the media extension from the URL path
    file_extension: str = parsed_url.path.split(".")[-1]
    file_name: str = parsed_url.path.split("/")[-1] or f"video.{file_extension}"
    # Create the file path with the correct extension
    file_path: Path = Path(file_name).with_suffix(f".{file_extension}")

    # Set up progress bar
    gui.progress_bar["maximum"] = content_size
    gui.progress_bar["value"] = 0
    gui.progress_percent.set("0%")
    # Reset flags
    gui.pause_download = False
    gui.cancel_download = False
    gui.downloading = True
    # Ensure initial draw
    gui.win.update_idletasks()

    downloaded = 0
    start_time: float = time.time()

    # Dynamically adjust chunk size based on content size for better performance
    chunk_size = DEFAULT_CHUNK_SIZE
    if content_size > 50 * MB:
        chunk_size = 256 * KB
    elif content_size > 5 * MB:
        chunk_size = 64 * KB

    with open(file_path, mode="wb") as f:

        def update_progress() -> None:
            gui.progress_bar["value"] = downloaded
            gui.progress_percent.set(f"{percent:.1f}%")

        for chunk in resp.iter_content(chunk_size):
            if gui.cancel_download:
                # Reset progress bar, label and flags
                gui.progress_bar["value"] = 0
                gui.progress_percent.set("0%")
                gui.pause_download = False  # reset pause flag
                gui.cancel_download = False  # reset cancel flag
                gui.downloading = False
                logger.info("Download cancelled by user.")
                return
            elif gui.pause_download:
                logger.info("Download paused by user.")
                while gui.pause_download:
                    time.sleep(0.1)  # Wait until unpaused
                logger.info("Download resumed by user.")

            if not chunk:
                continue

            f.write(chunk)
            downloaded += len(chunk)

            percent: float = (downloaded / content_size) * 100
            elapsed: float = time.time() - start_time
            rate: float = downloaded / elapsed if elapsed > 0 else 0
            remaining: float = (content_size - downloaded) / rate if rate > 0 else 0
            eta: str = time.strftime("%M:%S", time.gmtime(remaining))

            gui.win.after(0, update_progress)

    gui.downloading = False
    gui.win.after(
        0, lambda: gui.log_message(gui.translations["download_complete_message"])
    )
    gui.win.after(
        0, lambda: gui.log_message(gui.translations["video_saved"].format(file_path))
    )
    logger.info("Download complete for %r", file_path)


def quit_app(gui: VideoDownloaderUI) -> None:
    """
    Callback function to handle the quit button click event.

    Closes the main application window and exits the program.
    """
    logger.debug("Quit button clicked")

    gui.win.quit()
    gui.win.destroy()
    logger.debug("Destroyed the main window")


def show_about(gui: VideoDownloaderUI) -> None:
    """
    Callback function to handle the about button click event.

    Displays an informational message box with author, version, and current
    date.
    """
    logger.debug("About button clicked")

    today: str = date.today().strftime("%d/%m/%Y")
    about_message: str = gui.translations["about_message"].format(
        AUTHOR, VERSION, today
    )
    messagebox.showinfo(gui.translations["about_button"], about_message)


def show_help(gui: VideoDownloaderUI) -> None:
    """
    Callback function to handle the help button click event.

    Displays an informational message box with usage instructions or help
    content.
    """
    logger.debug("Help button clicked")
    help_message: str = gui.translations["help_message"]
    messagebox.showinfo(gui.translations["help_button"], help_message)


def cancel_download(gui: VideoDownloaderUI) -> None:
    """Sets the cancel flag to True."""
    logger.debug("Cancel download button clicked")
    if not gui.downloading:
        gui.log_message(gui.translations["no_download_message"])
        logger.warning("No download in progress to cancel.")
        return

    gui.cancel_download = True
    gui.log_message(gui.translations["cancelled_message"])


def pause_resume_download(gui: VideoDownloaderUI) -> None:
    """Sets the pause flag to True."""
    logger.debug("Pause download button clicked")
    if not gui.downloading:
        gui.log_message(gui.translations["no_download_message"])
        logger.warning("No download in progress to pause/resume.")
        return

    if gui.pause_download:
        gui.pause_download = False
        gui.log_message(gui.translations["resumed_message"])
        logger.info("Download resumed by user.")
    else:
        gui.pause_download = True
        gui.log_message(gui.translations["paused_message"])
        logger.info("Download paused by user.")


def change_language(gui: VideoDownloaderUI, lang_code: str) -> None:
    if gui.current_language == lang_code:
        logger.debug("Language change requested but already set to %s", lang_code)
        gui.log_message(gui.translations["language_already_set"].format(lang_code))
        return

    gui.translations = get_translations(lang_code)
    gui.current_language = lang_code

    # Update the OS Window title
    gui.win.title(gui.translations["window_title"])

    # Update buttons
    gui.help_btn.config(text=gui.translations["help_button"])
    gui.about_btn.config(text=gui.translations["about_button"])

    # Update other componentes
    gui.url_frame.config(text=gui.translations["enter_url_label"])
    gui.log_frame.config(text=gui.translations["log_frame_label"])
    gui.lang_label.config(text=gui.translations["language"])

    gui.log_message(gui.translations["language_changed_message"].format(lang_code))
