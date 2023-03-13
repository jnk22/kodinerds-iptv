"""TODO."""

from dataclasses import dataclass


@dataclass
class Stream:
    """Stores information about a TV or radio stream."""

    name: str
    group_title: str
    group_title_kodi: str
    quality: str
    radio: bool
    tvg_id: str
    tvg_name: str
    tvg_logo: str
    url: str
