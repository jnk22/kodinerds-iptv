"""Module for generating IPTV m3u files based on YAML source files."""

import itertools
from collections import defaultdict
from pathlib import Path

from .enums import ListType
from .io_utils import read_streams
from .line_writer import AutoLineWriter
from .stream import StreamCategory

EXTM3U_HEADER = "#EXTM3U"


def generate_sources(
    sources: list[Path],
    list_types: list[ListType],
    output_dir: Path,
    output_extension: str,
    logo_base_path: str | None,
) -> None:
    """TODO."""
    source_content: dict[str, list[StreamCategory]] = {}
    for source in sources:
        print(f"Reading source: {source}")
        source_content[source.stem] = read_streams(source)

    stream_lists: dict[str, list[str]] = {}
    for list_type in set(list_types):
        print(f"Generating stream lines for type '{list_type.value}'")
        stream_lists |= generate_stream_lines(source_content, list_type, logo_base_path)

    for file_name, streams in stream_lists.items():
        output_file = Path(f"{output_dir}/{file_name}.{output_extension}")

        print(f"Writing file: {output_file}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join((EXTM3U_HEADER, *streams, "")))

    print("Finished")


def generate_stream_lines(
    content: dict[str, list[StreamCategory]],
    list_type: ListType,
    logo_base_path: str | None,
) -> dict[str, list[str]]:
    """Generate stream lines for all categories based on type.

    Given an input of streams and a list type, this function generates a
    nested dictionary of lists containing final output lines.

    Parameters
    ----------
    content
        A dictionary of stream groups with respective source file name.
    list_type
        The type of required output format.
    logo_base_path
        Base path for images that 'tvg_logo' will be appended to.

    Returns
    -------
    dict[str, list[str]]
        A nested dictionary of lists containing parsed lines of content.
    """
    stream_lines: defaultdict[str, list[str]] = defaultdict(list)
    line_writer = AutoLineWriter.from_list_type(
        list_type, logo_base_path=logo_base_path
    )
    full_path = f"{list_type.value.lower()}/{list_type.value.lower()}"

    for source_name, stream_groups in content.items():
        source_path = f"{full_path}_{source_name}"

        for stream_group in stream_groups:
            category_path = f"{source_path}_{stream_group.name}"
            all_paths = (full_path, source_path, category_path)

            for stream, path in itertools.product(stream_group.streams, all_paths):
                stream_lines[path].extend(line_writer.get_lines(stream))

    return stream_lines
