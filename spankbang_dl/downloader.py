import re

import cloudscraper  # type: ignore
import requests

from .logs import logger

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}


def fetch_web_content(
    translations: dict, url: str, stream: bool = True
) -> requests.Response:
    """Fetch the web content from the given URL.

    Args:
        url (str): The URL to fetch the content from.
        headers (dict): The headers to use when fetching the content.
        stream (bool, optional): Whether to stream the content or not. Defaults to True.

    Returns:
        requests.Response: The response object.
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


def extract_video_info(translations, html):
    try:
        result = re.search('<video.*?src="(.*?)".*?>.*?</video>', html, re.S)
        src = result.group(1)
        result2 = re.search("<title.*?>Watch(.*?) - .*?</title.*?>", html, re.S)
        title = result2.group(1)

        return title, src
    except Exception as e:
        print(translations["video_not_found"], e)
        logger.error(e)
        raise
