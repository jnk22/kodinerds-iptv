"""Module for generating IPTV m3u files based on YAML source files."""

import itertools
from collections.abc import Sequence
from pathlib import Path

from loguru import logger

from .enums import ListType
from .line_writer import AutoLineWriter
from .stream import Stream


def generate_lists(
    streams: Sequence[Stream],
    list_types: Sequence[ListType],
    output_dir: Path,
    output_extension: str,
    logo_base_path: str,
) -> None:
    """TODO."""
    for list_type in set(list_types):
        line_writer = AutoLineWriter.from_list_type(
            list_type, logo_base_path=logo_base_path
        )

        lines = itertools.chain.from_iterable(
            line_writer.get_lines(stream) for stream in streams
        )

        output_file = Path(f"{output_dir}/{list_type.value}{output_extension}")
        logger.info(f"Writing streams file: {output_file}")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(("#EXTM3U", *lines, "")))
