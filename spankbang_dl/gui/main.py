import tkinter as tk
from tkinter import ttk

from core_helpers.logs import logger

from ..translations import detect_available_languages, get_translations
from . import commands


class VideoDownloaderUI:
    """
    A class to create the GUI interface.

    Args:
        selected_language (str, optional): The selected language. Defaults to "en".

    Attributes:
        win (tk.Tk): The main window.
        translations (dict): The translations for the selected language.

    Methods:
        log_message: Safely inserts text into the read-only text area.
        change_language: Change the UI language.
        run: Run the program.
    """

    window_height: int = 1400
    window_width: int = 1200

    cancel_download = False
    pause_download = False
    downloading = False

    def __init__(self, selected_language: str = "en") -> None:
        logger.debug("Creating GUI with selected language: %s", selected_language)

        self.current_language = selected_language
        # Load translations for the selected language
        self.translations: dict[str, str] = get_translations(selected_language)
        logger.debug("Translations loaded for language: %s", selected_language)

        # Main window configurations
        self.win = tk.Tk()
        self.win.title(self.translations["window_title"])
        self.win.geometry(f"{self.window_width}x{self.window_height}")
        logger.debug("Window created with title: %s", self.translations["window_title"])

        # Configure overall grid weights for responsiveness
        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(0, weight=1)

        # Set a modern clean theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Main container padding
        self.main_frame = ttk.Frame(self.win, padding="15")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)  # Give the text area the most weight

        # ---- Row 0: URL Input Area ----
        self.url_frame = ttk.LabelFrame(
            self.main_frame, text=self.translations["enter_url_label"], padding="10"
        )
        self.url_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.url_frame.columnconfigure(0, weight=1)

        self.a_url = ttk.Entry(self.url_frame, font=("Segoe UI", 10))
        self.a_url.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        logger.debug("URL entry field created")

        # ---- Row 1: Progress Bar ----
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.progress_frame.columnconfigure(0, weight=1)
        logger.debug("Progress frame created")

        self.progress_bar = ttk.Progressbar(
            self.progress_frame, orient="horizontal", mode="determinate"
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew")
        logger.debug("Progress bar created")

        # Percentage Label (Dynamic StringVar)
        self.progress_percent = tk.StringVar(value="0%")
        self.progress_label = ttk.Label(
            self.progress_frame,
            textvariable=self.progress_percent,
            font=("Segoe UI", 10, "bold"),
            width=6,
            anchor="center",
        )
        self.progress_label.grid(row=0, column=1, padx=(0, 10))
        logger.debug("Progress label created")

        # ---- Row 2: Read-Only Output Log ----
        self.log_frame = ttk.LabelFrame(
            self.main_frame, text=self.translations["log_frame_label"], padding="10"
        )
        self.log_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        # Text widget with a scrollbar
        self.log_text = tk.Text(
            self.log_frame,
            wrap="word",
            font=("Consolas", 9),
            state="disabled",
            bg="#f8f9fa",
            fg="#333333",
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        logger.debug("Scrolled text widget created")

        self.scrollbar = ttk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text["yscrollcommand"] = self.scrollbar.set
        logger.debug("Scroll bar created")

        # Write initial sample messages to log
        self.log_message(self.translations["startup_message"])

        # ---- Row 3: Control Buttons ----
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        self.start_btn = ttk.Button(
            self.progress_frame,
            text="▶",
            width=3,
            command=lambda: commands.start_download_thread(self),
        )
        self.start_btn.grid(row=0, column=2, padx=2)
        logger.debug("Download button created")

        self.pause_btn = ttk.Button(
            self.progress_frame,
            text="⏸",
            width=3,
            command=lambda: commands.pause_resume_download(self),
        )
        self.pause_btn.grid(row=0, column=3, padx=2)
        logger.debug("Pause button created")

        self.stop_btn = ttk.Button(
            self.progress_frame,
            text="⏹",
            width=3,
            command=lambda: commands.cancel_download(self),
        )
        self.stop_btn.grid(row=0, column=4, padx=(2, 0))
        logger.debug("Stop button created")

        # ---- Row 4: Utility Footer (Help, About, Language) ----
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.grid(row=4, column=0, sticky="ew")
        # Pushes language selector to the right
        self.footer_frame.columnconfigure(2, weight=1)

        self.help_btn = ttk.Button(
            self.footer_frame,
            text=self.translations["help_button"],
            width=10,
            command=lambda: commands.show_help(self),
        )
        self.help_btn.grid(row=0, column=0, padx=(0, 5))
        logger.debug("Help button created")

        self.about_btn = ttk.Button(
            self.footer_frame,
            text=self.translations["about_button"],
            width=10,
            command=lambda: commands.show_about(self),
        )
        self.about_btn.grid(row=0, column=1, padx=5)
        logger.debug("About button created")

        # Language Dropdown Selection
        self.lang_label = ttk.Label(
            self.footer_frame, text=self.translations["language"]
        )
        self.lang_label.grid(row=0, column=3, padx=(0, 5))

        self.languages = detect_available_languages()
        self.selected_lang = tk.StringVar(value=self.current_language)
        self.lang_menu = ttk.OptionMenu(
            self.footer_frame,
            self.selected_lang,
            self.current_language,
            *self.languages,
            command=self.change_language,
        )
        self.lang_menu.grid(row=0, column=4, sticky="e")
        logger.debug("Language dropdown menu created")

        self.win.update_idletasks()  # Update the window to calculate sizes
        min_width: int = self.main_frame.winfo_reqwidth()
        min_height: int = self.main_frame.winfo_reqheight()
        self.win.minsize(min_width, min_height)
        logger.debug("Minimum size set to: %s", f"{min_width}x{min_height}")

        logger.debug("GUI initialized successfully")

    # ---- Helper Methods ----

    def log_message(self, message) -> None:
        """Safely inserts text into the read-only text area."""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[Log] {message}\n")
        self.log_text.see(tk.END)  # Auto-scroll to the bottom
        self.log_text.config(state="disabled")

    # ---- Action Commands ----

    def change_language(self, choice) -> None:
        commands.change_language(self, choice)

    def run(self) -> None:
        """Run the program."""
        logger.debug("Starting the main loop of the GUI")

        self.win.mainloop()
