"""Main module for the SpankBang Downloader."""

from argparse import Namespace

from core_helpers.updates import check_updates
from rich.traceback import install

from .cli import get_parsed_args
from .consts import EXIT_SUCCESS, GITHUB
from .consts import __version__ as VERSION
from .gui import VideoDownloaderUI
from .logs import logger
from .translations import select_language
from .utils import exit_session


def main() -> None:
    args: Namespace = get_parsed_args()
    install(show_locals=args.debug)
    logger.info("Start of session")

    if GITHUB:
        check_updates(GITHUB, VERSION)

    if not args.language:
        logger.info("No language specified, prompting user to select one")
        language: str = select_language()
    else:
        language = args.language

    logger.info(f"Language specified: {language}")

    ui = VideoDownloaderUI(language)
    ui.run()

    exit_session(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
