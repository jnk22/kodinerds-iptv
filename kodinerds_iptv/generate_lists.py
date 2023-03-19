"""Module for generating IPTV m3u files based on YAML source files."""

import itertools
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from .enums import ListType
from .line_writer import AutoLineWriter
from .stream import Stream


def generate_stream_lines(
    content: dict[str, Any], list_type: ListType, logo_base_path: str
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
    """
    stream_lines: defaultdict[str, list[str]] = defaultdict(list)
    line_writer = AutoLineWriter.from_list_type(list_type, logo_base_path)
    full_path = f"{list_type.value.lower()}/{list_type.value.lower()}"

    for source_name, source in content.items():
        source_path = f"{full_path}_{source_name}"

        # Iterate over categories: countries for radio, genre for TV
        for category_name, category in source.items():
            all_paths = (full_path, source_path, f"{source_path}_{category_name}")

            for stream, path in itertools.product(category, all_paths):
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
