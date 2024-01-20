"""TODO."""

from enum import Enum, IntEnum


class ListType(Enum):
    """Enumeration for different types of stream lists.

    Attributes
    ----------
    CLEAN: Stream uses raw URL.
    KODI:  Stream has full Kodi compatibiliy with extended details.
    PIPE:  Stream is piped through FFmpeg with special header.
    """

    CLEAN = "clean"
    KODI = "kodi"
    PIPE = "pipe"


class StreamState(IntEnum):
    """TODO."""

    SUCCESS = 1
    WARNING = 2
    SKIPPED = 3
    ERROR = 4
    UNKNOWN = 5


class ReportFormat(Enum):
    """TODO."""

    TEXT = "text"
