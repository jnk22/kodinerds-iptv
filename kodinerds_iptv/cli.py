#!/usr/bin/env python3
"""Command line interface for kodinerds-iptv."""

from pathlib import Path
from types import NotImplementedType
from typing import Any

from typer import Argument, Option, Typer

from .enums import ListType
from .generate_lists import generate_stream_lines, read_source_file

ALL_LIST_TYPES = [list_type.value for list_type in ListType]

app = Typer()


@app.command()
def check(
    source: Path = Argument(..., exists=True, help="YAML source file."),
    report_file: Path = Option("report.txt", writable=True, help="Report file."),
) -> NotImplementedType:
    """Check stream URLs on availability."""
    print(f"Source: {source}")
    print(f"Report file: {report_file}")
    print("!!! Not implemented yet !!!")

    return NotImplemented


@app.command()
def generate(
    sources: list[Path] = Argument(..., exists=True, help="YAML source file."),
    list_type: list[ListType] = Option(ALL_LIST_TYPES, help="List type(s)."),
    output_dir: Path = Option("output", writable=True, help="Output directory."),
    output_extension: str = Option("m3u", help="Output file extension."),
    logo_base_path: str = Option("", help="Prepended base path for channel logos."),
) -> None:
    """Generate IPTV lists based on YAML source file."""
    source_content: dict[str, Any] = {}
    for source in sources:
        print(f"Reading source: {source}")
        source_content[source.stem] = read_source_file(source)

    stream_lists: dict[str, list[str]] = {}
    for lt in set(list_type):
        print(f"Generating stream lines for type '{lt.value}'")
        stream_lists |= generate_stream_lines(source_content, lt, logo_base_path)

    for file_name, streams in stream_lists.items():
        output_file = Path(f"{output_dir}/{file_name}.{output_extension}")

        print(f"Writing file: {output_file}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(("#EXTM3U", *streams, "")))

    print("Finished")
