"""Module for generating IPTV m3u files based on YAML source files."""

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from .enums import ListType
from .line_writer import AutoLineWriter
from .stream import Stream


def generate_stream_lines(
    content: dict[str, Any],
    list_type: ListType,
    logo_base_path: str,
) -> dict[str, list[str]]:
    """Generate stream lines for all categories based on type.

    Given a dictionary of content and a list type, this function
    generates a nested dictionary of lists containing parsed lines
    of content.

    Parameters
    ----------
    content
        A dictionary of content to be parsed.
    list_type
        The type of required output format.
    image_base_path
        Base path for images that 'tvg_logo' will be appended to.

    Returns
    -------
    dict[str, list[str]]
        A nested dictionary of lists containing parsed lines of content.

    Examples
    --------
    Generate lines for a single stream with the 'clean' list type:

    >>> stream = {"name": "ZDF", "tvg_name": "ZDF", "quality": "sd", "radio": "false", "tvg_id": "zdf.de", "group_title": "IPTV-DE", "group_title_kodi": "Vollprogramm", "tvg_logo": "tv/zdf.png", "url": "https://zdf.m3u8"}
    >>> content = {"tv": {"id": 1, "subcategories": {"main": {"id": 1, "streams": [stream]}}}}
    >>> generate_stream_lines(content, ListType.CLEAN, "https://example.com/logos/")  # doctest: +ELLIPSIS
    defaultdict(<class 'list'>, {'clean/clean': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8'], 'clean/clean_tv': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8'], 'clean/clean_tv_main': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8']})
    """  # noqa: E501
    stream_lines: defaultdict[str, list[str]] = defaultdict(list)
    line_writer = AutoLineWriter.from_list_type(list_type, logo_base_path)

    categories = dict(sorted(content.items(), key=lambda x: x[1]["id"]))
    all_path = f"{list_type.value.lower()}/{list_type.value.lower()}"

    # Iterate over main categories, i.e. TV and radio
    for category_name, category in categories.items():
        subcategories = dict(
            sorted(category["subcategories"].items(), key=lambda x: x[1]["id"]),
        )
        category_path = f"{all_path}_{category_name}"

        # Iterate over subcategories: countries for radio, genre for TV
        for subcategory_name, subcategory in subcategories.items():
            subcategory_path = f"{category_path}_{subcategory_name}"

            for stream in subcategory["streams"]:
                for path in [all_path, category_path, subcategory_path]:
                    stream_lines[path].extend(line_writer.get_lines(Stream(**stream)))

    return stream_lines


def read_source_file(source_file: Path) -> dict[str, Any]:
    """TODO."""
    try:
        with source_file.open("r") as file:
            return yaml.safe_load(file)

    except FileNotFoundError:
        print(f"Source file does not exist: {source_file}")
        sys.exit(1)

    except yaml.YAMLError as exc:
        print(f"Error while parsing YAML file: {exc}")
        sys.exit(1)
