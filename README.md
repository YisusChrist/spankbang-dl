[中文版本](.github/README.zh.md)

# Spankbang-Downloader

<p align="center">
    <img width="350" src="https://logos-world.net/wp-content/uploads/2023/01/SpankBang-Logo.png" alt="SpankBang logo">
</p>

<p align="center">
    <a href="https://github.com/YisusChrist/spankbang-dl/issues">
        <img src="https://img.shields.io/github/issues/YisusChrist/spankbang-dl?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/spankbang-dl/forks">
        <img src="https://img.shields.io/github/forks/YisusChrist/spankbang-dl?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/spankbang-dl/stargazers">
        <img src="https://img.shields.io/github/stars/YisusChrist/spankbang-dl?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/spankbang-dl/actions">
        <img alt="Tests Passing" src="https://github.com/YisusChrist/spankbang-dl/actions/workflows/github-code-scanning/codeql/badge.svg">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/spankbang-dl/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/YisusChrist/spankbang-dl?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/GPL-3.0/">
        <img alt="License" src="https://img.shields.io/github/license/YisusChrist/spankbang-dl?color=0088ff">
    </a>
</p>

<br>

<p align="center">
    <a href="https://github.com/YisusChrist/spankbang-dl/issues/new?assignees=YisusChrist&labels=bug&projects=&template=bug_report.yml">Report Bug</a>
    ·
    <a href="https://github.com/YisusChrist/spankbang-dl/issues/new?assignees=YisusChrist&labels=feature&projects=&template=feature_request.yml">Request Feature</a>
    ·
    <a href="https://github.com/YisusChrist/spankbang-dl/issues/new?assignees=YisusChrist&labels=question&projects=&template=question.yml">Ask Question</a>
    ·
    <a href="https://github.com/YisusChrist/spankbang-dl/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

![Alt](https://repobeats.axiom.co/api/embed/34abb58ec050df071832263d550f7db8cbd6f2e8.svg "Repobeats analytics image")

<br>

`spankbang-dl` is a GUI Python app that allows you to download albums from Spankbang. The GUI is built using [tkinter](https://docs.python.org/3/library/tkinter.html), a standard Python library for creating graphical user interfaces. The app is designed to be:

- User-friendly and easy to use, making it accessible for everyone
- Lightweight and fast, allowing you to download albums quickly and efficiently

<details>
<summary>Table of Contents</summary>

- [Spankbang-Downloader](#spankbang-downloader)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [From PyPI](#from-pypi)
    - [Manual installation](#manual-installation)
    - [Uninstall](#uninstall)
  - [Usage](#usage)
    - [Example of execution](#example-of-execution)
  - [Contributors](#contributors)
    - [How do I contribute to spankbang-dl?](#how-do-i-contribute-to-spankbang-dl)
  - [License](#license)
  - [Credits](#credits)

</details>

## Requirements

Here's a breakdown of the packages needed and their versions:

- [poetry](https://pypi.org/project/poetry) >= 1.7.1 (_only for manual installation_)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4) >= 4.13.4
- [cloudscraper](https://pypi.org/project/cloudscraper) >= 1.2.71
- [core-helpers](https://pypi.org/project/core-helpers) >= 1.2.0
- [inquirer](https://pypi.org/project/inquirer) >= 3.1.3
- [requests](https://pypi.org/project/requests) >= 2.31.0
- [rich](https://pypi.org/project/rich) >= 13.5.3

> [!NOTE]
> The software has been developed and tested using Python `3.13.5`. The minimum required version to run the software is Python 3.9. Although the software may work with previous versions, it is not guaranteed.

## Installation

### From PyPI

`spankbang-dl` can be installed easily as a PyPI package. Just run the following command:

```bash
pip3 install spankbang-dl
```

> [!IMPORTANT]
> For best practices and to avoid potential conflicts with your global Python environment, it is strongly recommended to install this program within a virtual environment. Avoid using the --user option for global installations. We highly recommend using [pipx](https://pypi.org/project/pipx) for a safe and isolated installation experience. Therefore, the appropriate command to install `spankbang-dl` would be:
>
> ```bash
> pipx install spankbang-dl
> ```

The program can now be ran from a terminal with the `spankbang-dl` command.

### Manual installation

If you prefer to install the program manually, follow these steps:

> [!WARNING]
> This will install the version from the latest commit, not the latest release.

1. Download the latest version of [spankbang-dl](https://github.com/YisusChrist/spankbang-dl) from this repository:

   ```bash
   git clone https://github.com/YisusChrist/spankbang-dl
   cd spankbang-dl
   ```

2. Install the package:

   ```bash
   poetry install --only main
   ```

3. Run the program:

   ```bash
   poetry run spankbang-dl
   ```

If you prefer, you can directly install the package from the repository using `pip`/`pipx`:

```bash
pipx install git+https://github.com/YisusChrist/spankbang-dl.git
```

### Uninstall

If you installed it using `pip`/`pipx`, you can use the following command:

```bash
pipx uninstall spankbang-dl
```

## Usage

> [!TIP]
> For more information about the usage of the program, run `spankbang-dl --help` or `spankbang-dl -h`.

![Usage](https://i.imgur.com/nOnokO8.png)

The program can be run from the terminal with the `spankbang-dl` command. It will open a window where you can introduce the URL of the video you want to download.

### Example of execution

https://github.com/user-attachments/assets/32c3911a-a756-44f8-b4a5-ba4ba472dc9e

## Contributors

<a href="https://github.com/YisusChrist/spankbang-dl/graphs/contributors"><img src="https://contrib.rocks/image?repo=YisusChrist/spankbang-dl" /></a>

### How do I contribute to spankbang-dl?

Before you participate in our delightful community, please read the [code of conduct](https://github.com/YisusChrist/.github/blob/main/CODE_OF_CONDUCT.md).

I'm far from being an expert and suspect there are many ways to improve – if you have ideas on how to make the configuration easier to maintain (and faster), don't hesitate to fork and send pull requests!

We also need people to test out pull requests. So take a look through [the open issues](https://github.com/YisusChrist/spankbang-dl/issues) and help where you can.

See [Contributing Guidelines](https://github.com/YisusChrist/.github/blob/main/CONTRIBUTING.md) for more details.

## License

`spankbang-dl` is released under the [GPL-3.0 License](https://opensource.org/license/GPL-3.0).

## Credits

<img src="https://avatars.githubusercontent.com/u/68385729" width="100px;" alt="Green Hat" border-radius="50% !important;" />

This program is a fork of an original project created by [hoppop-web](https://github.com/hoppop-web). I made a few modifications to the original script to fit my needs, which basically are:

- Convert the script into a package, easier to install and use
- Add cloudflare bypass support (#71)
- Resolve video information properly (#73)
- Add support for multiple languages
- Add logging capabilities
- Set the program to always use GUI
- Add some graphic improvements during the download process and fix the progress bar (#75)
