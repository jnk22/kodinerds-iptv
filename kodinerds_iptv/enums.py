"""TODO."""

from enum import Enum


class ListType(Enum):
    """Enumeration for different types of parsing.

    Attributes
    ----------
        CLEAN: Indicates that the parse should be done with
               no additional processing.
        KODI:  Indicates that the parse should be done in a way that is
               compatible with Kodi.
        PIPE:  Indicates that the parse should be done by piping the
               data through FFmpeg.
    """

    CLEAN = "clean"
    KODI = "kodi"
    PIPE = "pipe"
