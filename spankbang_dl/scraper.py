import cloudscraper  # type: ignore
import requests
from bs4 import BeautifulSoup

from .logs import logger

headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}


def fetch_web_content(url: str, **kwargs) -> requests.Response:
    """Fetch the web content from the given URL.

    Args:
        url (str): The URL to fetch the content from.
        **kwargs: Additional keyword arguments to pass to the request.

    Returns:
        requests.Response: The response object.
    """
    logger.debug("Fetching web content from URL: %s", url)

    scraper: cloudscraper.CloudScraper = cloudscraper.create_scraper()

    headers["Referer"] = url

    response: requests.Response = scraper.get(url, headers=headers, **kwargs)
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

    soup = BeautifulSoup(html, "html.parser")

    # Find the video container div
    video_container = soup.find("div", id="video_container")
    if not video_container:
        raise Exception("Video container not found in HTML.")

    # Find the <video> tag inside the container
    video_tag = video_container.find("video")
    if not video_tag:
        raise Exception(
            "Video tag with 'src' attribute not found inside video container."
        )

    src: str = video_tag.find("source")["src"]

    # Extract the title from the <title> tag
    title_tag = soup.find("title")
    if not title_tag:
        raise Exception("Title tag not found in HTML.")

    title_text: str = title_tag.get_text(strip=True)
    if not title_text.startswith("Watch"):
        raise Exception("Title format not recognized.")

    # Extract the portion between "Watch" and " -"
    title: str = title_text.removeprefix("Watch").split(" - ")[0].strip()

    return title, src
