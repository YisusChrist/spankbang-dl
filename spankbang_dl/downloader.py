import re

import requests

from .logs import logger

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.6",
    "Cookie": "coe=es; cfc_ok=00|2|es|www|master|0; ana_vid=713ca8f89270aefc942853c0e00c9fc843d98f720c9768719f81a54435f1576c; age_pass=1; cor=M; backend_version=main; cf_clearance=3.1sPebhq_Jd4veXaYld6yisbz.MgLMsW3ywx7Zzgcw-1695236852-0-1-605e7b01.6c69a1e6.dde1b57d-0.2.1695236852; pg_pop_v5=1; pg_interstitial_v5=1; preroll_skip=1; ana_sid=e2d3432ee672c104a4dd7cd9a2884d14c3cc875b5bcb1aad27ad8e0269b5f553; sb_session=eyJfcGVybWFuZW50Ijp0cnVlfQ.ZQuDxA.xisZQRjXFstaOfWLZWfMs32orYQ; __cf_bm=nYQSTL6vzbUnYCWosR8Z2Cu3HOmYytNsj4CQ505YLkM-1695253310-0-Aax/O+XC4BujMoByVTOYQJiAgg/9tMKyNoPRrpqkCrjhJvh65g8TjFD1aJboO68Fk1lSAYYCSsCK7bNSwubv0qQ=",
    "Dnt": "1",
    "Sec-Ch-Ua": '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
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
        session = requests.Session()

        headers["Referer"] = url

        response = session.get(url, headers=headers, stream=stream)
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
