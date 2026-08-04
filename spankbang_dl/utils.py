import sys

from core_helpers.logs import logger
from rich import print

from spankbang_dl.consts import EXIT_FAILURE, LOG_PATH


def format_file_size(size_in_bytes, unit: str = "B", lowercase: bool = False):
    # The units we want to cycle through
    prefixes = ["", "K", "M", "G", "T", "P"]

    size = float(size_in_bytes)
    unit_index = 0

    # Divide by 1024 until the size is less than 1024
    while size >= 1024 and unit_index < len(prefixes) - 1:
        size /= 1024
        unit_index += 1

    # Return formatted string: .2f removes unnecessary decimal clutter
    final_unit = (prefixes[unit_index] + unit).strip()
    if lowercase:
        final_unit = final_unit.lower()

    return f"{size:.2f} {final_unit}"


def exit_session(exit_value: int) -> None:
    """
    Exit the program with the given exit value.

    Args:
        exit_value (int): The POSIX exit value to exit with.
    """
    logger.info("End of session")
    # Check if the exit_value is a valid POSIX exit value
    if not 0 <= exit_value <= 255:
        exit_value = EXIT_FAILURE

    if exit_value == EXIT_FAILURE:
        print(
            "[red]There were errors during the execution of the script. "
            f"Check the logs at {LOG_PATH} for more information.[/red]"
        )

    # Exit the program with the given exit value
    sys.exit(exit_value)
