import re

import cloudscraper  # type: ignore
import requests

from .logs import logger

headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}


def fetch_web_content(url: str, stream: bool = True) -> requests.Response:
    """Fetch the web content from the given URL.

    Args:
        url (str): The URL to fetch the content from.
        stream (bool): Whether to stream the content or not. Defaults to True.

    Returns:
        requests.Response: The response object.
    """
    logger.debug("Fetching web content from URL: %s", url)

    scraper: cloudscraper.CloudScraper = cloudscraper.create_scraper()

    headers["Referer"] = url

    response: requests.Response = scraper.get(url, headers=headers, stream=stream)
    response.raise_for_status()

    return response


def extract_video_info(html: str) -> tuple[str, str]:
    """
    Extract video information from the HTML content.

    Args:
        html (str): The HTML content to extract information from.

    Returns:
        tuple[str, str]: A tuple containing the video title and source URL.

    Raises:
        Exception: If the video information cannot be extracted.
    """
    logger.debug("Extracting video information from HTML content")

    result: re.Match[str] | None = re.search(
        '<video.*?src="(.*?)".*?>.*?</video>', html, re.S
    )
    src: str = result.group(1)
    result2: re.Match[str] | None = re.search(
        "<title.*?>Watch(.*?) - .*?</title.*?>", html, re.S
    )
    title: str = result2.group(1).strip()

    return title, src
