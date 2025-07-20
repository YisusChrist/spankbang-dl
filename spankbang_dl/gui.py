# 写UI
import time
import tkinter as tk
from datetime import date
from pathlib import Path
from threading import Thread
from tkinter import messagebox, scrolledtext, ttk
from typing import Optional
from urllib.parse import ParseResult, urlparse

import requests

from .consts import AUTHOR, MB
from .consts import __version__ as VERSION
from .logs import logger
from .scraper import extract_video_info, fetch_web_content
from .translations import get_translations

# 引入库


class VideoDownloaderUI:
    """
    A class to create the GUI interface.

    Args:
        selected_language (str, optional): The selected language. Defaults to "en".

    Attributes:
        win (tk.Tk): The main window.
        translations (dict): The translations for the selected language.

    Methods:
        _download: Download the video.
        _quit: Quit the program.
        _about: Show the about message.
        _help: Show the help message.
        run: Run the program.
    """

    def __init__(self, selected_language: str = "en") -> None:
        """
        Initialize the class.

        Args:
            selected_language (str, optional): The selected language. Defaults
            to "en".
        """
        logger.debug("Creating GUI with selected language: %s", selected_language)

        # Load translations for the selected language
        self.translations: dict[str, str] = get_translations(selected_language)
        logger.debug("Translations loaded for language: %s", selected_language)

        # 创建窗口
        self.win = tk.Tk()
        self.win.title(self.translations["window_title"])
        self.win.geometry("800x400")  # Set window size to 800x400 pixels
        self.win.resizable(True, True)  # The window can be resized in both directions
        logger.debug("Window created with title: %s", self.translations["window_title"])

        # Create a main frame to center-align the content
        main_frame = ttk.Frame(self.win)
        main_frame.pack(expand=True, fill="both")
        logger.debug("Main frame created and packed")

        # Create UI elements with translated text and icons
        aLabel = ttk.Label(main_frame, text=self.translations["enter_url_label"])
        aLabel.grid(column=0, row=0, padx=10, pady=10)
        self.a_url = ttk.Entry(main_frame)
        self.a_url.grid(column=1, row=0, padx=10, pady=10)
        logger.debug("URL entry field created")

        # Replace with your icon file
        action = ttk.Button(
            main_frame,
            text=self.translations["download_button"],
            command=self._download,
            # image=download_icon,
            compound=tk.LEFT,
        )
        action.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
        logger.debug("Download button created")

        action2 = ttk.Button(
            main_frame,
            text=self.translations["quit_button"],
            command=self._quit,
            # image=quit_icon,
            compound=tk.LEFT,
        )
        action2.grid(column=1, row=2, columnspan=2, padx=10, pady=10)
        logger.debug("Quit button created")

        action3 = ttk.Button(
            main_frame,
            text=self.translations["about_button"],
            command=self._about,
            # image=about_icon,
            compound=tk.LEFT,
        )
        action3.grid(column=0, row=3, columnspan=2, padx=10, pady=10)
        logger.debug("About button created")

        action4 = ttk.Button(
            main_frame,
            text=self.translations["help_button"],
            command=self._help,
            # image=help_icon,
            compound=tk.LEFT,
        )
        action4.grid(column=1, row=3, columnspan=2, padx=10, pady=10)
        logger.debug("Help button created")

        # Create a scrolled text widget
        scrolW = 80
        scrolH = 10
        self.scr = scrolledtext.ScrolledText(
            main_frame, width=scrolW, height=scrolH, wrap=tk.WORD
        )
        self.scr.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
        logger.debug("Scrolled text widget created")

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(
            main_frame, orient="horizontal", length=400, mode="determinate"
        )
        self.progress_bar.grid(column=0, row=4, columnspan=2, padx=10, pady=(10, 0))
        logger.debug("Progress bar created")

        # Percentage label
        self.progress_label = ttk.Label(main_frame, text="0%")
        self.progress_label.grid(column=0, row=5, columnspan=2)
        logger.debug("Progress label created")

        # Cancel button
        self.cancel_download = False  # flag to signal cancellation
        cancel_button = ttk.Button(
            main_frame,
            text=self.translations["cancel_button"],
            command=self._cancel_download,
        )
        cancel_button.grid(column=0, row=6, columnspan=2, pady=(5, 10))

        # Create a menu bar
        menuBar = tk.Menu(self.win)
        self.win.config(menu=menuBar)
        logger.debug("Menu bar created")

        # Set minimum sizes for the main frame and its children
        self.win.update_idletasks()  # Update the window to calculate sizes
        min_width: int = main_frame.winfo_reqwidth()
        min_height: int = main_frame.winfo_reqheight()
        self.win.minsize(min_width, min_height)
        logger.debug("Minimum size set to: %s", f"{min_width}x{min_height}")
        logger.debug("GUI initialized successfully")

    def handle_web_content_fetch(
        self, url: str, stream: bool = False
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
            status_code: str = (
                str(e.response.status_code) if e.response else "No response"
            )
            self.scr.insert(
                tk.INSERT,
                self.translations["failure_message"].format(status_code) + "\n",
            )
            logger.error(
                "Failed to fetch content from %s: %s", url, status_code, exc_info=True
            )
            return None

    def extract_and_display_video_info(self, url: str, html: str) -> Optional[str]:
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
            self.scr.insert(
                tk.INSERT,
                self.translations["video_not_found"].format(str(e)) + "\n",
            )
            logger.error(
                "Video information not found in the web content", exc_info=True
            )
            return ""

        # Display the translated messages and labels
        self.scr.insert(
            tk.INSERT, self.translations["download_video_message"].format(url) + "\n"
        )
        self.scr.insert(
            tk.INSERT, self.translations["video_title"].format(title) + "\n"
        )
        self.scr.insert(tk.INSERT, self.translations["video_url"].format(video) + "\n")
        logger.debug("Extracted video info: Title: %r, URL: %s", title, video)

        return video

    def download_video_and_display_progress(self, resp: requests.Response) -> None:
        """
        Download the video and display the download progress.

        Args:
            resp (requests.Response): The response object containing the video data.
        """
        logger.debug("Starting video download for URL: %s", resp.url)

        content_size: float = int(resp.headers["Content-Length"]) / MB
        parsed_url: ParseResult = urlparse(resp.url)
        if not parsed_url.path:
            self.scr.insert(
                tk.INSERT,
                self.translations["invalid_url_message"].format(resp.url) + "\n",
            )
            logger.error("Invalid URL: %s", resp.url)
            return

        self.scr.insert(
            tk.INSERT,
            self.translations["total_size_message"].format(content_size) + "\n",
        )
        logger.debug("Total size of the video: {:.2f} MB".format(content_size))

        # Extract the media extension from the URL path
        file_extension: str = parsed_url.path.split(".")[-1]
        file_name: str = parsed_url.path.split("/")[-1] or f"video.{file_extension}"
        # Create the file path with the correct extension
        file_path: Path = Path(file_name).with_suffix(f".{file_extension}")

        # Set up progress bar
        self.progress_bar["maximum"] = content_size
        self.progress_bar["value"] = 0
        self.progress_label.config(text="0%")
        self.cancel_download = False  # reset cancel flag
        self.win.update_idletasks()  # Ensure initial draw

        downloaded = 0
        start_time: float = time.time()

        with open(file_path, mode="wb") as f:

            def update_progress() -> None:
                self.progress_bar["value"] = downloaded
                self.progress_label.config(text=f"{percent:.1f}%  ETA: {eta}")

            for chunk in resp.iter_content(MB):
                if self.cancel_download:
                    self.scr.insert(
                        tk.INSERT, self.translations["cancelled_message"] + "\n"
                    )
                    logger.info("Download cancelled by user.")
                    return

                if not chunk:
                    continue

                f.write(chunk)
                downloaded += 1

                percent: float = (downloaded / content_size) * 100
                elapsed: float = time.time() - start_time
                rate: float = downloaded / elapsed if elapsed > 0 else 0
                remaining: float = (content_size - downloaded) / rate if rate > 0 else 0
                eta: str = time.strftime("%M:%S", time.gmtime(remaining))

                self.win.after(0, update_progress)  # Schedule GUI update

        self.win.after(
            0,
            lambda: self.scr.insert(
                tk.INSERT, self.translations["download_complete_message"] + "\n"
            ),
        )
        self.win.after(
            0,
            lambda: self.scr.insert(
                tk.INSERT, self.translations["video_saved"].format(file_path) + "\n"
            ),
        )
        logger.info("Download complete for %r", file_path)

    # 创建一个下载按钮
    def _download(self) -> None:
        """
        Callback function to handle the download button click event.

        Retrieves the video URL from the input field, fetches the web content,
        extracts video information, and downloads the video while displaying
        progress in the GUI.
        """
        logger.debug("Download button clicked")

        url: str = self.a_url.get()
        if not url:
            messagebox.showwarning(
                self.translations["warning_title"],
                self.translations["empty_url_message"],
            )
            logger.warning("No URL provided for download!")
            return

        r: requests.Response | None = self.handle_web_content_fetch(url)
        if r is None:
            return

        video: str | None = self.extract_and_display_video_info(url, r.text)
        if not video:
            return

        resp: requests.Response | None = self.handle_web_content_fetch(
            video, stream=True
        )
        if resp is None:
            return

        try:
            thread = Thread(
                target=self.download_video_and_display_progress,
                args=(resp,),
                daemon=True,
            )
            thread.start()
        except Exception as e:
            self.scr.insert(
                tk.INSERT,
                self.translations["download_failed_message"].format(str(e)) + "\n",
            )
            logger.error("Error downloading video from %s", url, exc_info=True)
            raise

    def _quit(self) -> None:
        """
        Callback function to handle the quit button click event.

        Closes the main application window and exits the program.
        """
        logger.debug("Quit button clicked")

        self.win.quit()
        self.win.destroy()
        logger.debug("Destroyed the main window")

    def _about(self) -> None:
        """
        Callback function to handle the about button click event.

        Displays an informational message box with author, version, and current
        date.
        """
        logger.debug("About button clicked")

        today: str = date.today().strftime("%d/%m/%Y")
        about_message: str = self.translations["about_message"].format(
            AUTHOR, VERSION, today
        )
        messagebox.showinfo(self.translations["about_button"], about_message)

    def _help(self) -> None:
        """
        Callback function to handle the help button click event.

        Displays an informational message box with usage instructions or help
        content.
        """
        logger.debug("Help button clicked")

        messagebox.showinfo(
            self.translations["help_button"], self.translations["help_message"]
        )

    def _cancel_download(self) -> None:
        """Sets the cancel flag to True."""
        logger.debug("Cancel download button clicked")
        self.cancel_download = True

    def run(self) -> None:
        """Run the program."""
        logger.debug("Starting the main loop of the GUI")

        self.win.mainloop()
