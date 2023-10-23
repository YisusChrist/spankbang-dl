import json
import os
from pathlib import Path

import inquirer

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
        return answer["language"]
    except:
        exit_session(EXIT_FAILURE)


def detect_available_languages() -> list:
    """
    Detect the available languages in the strings folder.

    Returns:
        list: The available languages.
    """
    logger.debug("Detecting available languages")

    available_languages = []
    for filename in os.listdir(STRINGS_PATH):
        if filename.startswith("strings_") and filename.endswith(".json"):
            lang_code = filename.replace("strings_", "").replace(".json", "")
            available_languages.append(lang_code)
    return available_languages


def get_translations(selected_language: str) -> dict:
    """
    Get the translations for the selected language.

    Args:
        selected_language (str): The selected language.

    Returns:
        dict: The translations.
    """
    logger.debug("Getting translations")

    file = Path(STRINGS_PATH).resolve() / f"strings_{selected_language}.json"
    with open(file, encoding="utf-8") as json_file:
        translations = json.load(json_file)
    return translations
