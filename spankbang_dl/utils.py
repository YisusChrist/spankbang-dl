import sys

import requests
import semver
from rich import print

from .consts import EXIT_FAILURE, LOG_PATH, VERSION
from .logs import logger


def pretty_print_http_request(req: requests.models.PreparedRequest) -> None:
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.

    Reference: https://stackoverflow.com/a/23816211/19705722

    Args:
        req (requests.models.PreparedRequest): The request to print.
    """
    if "Host" not in req.headers:
        req.headers["Host"] = req.url.split("/")[2]

    path = req.url.split(req.headers["Host"])[-1]
    http_version = f"HTTP/1.1"

    print(
        "{}\n{}\r\n{}\r\n\r\n{}\n{}".format(
            "-----------START-----------",
            f"{req.method} {path} {http_version}",
            "\r\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
            req.body or "",
            "------------END------------",
        )
    )


def pretty_print_http_response(resp: requests.models.Response) -> None:
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.

    Args:
        resp (requests.models.Response): The response to print.
    """
    http_version = f"HTTP/{resp.raw.version // 10}.{resp.raw.version % 10}"

    print(
        "{}\n{}\r\n{}\r\n\r\n{}\n{}".format(
            "-----------START-----------",
            f"{http_version} {resp.status_code} {resp.reason}",
            "\r\n".join("{}: {}".format(k, v) for k, v in resp.headers.items()),
            resp.text or resp.content.decode(),
            "------------END------------",
        )
    )


def check_for_updates():
    """Check if there is a newer version of the script available in the GitHub repository."""
    logger.debug("Checking for updates")

    print("[bold yellow]Checking for updates...[/bold yellow]")

    try:
        project = "yisuschrist/spankbang-dl"
        repo_url = f"https://api.github.com/repos/{project}/releases/latest"

        response = requests.get(repo_url)
        response.raise_for_status()
        latest_version = response.json()["tag_name"]

        if semver.compare(latest_version, VERSION) > 0:
            print(
                f"\n[yellow]Newer version of the script available: {latest_version}.\n"
                "Please consider updating your version.[/yellow]"
            )
        else:
            print("[green]You are using the latest version of the script[/green]")
    except requests.exceptions.RequestException:
        print("[bold red]Could not check for updates[/bold red]")


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
