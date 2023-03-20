"""TODO."""

import asyncio
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from itertools import chain
from pathlib import Path
from typing import Any

from httpx import AsyncClient, AsyncHTTPTransport

from .io_utils import read_streams
from .stream import Stream, StreamCategory


class StreamState(Enum):
    """TODO."""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StreamCheck:
    """TODO."""

    stream: Stream
    state: StreamState
    response: Any = None
    reason: str | None = None

    @property
    def output(self) -> str:
        """TODO."""
        error_line = f" ({self.reason})" if self.reason else ""
        return f"{self.stream.name}: {self.state.value}{error_line}"


def check_wrapper(
    sources: list[Path], report_dir: Path, timeout: int, retries: int
) -> None:
    """TODO."""
    asyncio.run(check_availability(sources, report_dir, timeout, retries))


async def check_availability(
    sources: list[Path], report_dir: Path, timeout: int, retries: int
) -> None:
    """TODO."""
    source_content: dict[str, list[StreamCategory]] = {}
    for source in sources:
        print(f"Reading source: {source}")
        source_content[source.stem] = read_streams(source)

    transport = AsyncHTTPTransport(retries=retries)
    final_results: dict[str, list[StreamCheck]] = {}

    async with AsyncClient(transport=transport) as client:
        for source_name, stream_groups in source_content.items():
            print(f"Checking streams from {source_name}")

            streams = list(chain.from_iterable(sg.streams for sg in stream_groups))
            tasks = [
                skip_check()
                if stream.skip_check
                else client.head(stream.url, timeout=timeout)
                for stream in streams
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            stream_results = zip(streams, results, strict=True)

            stream_checks = []
            for stream, response in stream_results:
                # TODO: Replace with pattern matching

                if response is StreamState.SKIPPED:
                    check = StreamCheck(stream, state=StreamState.SKIPPED)

                elif isinstance(response, Exception):
                    check = StreamCheck(
                        stream, StreamState.FAILED, reason=str(response)
                    )

                elif response.status_code != HTTPStatus.OK:
                    http_error = f"HTTP {response.status_code}"
                    check = StreamCheck(stream, StreamState.FAILED, reason=http_error)

                else:
                    check = StreamCheck(stream, state=StreamState.SUCCESS)

                stream_checks.append(check)

            final_results[source_name] = stream_checks

    for source_name, stream_checks in final_results.items():
        report_file = report_dir / f"{source_name}.txt"
        write_results(stream_checks, report_file)


async def skip_check() -> StreamState:
    """TODO."""
    return StreamState.SKIPPED


def write_results(results: list[StreamCheck], output_file: Path) -> None:
    """TODO."""
    print(f"Writing file: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [result.output for result in results]
    output_file.write_text("\n".join(lines))
