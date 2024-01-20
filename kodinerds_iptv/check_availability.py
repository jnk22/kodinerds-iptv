"""TODO."""

import functools
from collections.abc import Sequence
from pathlib import Path
from ssl import SSLError

import aiometer
from httpx import URL, AsyncClient, AsyncHTTPTransport, Response, TransportError
from loguru import logger
from tabulate import tabulate

from .enums import StreamState
from .stream import Stream, StreamCheck


async def check_availability(
    streams: Sequence[Stream],
    report_dir: Path,
    *,
    timeout: int,
    max_retries: int,
    max_parallel: int,
) -> None:
    """TODO."""
    transport = AsyncHTTPTransport(retries=max_retries)
    client = AsyncClient(transport=transport, follow_redirects=True, timeout=timeout)
    params = functools.partial(__check_stream, client)

    async with aiometer.amap(params, streams, max_at_once=max_parallel) as results:
        stream_checks = [
            __stream_check_response(stream, response)
            async for stream, response in results
        ]

    __write_results(stream_checks, report_dir / "report.txt")


async def __check_stream(
    client: AsyncClient, stream: Stream
) -> tuple[Stream, Response | Exception | None]:
    logger.debug(f"Checking stream: {stream.name}")
    # TODO: Enable caching for already checked stream URLs.

    if stream.skip_check:
        return stream, None

    try:
        return stream, await client.send(client.build_request("HEAD", stream.url))
    except (TransportError, SSLError) as e:
        return stream, e


def __stream_check_response(
    stream: Stream, response: Response | Exception | None
) -> StreamCheck:
    if response is None:
        # Happens if 'stream.skip_check' is True, therefore no response.
        return StreamCheck(stream, StreamState.SKIPPED)

    if isinstance(response, Exception):
        return StreamCheck(stream, StreamState.ERROR, reason=str(response))

    if response.is_error:
        return StreamCheck(
            stream, StreamState.ERROR, reason=f"HTTP status: {response.status_code}"
        )

    if response.is_redirect:
        return StreamCheck(
            stream, StreamState.WARNING, reason="Redirected to: {response.url}"
        )

    if response.is_success and URL(stream.url).scheme == "http":
        return StreamCheck(
            stream, StreamState.WARNING, reason="Using HTTP instead of HTTPS"
        )

    if response.is_success:
        return StreamCheck(stream, StreamState.SUCCESS)

    # All other cases, including HTTP 1xx status codes.
    return StreamCheck(
        stream,
        StreamState.UNKNOWN,
        reason=f"Unknown (HTTP status: {response.status_code})",
    )


def __write_results(results: Sequence[StreamCheck], output_file: Path) -> None:
    logger.info(f"Writing report file: {output_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(__generate_result_lines(sorted(results)))


def __generate_result_lines(stream_checks: Sequence[StreamCheck]) -> str:
    data = [
        {
            "name": check.stream.name,
            "source": check.stream.source_file,
            "state": check.state.name,
            "reason": check.reason,
        }
        for check in stream_checks
    ]

    return tabulate(data, headers="keys")
