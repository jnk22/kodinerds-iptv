"""TODO."""

import functools
from dataclasses import KW_ONLY, dataclass, field
from pathlib import Path

from .enums import StreamState


@dataclass(frozen=True, slots=True)
class Stream:
    """Stores information about a TV or radio stream."""

    name: str
    url: str  # TODO: Integrate various URL types: IPTV/M3U8, YouTube, RTMP, DASH, ...
    category: str | None = None
    tvg_name: str | None = None
    tvg_logo: str | None = None  # TODO: Allow absolute URLs.
    group_title: str | None = None
    group_titles_kodi: list[str] = field(default_factory=list)
    tvg_id: str | None = None
    quality: str | None = None
    radio: bool = False
    skip_check: bool = False
    origin: str | None = None
    source_file: Path | None = None


@dataclass(frozen=True, slots=True)
class StreamCategory:
    """Wrapper for streams in a category."""

    name: str
    streams: list[Stream]


@dataclass(slots=True)
@functools.total_ordering
class StreamCheck:
    """TODO."""

    stream: Stream
    state: StreamState
    _: KW_ONLY
    reason: str | None = None

    @property
    def output(self) -> str:
        """TODO."""
        error_line = f" ({self.reason})" if self.reason else ""
        return f"{self.stream.name}: {self.state.value}{error_line}"

    def __eq__(self, other: object) -> bool:
        """TODO."""
        if not isinstance(other, StreamCheck):
            return NotImplemented

        return self.state == other.state

    def __lt__(self, other: object) -> bool:
        """TODO."""
        if not isinstance(other, StreamCheck):
            return NotImplemented

        return self.state < other.state
