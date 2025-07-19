# 写UI
import sys
import tkinter as tk
from datetime import date
from tkinter import messagebox, scrolledtext, ttk

import requests
from tqdm import tqdm  # type: ignore

from .consts import AUTHOR, MB
from .consts import __version__ as VERSION
from .downloader import extract_video_info, fetch_web_content
from .logs import logger
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
            selected_language (str, optional): The selected language.
                Defaults to "en".
        """
        # 创建窗口
        self.translations: dict[str, str] = get_translations(selected_language)

        self.win = tk.Tk()
        self.win.title(self.translations["window_title"])
        self.win.geometry("800x400")  # Set window size to 800x400 pixels
        self.win.resizable(True, True)  # The window can be resized in both directions

        # Create a main frame to center-align the content
        main_frame = ttk.Frame(self.win)
        main_frame.pack(expand=True, fill="both")

        # Create UI elements with translated text and icons
        aLabel = ttk.Label(main_frame, text=self.translations["enter_url_label"])
        aLabel.grid(column=0, row=0, padx=10, pady=10)
        self.a_url = ttk.Entry(main_frame)
        self.a_url.grid(column=1, row=0, padx=10, pady=10)

        # Replace with your icon file
        action = ttk.Button(
            main_frame,
            text=self.translations["download_button"],
            command=self._download,
            # image=download_icon,
            compound=tk.LEFT,
        )
        action.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

        action2 = ttk.Button(
            main_frame,
            text=self.translations["quit_button"],
            command=self._quit,
            # image=quit_icon,
            compound=tk.LEFT,
        )
        action2.grid(column=1, row=2, columnspan=2, padx=10, pady=10)

        action3 = ttk.Button(
            main_frame,
            text=self.translations["about_button"],
            command=self._about,
            # image=about_icon,
            compound=tk.LEFT,
        )
        action3.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

        action4 = ttk.Button(
            main_frame,
            text=self.translations["help_button"],
            command=self._help,
            # image=help_icon,
            compound=tk.LEFT,
        )
        action4.grid(column=1, row=3, columnspan=2, padx=10, pady=10)

        # Create a scrolled text widget
        scrolW = 80
        scrolH = 10
        self.scr = scrolledtext.ScrolledText(
            main_frame, width=scrolW, height=scrolH, wrap=tk.WORD
        )
        self.scr.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(
            main_frame, orient="horizontal", length=400, mode="determinate"
        )
        self.progress_bar.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

        # Create a menu bar
        menuBar = tk.Menu(self.win)
        self.win.config(menu=menuBar)

        # Set minimum sizes for the main frame and its children
        self.win.update_idletasks()  # Update the window to calculate sizes
        min_width: int = main_frame.winfo_reqwidth()
        min_height: int = main_frame.winfo_reqheight()
        self.win.minsize(min_width, min_height)

    def handle_web_content_fetch(self, url: str) -> requests.Response | None:
        """
        Fetch web content from the given URL and handle exceptions.

        Args:
            url (str): The URL to fetch web content from.

        Returns:
            requests.Response | None: The response object if successful, None
            otherwise.
        """
        try:
            response: requests.Response = fetch_web_content(
                self.translations, url, stream=True
            )
            if response.status_code != 200:
                self.scr.insert(
                    tk.INSERT,
                    self.translations["failure_message"]
                    + str(response.status_code)
                    + "\n",
                )
            return response

        except requests.exceptions.RequestException as e:
            logger.error(e)
            self.scr.insert(
                tk.INSERT,
                self.translations["download_failed_message"].format(str(e)) + "\n",
            )
            return None

    def extract_and_display_video_info(self, html: str) -> str:
        """
        Extract and display video information.

        Args:
            html (str): The HTML content of the page.

        Returns:
            str: The video title.
        """
        try:
            result, title = extract_video_info(self.translations, html)

            # Display the translated messages and labels
            self.scr.insert(
                tk.INSERT, self.translations["download_video_message"].format(title)
            )
            self.scr.insert(tk.INSERT, self.translations["video_title"].format(title))
            self.scr.insert(tk.INSERT, self.translations["video_url"].format(result))

            return title
        except Exception as e:
            self.scr.insert(
                tk.INSERT,
                self.translations["download_failed_message"].format(str(e)) + "\n",
            )
            logger.error(e)
            raise

    def download_video_and_display_progress(
        self, resp: requests.Response, title: str
    ) -> None:
        """
        Download the video and display the download progress.

        Args:
            resp (requests.Response): The response object containing the video data.
            title (str): The title of the video.
        """
        content_size: float = int(resp.headers["Content-Length"]) / MB
        with open(title + ".mp4", mode="wb") as f:
            self.scr.insert(
                tk.INSERT,
                self.translations["total_size_message"].format(content_size),
            )
            for data in tqdm(
                iterable=resp.iter_content(MB),
                total=content_size,
                unit="MB",
                desc=title,
                gui=True,
                leave=False,
                position=1,
                file=sys.stdout,
            ):
                f.write(data)
                # Update the progress bar
                # self.progress_bar["value"] = download_progress_percentage
            self.scr.insert(
                tk.INSERT, self.translations["download_complete_message"] + "\n"
            )

    # 创建一个下载按钮
    def _download(self) -> None:
        """
        Callback function to handle the download button click event.

        Retrieves the video URL from the input field, fetches the web content,
        extracts video information, and downloads the video while displaying
        progress in the GUI.
        """
        logger.debug("Downloading video")

        url: str = self.a_url.get()

        r: requests.Response | None = self.handle_web_content_fetch(url)
        if r is None:
            return

        title: str = self.extract_and_display_video_info(r.text)
        resp: requests.Response | None = self.handle_web_content_fetch(title)
        if resp is None:
            return
        
        self.download_video_and_display_progress(resp, title)

    def _quit(self) -> None:
        """
        Callback function to handle the quit button click event.

        Closes the main application window and exits the program.
        """
        logger.debug("Quitting program")

        self.win.quit()
        self.win.destroy()
        exit()

    def _about(self) -> None:
        """
        Callback function to handle the about button click event.

        Displays an informational message box with author, version, and current
        date.
        """
        logger.debug("Showing about message")

        today: str = date.today().strftime("%d/%m/%Y")
        about_message: str = self.translations["about_message"].format(
            AUTHOR, VERSION, today
        )
        messagebox.showinfo("About", about_message)

    def _help(self) -> None:
        """
        Callback function to handle the help button click event.

        Displays an informational message box with usage instructions or help
        content.
        """
        logger.debug("Showing help message")

        help_message = self.translations["help_message"]
        messagebox.showinfo("Help", help_message)

    def run(self) -> None:
        """Run the program."""
        logger.debug("Running program")

        self.win.mainloop()
