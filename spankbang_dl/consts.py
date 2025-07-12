"""Constants for the project."""

from pathlib import Path
from core_helpers.xdg_paths import PathType, get_user_path

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore

__version__ = metadata.version(__package__ or __name__)
__desc__ = metadata.metadata(__package__ or __name__)["Summary"]
PACKAGE = metadata.metadata(__package__ or __name__)["Name"]
GITHUB = metadata.metadata(__package__ or __name__)["Home-page"]
AUTHOR = metadata.metadata(__package__ or __name__)["Author"]

CONFIG_PATH = get_user_path(PACKAGE, PathType.CONFIG)
CONFIG_FILE = CONFIG_PATH / f"{PACKAGE}.ini"
LOG_PATH = get_user_path(PACKAGE, PathType.LOG)
LOG_FILE = LOG_PATH / f"{PACKAGE}.log"
STRINGS_PATH = (Path(__file__).parent / "strings").resolve()

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

DEBUG = False
PROFILE = False

MB = 1024 * 1024
