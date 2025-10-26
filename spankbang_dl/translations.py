import json
from pathlib import Path

import inquirer  # type: ignore
from core_helpers.logs import logger
from rich import print

from spankbang_dl.consts import EXIT_FAILURE, STRINGS_PATH
from spankbang_dl.utils import exit_session


def select_language() -> str:
    """
    Ask the user to select a language from the available languages.

    Returns:
        str: The selected language.
    """
    logger.debug("Selecting language")
    available_languages: list[str] = detect_available_languages()
    if not available_languages:
        print("[red]ERROR[/]: No available languages found")
        logger.error("No available languages found")
        exit_session(EXIT_FAILURE)

    try:
        # Ask the user to select a column to use as key
        questions: list[inquirer.List] = [
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


def detect_available_languages() -> list[str]:
    """
    Detect the available languages in the strings folder.

    Returns:
        list[str]: The available languages.
    """
    return [
        file.stem.replace("strings_", "")
        for file in STRINGS_PATH.glob("strings_*.json")
    ]


def get_translations(selected_language: str) -> dict[str, str]:
    """
    Get the translations for the selected language.

    Args:
        selected_language (str): The selected language.

    Returns:
        dict[str, str]: The translations.
    """
    logger.debug("Loading translations for language: %s", selected_language)

    file: Path = STRINGS_PATH / f"strings_{selected_language}.json"
    with open(file, encoding="utf-8") as json_file:
        return json.load(json_file)
