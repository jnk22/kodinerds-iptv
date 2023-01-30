#!/usr/bin/env python3
"""Module for generating IPTV m3u files based on YAML source files."""

import argparse
import collections
import sys
from pathlib import Path
from typing import Any

import yaml
from line_parser import LineParser, ParseType, Stream


def generate_stream_lines(
    content: dict[str, Any],
    list_type: ParseType,
    image_base_path: str,
) -> dict[str, list[str]]:
    """Generate stream lines for all categories based on type.

    Given a dictionary of content and a parse type, this function
    generates a nested dictionary of lists containing parsed lines
    of content.

    Parameters
    ----------
    content : dict[str, Any]
        A dictionary of content to be parsed.
    list_type : ParseType
        The type of parse to be applied to the content.
    image_base_path : str
        Base path for images that 'tvg_logo' will be appended to.

    Returns
    -------
    dict[str, list[str]]: A nested dictionary of lists containing parsed
                          lines of content.

    Examples
    --------
    >>> stream = {"name": "ZDF", "tvg_name": "ZDF", "quality": "sd", "radio": "false", "tvg_id": "zdf.de", "group_title": "IPTV-DE", "group_title_kodi": "Vollprogramm", "tvg_logo": "tv/zdf.png", "url": "https://zdf.m3u8"}
    >>> content = {"tv": {"id": 1, "subcategories": {"main": {"id": 1, "streams": [stream]}}}}
    >>> image_base_path = "https://example.com/logos/"
    >>> list_type = ParseType.CLEAN
    >>> generate_stream_lines(content, list_type, image_base_path)  # doctest: +ELLIPSIS
    defaultdict(<class 'list'>, {'clean/clean': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8'], 'clean/clean_tv': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8'], 'clean/clean_tv_main': ['#EXTINF:-1 tvg-name="ZDF" ..., 'https://zdf.m3u8']})
    """  # noqa: E501
    output_contents = collections.defaultdict(list)
    line_parser = LineParser.from_list_type(list_type)

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
                    lines = line_parser.get_lines(Stream(**stream), image_base_path)
                    output_contents[path].extend(lines)

    return output_contents


def __parse_arguments() -> argparse.Namespace:
    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="YAML source file.")
    parser.add_argument(
        "-d",
        "--destination",
        default="output",
        type=Path,
        help="Output directory",
    )
    parser.add_argument(
        "-e",
        "--extension",
        default="m3u",
        type=str,
        help="Output file extension",
    )
    parser.add_argument(
        "-b",
        "--image_base_path",
        type=str,
        help="Base path for images",
    )

    return parser.parse_args()


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


def __write_output_file(output_file: Path, lines: list[str]) -> None:
    # Write output file with given lines.
    # Each line will be written as a separate line in the file.
    print(f"Writing file: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as file:
        file.write("#EXTM3U\n")
        file.writelines(f"{line}\n" for line in lines)


def main() -> None:
    """Generate IPTV lists based on YAML source file."""
    args = __parse_arguments()
    content = __read_source_file(args.source)

    output_content = {}
    for list_type in ParseType:
        print(f"Generating content for type '{list_type.value}'")
        output_content |= generate_stream_lines(
            content,
            list_type,
            image_base_path=args.image_base_path,
        )

    for file_name_part, lines in output_content.items():
        output_file = Path(f"{args.destination}/{file_name_part}.{args.extension}")
        __write_output_file(output_file, lines)


if __name__ == "__main__":
    main()
