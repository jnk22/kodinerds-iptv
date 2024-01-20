"""Module for generating IPTV m3u files based on YAML source files."""

import itertools
import sys
from pathlib import Path
from typing import Any

import yaml
from loguru import logger

from .stream import Stream


def read_stream_sources(*source_files: Path) -> list[Stream]:
    """TODO."""
    logger.debug("Starting to read all source files")

    stream_reads = (__read_streams(source_file) for source_file in source_files)
    return list(itertools.chain.from_iterable(stream_reads))


def __read_streams(source_file: Path) -> list[Stream]:
    logger.info(f"Reading source file: {source_file}")

    yaml_content = __yaml_to_dict(source_file)
    return [Stream(**stream, source_file=source_file) for stream in yaml_content]


def __yaml_to_dict(source_file: Path) -> list[dict[str, Any]]:
    try:
        with source_file.open("r") as file:
            return yaml.safe_load(file)

    except FileNotFoundError:
        logger.error(f"Source file does not exist: {source_file}")
        sys.exit(1)

    except yaml.YAMLError as exc:
        logger.error(f"Error while parsing YAML file: {exc}")
        sys.exit(1)
