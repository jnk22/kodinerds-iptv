"""Command line interface for kodinerds-iptv."""

from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from .cli_helpers import version_callback
from .enums import ListType

StrOrNone = Optional[str]


CLI_SOURCES = Argument(..., exists=True, help="YAML source files.")
CLI_VERSION = Option(None, "--version", callback=version_callback, is_eager=True)

DEFAULT_LIST_TYPES = [lt.value for lt in {ListType.CLEAN, ListType.KODI, ListType.PIPE}]

app = Typer()


@app.callback()
def callback(*, value: bool = CLI_VERSION) -> None:  # noqa: ARG001
    """Kodinerds IPTV CLI application."""


@app.command("check")
def check(
    sources: list[Path] = CLI_SOURCES,
    *,
    output_dir: Path = Option("reports", writable=True, help="Reports directory."),
    timeout: int = Option(1, help="Timeout for stream check."),
    retries: int = Option(1, help="Retries for failed stream check."),
) -> None:
    """Check stream URLs on availability."""
    # TODO: Check for duplicates in sources.
    from .check_availability import check_sources

    check_sources(sources, output_dir, timeout, retries)


@app.command()
def generate(
    sources: list[Path] = CLI_SOURCES,
    *,
    list_types: list[ListType] = Option(DEFAULT_LIST_TYPES, help="List types."),
    output_dir: Path = Option("output", writable=True, help="Output directory."),
    output_extension: str = Option("m3u", help="Output file extension."),
    logo_base_path: StrOrNone = Option(
        None, help="Prepended base path for channel logos."
    ),
) -> None:
    """Generate IPTV lists based on YAML source file."""
    # TODO: Check for duplicates in sources.
    from .generate_lists import generate_sources

    generate_sources(sources, list_types, output_dir, output_extension, logo_base_path)
