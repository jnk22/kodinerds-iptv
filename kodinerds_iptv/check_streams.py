#!/usr/bin/env python3
"""TODO."""

import argparse
import collections
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from pathlib import Path
from typing import Any

import trio
import yaml
from httpx import AsyncClient, ConnectError, ReadTimeout

from .stream import Stream


@dataclass
class StreamCheck:
    """TODO."""

    stream: Stream
    retries: int = 0


class TestResult(Enum):
    """TODO."""

    AVAILABLE, UNAVAILABLE, UNKNOWN, SKIPPED, ERROR = range(5)


def get_streams(content: dict[str, Any]) -> list[Stream]:
    """TODO.

    TODO.

    Parameters
    ----------
    TODO.

    Returns
    -------
    TODO.

    Examples
    --------
    TODO.
    """
    streams = []
    categories = dict(sorted(content.items(), key=lambda x: x[1]["id"]))

    # Iterate over main categories, i.e. TV and radio
    for category in categories.values():
        subcategories = dict(
            sorted(category["subcategories"].items(), key=lambda x: x[1]["id"]),
        )

        # Iterate over subcategories: countries for radio, genre for TV
        for subcategory in subcategories.values():
            streams.extend(Stream(**stream) for stream in subcategory["streams"])

    return streams


async def test_streams(
    streams: list[Stream], max_retries: int = 5, timeout: int = 10
) -> dict[TestResult, list[Stream]]:
    """TODO.

    TODO.

    Parameters
    ----------
    TODO.

    Returns
    -------
    TODO.

    Examples
    --------
    TODO.
    """
    stream_queue = collections.deque(StreamCheck(stream) for stream in streams)

    print(max_retries)
    print(timeout)

    results = collections.defaultdict(list)
    while stream_queue:
        check = stream_queue.popleft()
        async with AsyncClient(timeout=timeout) as client:
            print(
                f"Testing ({check.retries}): {check.stream.name} ({check.stream.url})"
            )
            try:
                response = await client.get(check.stream.url)

            except ConnectError:
                logging.exception("Connection error")
                results[TestResult.ERROR].append(check.stream)
                continue
            except ReadTimeout:
                logging.exception("Timeout error")
                results[TestResult.ERROR].append(check.stream)
                continue
            except Exception:
                logging.exception("Unknown error")
                results[TestResult.ERROR].append(check.stream)
                continue

            if response.status_code == HTTPStatus.OK:
                logging.info("Success")
                results[TestResult.AVAILABLE].append(check.stream)
            else:
                logging.info("Failure. Trying again")
                if check.retries < max_retries:
                    check.retries += 1
                    stream_queue.append(check)

    return results


def __parse_arguments() -> argparse.Namespace:
    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="YAML source file.")
    parser.add_argument(
        "-d",
        "--destination",
        default="results.txt",
        type=Path,
        help="Output path for results",
    )
    parser.add_argument(
        "-r",
        "--max_retries",
        type=int,
        default=5,
        help="Maximum retries for each stream",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=10,
        help="Timeout for each stream request",
    )

    return parser.parse_args()


def __read_source_file(source_file: Path) -> dict[str, Any]:
    # Read YAML source file.
    print(f"Reading source: {source_file}")
    try:
        with source_file.open("r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Source file does not exist: {source_file}")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error while parsing YAML file: {exc}")
        sys.exit(1)


async def main() -> None:
    """Generate IPTV lists based on YAML source file."""
    args = __parse_arguments()
    streams = get_streams(__read_source_file(args.source))
    results = await test_streams(
        streams, max_retries=args.max_retries, timeout=args.timeout
    )
    print(results)


if __name__ == "__main__":
    trio.run(main)
