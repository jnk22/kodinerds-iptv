"""TODO."""

from enum import Enum


class ListType(Enum):
    """Enumeration for different types of stream lists.

    Attributes
    ----------
    CLEAN: Indicates that list should use raw stream URL.
    KODI:  Indicates that list should be compatible with Kodi.
    PIPE:  Indicates that stream should be piped through FFmpeg with special header.
    """

    CLEAN = "clean"
    KODI = "kodi"
    PIPE = "pipe"
