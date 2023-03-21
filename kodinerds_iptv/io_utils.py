"""Module for generating IPTV m3u files based on YAML source files."""

import sys
from pathlib import Path
from typing import Any

import yaml

from .stream import Stream, StreamCategory


def read_streams(source_file: Path) -> list[StreamCategory]:
    """TODO."""
    source_content = __yaml_to_dict(source_file)
    return [
        StreamCategory(category_name, [Stream(**stream) for stream in category])
        for category_name, category in source_content.items()
    ]


def __yaml_to_dict(source_file: Path) -> dict[str, Any]:
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
