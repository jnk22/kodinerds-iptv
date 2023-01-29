"""Parser module for generating IPTV m3u lines."""

from __future__ import annotations

from enum import Enum
from functools import reduce
from typing import Any


class ParseType(Enum):
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

    CLEAN = "CLEAN"
    KODI = "KODI"
    PIPE = "PIPE"


class LineParser:
    """Default class for parsing lines of stream information.

    This class provides basic functionality for parsing stream
    information and generating a header line and stream line for the
    stream.
    """

    @staticmethod
    def from_list_type(list_type: ParseType) -> LineParser:
        """Return an instance of LineParser class based on parse type.

        Parameters
        ----------
        list_type : ParseType
            The type of parsing to be performed.

        Returns
        -------
        An instance of the appropriate LineParser subclass.
        """
        return next(
            parser() for key, parser in _PARSER_MAPPING.items() if key == list_type
        )

    def get_lines(
        self,
        stream: dict[str, Any],
        image_base_path: str = "",
    ) -> tuple[str, str]:
        """Return a tuple of the header and stream line for the provided stream.

        Parameters
        ----------
        stream : dict[str, Any]
            A dictionary containing information about the stream.
        image_base_path : str
            Base path for images that 'tvg_logo' will be appended to.

        Returns
        -------
        tuple[str, str]: A tuple containing the header line and stream
                         line for the provided stream.

        Examples
        --------
        >>> stream = {"id": 1, "name": "ZDF", "tvg_name": "ZDF", "quality": "sd", "radio": False, "tvg_id": "zdf.de", "group_title": "IPTV-DE", "group_title_kodi": "Vollprogramm", "tvg_logo": "zdf.png", "url": "https://zdf.m3u8"}
        >>> image_base_path = "https://example.com/logos/"
        >>> list_type = ParseType.CLEAN
        >>> LineParser().get_lines(stream, image_base_path)
        ('#EXTINF:-1 tvg-name="ZDF" tvg-id="zdf.de" group-title="IPTV-DE" tvg-logo="https://example.com/logos/zdf.png",ZDF', 'https://zdf.m3u8')
        """  # noqa: E501
        return tuple(
            " ".join(line.split())
            for line in (
                self._header_line(stream, image_base_path),
                self._stream_line(stream),
            )
        )

    def _header_line(self, stream: dict[str, Any], image_base_path: str) -> str:
        # Return header line for stream.
        radio_stream = bool(stream["radio"])

        return f"""
        #EXTINF:-1
        tvg-name="{stream["tvg_name"]}"
        {"" if radio_stream else f'tvg-id="{stream["tvg_id"]}"'}
        group-title="{self._group_title(stream)}"
        {'radio="true"' if radio_stream else ""}
        tvg-logo="{image_base_path}{stream["tvg_logo"]}",{stream["name"]}
        """

    def _stream_line(self, stream: dict[str, Any]) -> str:
        # Return stream line inclurding URL for stream.
        return f"{stream['url']}"

    def _group_title(self, stream: dict[str, Any]) -> str:
        # Return default group title for stream.
        return stream["group_title"]


class KodiLineParser(LineParser):
    """A LineParser subclass for Kodi-specific parsing.

    This class inherits from the LineParser class and overrides certain
    methods to provide Kodi-specific parsing. This includes modifying
    the group title and replacing URLs for YouTube streams to be
    compatible with Kodi's YouTube plugin.
    """

    _YOUTUBE_REPLACE = (
        "https://www.youtube.com/embed/",
        "plugin://plugin.video.youtube/play/?video_id=",
    )

    def _group_title(self, stream: dict[str, Any]) -> str:
        # Override group title with Kodi specific group.
        return stream["group_title_kodi"]

    def _stream_line(self, stream: dict[str, Any]) -> str:
        # Override YouTube streams for usage with Kodi's YouTube plugin.
        return stream["url"].replace(*KodiLineParser._YOUTUBE_REPLACE)


class PipeLineParser(LineParser):
    """A LineParser subclass for parsing lines for use with FFmpeg.

    This class inherits from the LineParser class and overrides certain
    methods to provide parsing that is suitable for use with FFmpeg.
    This includes replacing special characters in the stream url and
    adding codec information to the stream url.
    """

    _REPLACE_CHARS = {
        ("Ä", "Ae"),
        ("ä", "ae"),
        ("Ö", "Oe"),
        ("ö", "oe"),
        ("Ü", "Ue"),
        ("ü", "ue"),
        ("'", "."),
        (" ", "\\ "),
    }

    def _stream_line(self, stream: dict[str, Any]) -> str:
        # Override stream line for pipe usage.
        # The stream URL includes several required attributes for FFmpeg.
        codec_part = "radio" if stream["radio"] else f"{stream['quality']}tv"
        service_name = reduce(
            lambda s, kv: s.replace(*kv),
            PipeLineParser._REPLACE_CHARS,
            stream["name"],
        )

        return f"""
        pipe://ffmpeg
        -loglevel fatal
        -i {stream["url"]}
        -vcodec copy
        -acodec copy
        -metadata service_name={service_name}
        -metadata service_provider={stream["group_title"]}
        -mpegts_service_type advanced_codec_digital_{codec_part}
        -f mpegts
        pipe:1
        """


_PARSER_MAPPING: dict[ParseType, Any] = {
    ParseType.CLEAN: LineParser,
    ParseType.KODI: KodiLineParser,
    ParseType.PIPE: PipeLineParser,
}
