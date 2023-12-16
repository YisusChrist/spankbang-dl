#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from rich.traceback import install
from rich_argparse_plus import RichHelpFormatterPlus

from .consts import DESC, EXIT_SUCCESS, NAME, VERSION
from .gui import VideoDownloaderUI
from .logs import logger
from .translations import detect_available_languages, select_language
from .utils import exit_session, check_for_updates


def get_parsed_args() -> argparse.Namespace:
    """
    Parse and return command-line arguments.

    Returns:
        The parsed arguments as an argparse.Namespace object.
    """
    global parser

    RichHelpFormatterPlus.choose_theme("grey_area")

    parser = argparse.ArgumentParser(
        description=DESC,  # Program description
        formatter_class=RichHelpFormatterPlus,  # Disable line wrapping
        allow_abbrev=False,  # Disable abbreviations
        add_help=False,  # Disable default help
    )

    # Create a group for the required arguments
    g_required = parser.add_argument_group("Required Arguments")

    # Language
    g_required.add_argument(
        "-l",
        "--language",
        type=str,
        choices=detect_available_languages(),
        # default="en",
        help="The language to use. Default is English.",
    )

    g_misc = parser.add_argument_group("Miscellaneous Options")
    # Help
    g_misc.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    # Verbose
    g_misc.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Show log messages on screen. Default is False.",
    )
    # Debug
    g_misc.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Activate debug logs. Default is False.",
    )
    g_misc.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show version number and exit.",
        version=f"[argparse.prog]{NAME}[/] version [i]{VERSION}[/]",
    )

    return parser.parse_args()


def main():
    args = get_parsed_args()
    logger.info("Start of session")

    check_for_updates()

    if not args.language:
        logger.info("No language specified, prompting user to select one")
        language = select_language()
    else:
        language = args.language

    logger.info(f"Language specified: {language}")

    ui = VideoDownloaderUI(language)
    ui.run()

    exit_session(EXIT_SUCCESS)


if __name__ == "__main__":
    install(show_locals=False)
    main()
