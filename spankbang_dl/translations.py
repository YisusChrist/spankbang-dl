import json

import inquirer  # type: ignore
from rich import print

from .consts import EXIT_FAILURE, STRINGS_PATH
from .logs import logger
from .utils import exit_session


def select_language() -> str:
    """
    Ask the user to select a language from the available languages.

    Returns:
        str: The selected language.
    """
    logger.debug("Selecting language")
    available_languages = detect_available_languages()
    if not available_languages:
        print("[red]ERROR[/]: No available languages found")
        logger.error("No available languages found")
        exit_session(EXIT_FAILURE)

    try:
        # Ask the user to select a column to use as key
        questions = [
            inquirer.List(
                "language",
                message="Select your language",
                choices=available_languages,
            ),
        ]
        answer = inquirer.prompt(questions)
    except:
        exit_session(EXIT_FAILURE)
    return answer["language"]


def detect_available_languages() -> list:
    """
    Detect the available languages in the strings folder.

    Returns:
        list: The available languages.
    """
    logger.debug("Detecting available languages")

    return [
        file.stem.replace("strings_", "")
        for file in STRINGS_PATH.glob("strings_*.json")
    ]


def get_translations(selected_language: str) -> dict:
    """
    Get the translations for the selected language.

    Args:
        selected_language (str): The selected language.

    Returns:
        dict: The translations.
    """
    logger.debug("Getting translations")

    file = STRINGS_PATH / f"strings_{selected_language}.json"
    with open(file, encoding="utf-8") as json_file:
        return json.load(json_file)
