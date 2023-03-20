"""Command line interface for kodinerds-iptv."""

from pathlib import Path

from typer import Argument, Option, Typer

from .check_availability import check_wrapper
from .enums import ListType
from .generate_lists import generate_wrapper

DEFAULT_LIST_TYPES = [lt.value for lt in {ListType.CLEAN, ListType.KODI, ListType.PIPE}]

app = Typer()


@app.command()
def check(
    sources: list[Path] = Argument(..., exists=True, help="YAML source file."),
    report_dir: Path = Option("reports", writable=True, help="Reports directory."),
    timeout: int = Option(1, help="Timeout for single stream checks."),
    retries: int = Option(1, help="Retries for failed stream checks."),
) -> None:
    """Check stream URLs on availability."""
    check_wrapper(sources, report_dir, timeout, retries)


@app.command()
def generate(
    sources: list[Path] = Argument(..., exists=True, help="YAML source file."),
    list_type: list[ListType] = Option(DEFAULT_LIST_TYPES, help="List type(s)."),
    output_dir: Path = Option("output", writable=True, help="Output directory."),
    output_extension: str = Option("m3u", help="Output file extension."),
    logo_base_path: str = Option("", help="Prepended base path for channel logos."),
) -> None:
    """Generate IPTV lists based on YAML source file."""
    generate_wrapper(sources, list_type, output_dir, output_extension, logo_base_path)
