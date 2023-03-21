"""TODO."""

from dataclasses import dataclass


@dataclass
class Stream:
    """Stores information about a TV or radio stream."""

    name: str
    url: str
    group_title: str
    group_title_kodi: str
    tvg_name: str
    tvg_logo: str
    tvg_id: str | None = None
    quality: str | None = None
    radio: bool = False
    skip_check: bool = False


@dataclass
class StreamCategory:
    """Wrapper for streams in a category."""

    name: str
    streams: list[Stream]
