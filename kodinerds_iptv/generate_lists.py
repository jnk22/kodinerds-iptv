#!/usr/bin/env python3
"""Module for generating IPTV m3u files based on YAML source files."""

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml
from typer import Argument, Option, Typer

from .enums import ListType
from .line_parser import AutoLineParser
from .stream import Stream

ALL_LIST_TYPES = [list_type.value for list_type in ListType]

app = Typer()


def __generate_stream_lines(
    content: dict[str, Any],
    list_type: ListType,
    logo_base_path: str,
) -> dict[str, list[str]]:
    """Generate stream lines for all categories based on type.

    Given a dictionary of content and a parse type, this function
    generates a nested dictionary of lists containing parsed lines
    of content.

    Parameters
    ----------
    content
        A dictionary of content to be parsed.
    list_type
        The type of parse to be applied to the content.
    image_base_path
        Base path for images that 'tvg_logo' will be appended to.

    Returns
    -------
    dict[str, list[str]]
        A nested dictionary of lists containing parsed lines of content.

    Examples
    --------
    Generate lines for a single stream with the 'clean' parse type:

    >>> stream = {"name": "ZDF", "tvg_name": "ZDF", "quality": "sd", "radio": "false", "tvg_id": "zdf.de", "group_title": "IPTV-DE", "group_title_kodi": "Vollprogramm", "tvg_logo": "tv/zdf.png", "url": "https://zdf.m3u8"}
    >>> content = {"tv": {"id": 1, "subcategories": {"main": {"id": 1, "streams": [stream]}}}}
    >>> __generate_stream_lines(content, ListType.CLEAN, "https://example.com/logos/")  # doctest: +ELLIPSIS
    defaultdict(<class 'list'>, {'clean/clean': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8'], 'clean/clean_tv': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8'], 'clean/clean_tv_main': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8']})
    """  # noqa: E501
    output_contents: defaultdict[str, list[str]] = defaultdict(list)
    line_parser = AutoLineParser.from_list_type(list_type, logo_base_path)

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
                    stream_lines = line_parser.get_lines(Stream(**stream))
                    output_contents[path].extend(stream_lines)

    return output_contents


def __read_source_file(source_file: Path) -> dict[str, Any]:
    # Read YAML source file.
    print(f"Reading source: {source_file}")

    try:
        with source_file.open("r") as file:
            return yaml.safe_load(file)

    except FileNotFoundError:
        print(f"Source file does not exist: {source_file}")
        sys.exit(1)

    except yaml.YAMLError as exc:
        print(f"Error while parsing YAML file: {exc}")
        sys.exit(1)


def __write_streams(lines: list[str], output_file: Path) -> None:
    # Write output file with given lines.
    # Each line will be written as a separate line in the file.
    print(f"Writing file: {output_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(("#EXTM3U", *lines, "")))


@app.command()
def main(
    source: Path = Argument(..., exists=True, help="YAML source file."),
    list_type: list[ListType] = Option(ALL_LIST_TYPES, help="List type(s)."),
    output_path: Path = Option("output", writable=True, help="Output directory."),
    output_extension: str = Option("m3u", help="Output file extension."),
    logo_base_path: str = Option("", help="Prepended base path for channel logos."),
) -> None:
    """Generate IPTV lists based on YAML source file."""
    yaml_content = __read_source_file(source)

    stream_lists: dict[str, list[str]] = {}
    for lt in set(list_type):
        print(f"Generating content for type '{lt.value}'")
        stream_lists |= __generate_stream_lines(yaml_content, lt, logo_base_path)

    for file_name, streams in stream_lists.items():
        __write_streams(streams, Path(f"{output_path}/{file_name}.{output_extension}"))

    print("Finished")
