"""TODO."""

from enum import Enum


class ListType(Enum):
    """Enumeration for different types of stream lists.

    Attributes
    ----------
    CLEAN: Stream uses raw URL.
    KODI:  Stream has full Kodi compatibiliy with extended details.
    PIPE:  Stream is piped through FFmpeg with special header.
    DASH:  Stream has special header to be used with Kodi's adaptive inputstream.
    """

    CLEAN = "clean"
    KODI = "kodi"
    PIPE = "pipe"
    DASH = "dash"


class StreamState(Enum):
    """TODO."""

    SUCCESS = "success"
    WARNING = "warning"
    SKIPPED = "skipped"
    ERROR = "error"
    UNKNOWN = "unknown"
