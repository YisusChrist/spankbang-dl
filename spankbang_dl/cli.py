"""Command-line interface for the program."""

from argparse import Namespace

from core_helpers.cli import ArgparseColorThemes, setup_parser

from .consts import PACKAGE
from .consts import __desc__ as DESC
from .consts import __version__ as VERSION
from .translations import detect_available_languages


def get_parsed_args() -> Namespace:
    """
    Parse and return command-line arguments.

    Returns:
        The parsed arguments as an argparse.Namespace object.
    """
    parser, g_required = setup_parser(
        package=PACKAGE,
        description=DESC,
        version=VERSION,
        theme=ArgparseColorThemes.GREY_AREA,
    )

    # Language
    g_required.add_argument(
        "-l",
        "--language",
        type=str,
        choices=detect_available_languages(),
        # default="en",
        help="The language to use. Default is English.",
    )

    return parser.parse_args()
