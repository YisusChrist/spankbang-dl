import re

import cloudscraper  # type: ignore
import requests

from .logs import logger

headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}


def fetch_web_content(
    translations: dict[str, str], url: str, stream: bool = True
) -> requests.Response:
    """Fetch the web content from the given URL.

    Args:
        translations (dict[str, str]): A dictionary containing translation strings.
        url (str): The URL to fetch the content from.
        stream (bool, optional): Whether to stream the content or not. Defaults to True.

    Returns:
        requests.Response: The response object.

    Raises:
        requests.exceptions.RequestException: If there is an error during the request.
    """
    try:
        scraper: cloudscraper.CloudScraper = cloudscraper.create_scraper()

        headers["Referer"] = url

        response: requests.Response = scraper.get(url, headers=headers, stream=stream)
        response.raise_for_status()

        print(translations["success_message"].format(str(response.status_code)))
        return response

    except requests.exceptions.RequestException as e:
        print(translations["failure_message"].format(str(e)))
        logger.error(e)
        raise


def extract_video_info(translations: dict[str, str], html: str) -> tuple[str, str]:
    """
    Extract video information from the HTML content.

    Args:
        translations (dict[str, str]): A dictionary containing translation strings.
        html (str): The HTML content to extract information from.

    Returns:
        tuple[str, str]: A tuple containing the video title and source URL.

    Raises:
        Exception: If the video information cannot be extracted.
    """
    try:
        result: re.Match[str] | None = re.search(
            '<video.*?src="(.*?)".*?>.*?</video>', html, re.S
        )
        src: str = result.group(1)
        result2: re.Match[str] | None = re.search(
            "<title.*?>Watch(.*?) - .*?</title.*?>", html, re.S
        )
        title: str = result2.group(1)

        return title, src
    except Exception as e:
        print(translations["video_not_found"], e)
        logger.error(e)
        raise
