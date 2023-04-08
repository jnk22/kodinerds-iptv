"""TODO."""

import asyncio
from collections import defaultdict
from collections.abc import Coroutine
from http import HTTPStatus
from itertools import chain
from pathlib import Path
from typing import Any, Protocol

from httpx import AsyncClient, AsyncHTTPTransport, Response
from tabulate import tabulate

from .enums import ReportFormat, StreamState
from .io_utils import read_streams
from .stream import Stream, StreamCategory, StreamCheck


class ReportOutput(Protocol):
    """TODO."""

    def write_header(self, state: StreamState) -> str:
        """TODO."""
        ...

    def write_table(self, stream_checks: list[StreamCheck]) -> str:
        """TODO."""
        ...


def check_sources(
    sources: list[Path],
    output_dir: Path,
    timeout: int,
    retries: int,
    report_format: ReportFormat,
) -> None:
    """TODO."""
    asyncio.run(
        check_availability(sources, output_dir, timeout, retries, report_format)
    )


async def check_availability(
    sources: list[Path],
    report_dir: Path,
    timeout: int,
    retries: int,
    report_format: ReportFormat,
) -> None:
    """TODO."""
    source_content: dict[str, list[StreamCategory]] = {}
    for source in sources:
        print(f"Reading source: {source}")
        source_content[source.stem] = read_streams(source)

    transport = AsyncHTTPTransport(retries=retries)
    results: dict[str, list[StreamCheck]] = {}

    async with AsyncClient(transport=transport) as client:
        for source_name, stream_groups in source_content.items():
            print(f"Checking streams from source '{source_name}'")

            streams = list(chain.from_iterable(sg.streams for sg in stream_groups))
            tasks = [await check(stream, client, timeout) for stream in streams]
            gather_results = await asyncio.gather(*tasks, return_exceptions=True)

            results[source_name] = [
                match_stream_check_response(*stream_result)
                for stream_result in zip(streams, gather_results, strict=True)
            ]

    file_extension = "md" if report_format == ReportFormat.MARKDOWN else "txt"
    for source_name, stream_checks in results.items():
        report_file = report_dir / f"{source_name}.{file_extension}"
        write_results(stream_checks, report_file)

    print("Finished")


def match_stream_check_response(
    stream: Stream, response: Response | Exception | None
) -> StreamCheck:
    """TODO."""
    match response:
        case None:
            return StreamCheck(stream, StreamState.SKIPPED)

        case Exception() as e:
            return StreamCheck(stream, StreamState.ERROR, reason=str(e))

        case _:
            # TODO: Check for redirects.
            # TODO: Match against more status codes explicitly.
            status = response.status_code
            check = (
                StreamCheck(stream, StreamState.SUCCESS)
                if status == HTTPStatus.OK
                else StreamCheck(stream, StreamState.ERROR, reason=f"HTTP: {status}")
            )

            if check.state == StreamState.SUCCESS and stream.url.startswith("http://"):
                # Stream URL is HTTP, but it works.
                check.state = StreamState.WARNING
                check.reason = "Try using https:// instead of http://"

            return check


async def check(
    stream: Stream, client: AsyncClient, timeout: int
) -> Coroutine[Any, Any, Response | None]:
    """TODO."""
    return noop() if stream.skip_check else client.head(stream.url, timeout=timeout)


async def noop() -> None:
    """No-op function."""


def write_results(results: list[StreamCheck], output_file: Path) -> None:
    """TODO."""
    print(f"Writing file: {output_file}")
    sorted_results: defaultdict[StreamState, list[StreamCheck]] = defaultdict(list)
    for result in results:
        sorted_results[result.state].append(result)

    final_result: str = "\n\n".join(
        f"{'='*29} Results for: {state} {'='*29}\n{result_lines(sorted_results[state])}"
        for state in StreamState
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(final_result)


def result_lines(results: list[StreamCheck]) -> str:
    """TODO."""
    return (
        tabulate(
            [
                {
                    "name": res.stream.name,
                    "state": res.state.value,
                    "reason": res.reason,
                }
                for res in results
            ],
            headers="keys",
            tablefmt="github",
        )
        if results
        else "Nothing here..."
    )
