"""Command line interface for kodinerds-iptv."""

from pathlib import Path
from typing import Annotated, Final, Optional

from typer import Argument, Option, Typer

from .cli_helpers import version_callback
from .enums import ListType, ReportFormat
from .io_utils import read_stream_sources

# Workaround for Typer not support '|' for Union types:
# GitHub issue: https://github.com/tiangolo/typer/issues/533
OptionalStr = Optional[str]  # noqa: UP007
OptionalBool = Optional[bool]  # noqa: UP007

HELP_VERSION = "Show version and exit."
HELP_SOURCES = "YAML source files."
HELP_LIST_TYPES = "List types."
HELP_OUTPUT_DIR = "Output directory."
HELP_OUTPUT_EXTENSION = "Output file extension."
HELP_LOGO_BASE_PATH = "Prepended base path for channel logos."
HELP_TIMEOUT = "Timeout for stream availability check."
HELP_MAX_RETRIES = "Maximum retries for failed stream check."
HELP_MAX_PARALLEL = "Maximum parallel connections from client."
HELP_REPORT_FORMAT = "Format for report output."
HELP_REPORTS_DIR = "Reports directory."

Version = Annotated[
    OptionalBool,
    Option(
        "--version",
        callback=version_callback,
        is_eager=True,
        show_default=False,
        help=HELP_VERSION,
    ),
]
Sources = Annotated[list[Path], Argument(exists=True, help=HELP_SOURCES)]
CheckReportsOutputDir = Annotated[
    Path, Option(writable=True, dir_okay=True, help=HELP_REPORTS_DIR)
]
CheckTimeout = Annotated[int, Option(help=HELP_TIMEOUT)]
CheckMaxRetries = Annotated[int, Option(help=HELP_MAX_RETRIES)]
CheckMaxParallel = Annotated[int, Option(help=HELP_MAX_PARALLEL)]
CheckReportFormat = Annotated[
    ReportFormat, Option(help=HELP_REPORT_FORMAT, hidden=True)
]
GenerateListTypes = Annotated[list[ListType], Option(help=HELP_LIST_TYPES)]
GenerateOutputDir = Annotated[Path, Option(help=HELP_OUTPUT_DIR)]
GenerateOutputExtension = Annotated[str, Option(help=HELP_OUTPUT_EXTENSION)]
GenerateLogoBasePath = Annotated[str, Option(help=HELP_LOGO_BASE_PATH)]

DEFAULT_LIST_TYPES: Final[list[str]] = [
    ListType.CLEAN.value,
    ListType.KODI.value,
    ListType.PIPE.value,
]

app = Typer()


@app.command()
def generate(
    sources: Sources,
    *,
    list_types: GenerateListTypes = DEFAULT_LIST_TYPES,  # pyright: ignore [reportGeneralTypeIssues]
    output_dir: GenerateOutputDir = Path("output"),
    output_extension: GenerateOutputExtension = ".m3u",
    logo_base_path: GenerateLogoBasePath = "",
) -> None:
    """Generate IPTV lists based on YAML source file."""
    # TODO: Allow output file(s) name to be configured.
    # TODO: Allow custom filtering, sorting, and grouping.
    # TODO: Log total duration.
    # TODO: Filter duplicates.
    from .generate_lists import generate_lists

    generate_lists(
        read_stream_sources(*sources),
        list_types,
        output_dir,
        output_extension,
        logo_base_path,
    )


@app.command("check")
def check(
    sources: Sources,
    *,
    output_dir: CheckReportsOutputDir = Path("reports"),
    timeout: CheckTimeout = 10,
    max_retries: CheckMaxRetries = 3,
    max_parallel: int = 10,
    _report_format: CheckReportFormat = ReportFormat.TEXT.value,  # pyright: ignore [reportGeneralTypeIssues]
) -> None:
    """Check stream URLs on availability."""
    # TODO: Allow output file(s) name to be configured.
    # TODO: Allow custom filtering, sorting, and grouping.
    # TODO: Allow custom output format (e.g. JSON, HTML, CSV, Markdown, ...).
    # TODO: Log total duration.
    # TODO: Filter duplicates.
    import asyncio

    from .check_availability import check_availability

    asyncio.run(
        check_availability(
            read_stream_sources(*sources),
            output_dir,
            timeout=timeout,
            max_retries=max_retries,
            max_parallel=max_parallel,
        )
    )


@app.callback()
def callback(*, _version: Version = None) -> None:
    """Kodinerds IPTV CLI application."""
