"""Main module for the SpankBang Downloader."""

from argparse import Namespace

from core_helpers.logs import logger
from core_helpers.updates import check_updates
from rich.traceback import install

from spankbang_dl.cli import get_parsed_args
from spankbang_dl.consts import EXIT_SUCCESS, GITHUB, LOG_FILE, PACKAGE
from spankbang_dl.consts import __version__ as VERSION
from spankbang_dl.gui import VideoDownloaderUI
from spankbang_dl.translations import select_language
from spankbang_dl.utils import exit_session


def main() -> None:
    args: Namespace = get_parsed_args()
    install(show_locals=args.debug)
    logger.setup_logger(PACKAGE, LOG_FILE, args.debug, args.verbose)
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
