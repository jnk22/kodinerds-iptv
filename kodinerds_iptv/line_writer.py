"""Writer module for generating IPTV stream lines."""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import TYPE_CHECKING, Any

from .enums import ListType

if TYPE_CHECKING:
    from .stream import Stream


@dataclass
class LineWriter:
    """Default class for creating lines of stream information.

    This class provides basic functionality for creating stream
    information output, including a header line and stream line.
    """

    logo_base_path: str = ""

    def get_lines(self, stream: Stream) -> tuple[str, str]:
        """Return a tuple of the header and stream line for the provided stream.

        Parameters
        ----------
        stream
            Stream object containing information about the stream.

        Returns
        -------
        tuple[str, str]
            A tuple containing the header line and stream line for the provided stream.

        Examples
        --------
        Generate lines for a single stream:

        >>> from .stream import Stream
        >>> line_writer = AutoLineWriter.from_list_type(ListType.CLEAN, "https://example.com/logos/")
        >>> stream = Stream(name="ZDF", tvg_name="ZDF", quality="sd", radio=False, tvg_id="zdf.de", group_title="IPTV-DE", group_title_kodi="Vollprogramm", tvg_logo="zdf.png", url="https://zdf.m3u8")
        >>> line_writer.get_lines(stream)
        ('#EXTINF:-1 tvg-name="ZDF" tvg-id="zdf.de" group-title="IPTV-DE" tvg-logo="https://example.com/logos/zdf.png",ZDF', 'https://zdf.m3u8')
        """  # noqa: E501
        lines = (self._header_line(stream), self._stream_line(stream))
        header_line, stream_line = (" ".join(line.split()) for line in lines)

        return header_line, stream_line

    def _header_line(self, stream: Stream) -> str:
        # Return header line for stream.
        return f"""
        #EXTINF:-1
        tvg-name="{stream.tvg_name}"
        {"" if stream.radio else f'tvg-id="{stream.tvg_id}"'}
        group-title="{self._group_title(stream)}"
        {'radio="true"' if stream.radio else ""}
        tvg-logo="{self.logo_base_path}{stream.tvg_logo}",{stream.name}
        """

    def _stream_line(self, stream: Stream) -> str:
        # Return stream line inclurding URL for stream.
        return f"{stream.url}"

    def _group_title(self, stream: Stream) -> str:
        # Return default group title for stream.
        return stream.group_title


class KodiLineWrite(LineWriter):
    """A LineWrite subclass for Kodi-specific stream lines.

    This class inherits from the LineWriter class and overrides certain
    methods to provide Kodi-specific stream lines. This includes
    modifying the group title and replacing URLs for YouTube streams to
    be compatible with Kodi's YouTube plugin.
    """

    _YOUTUBE_REPLACE = (
        "https://www.youtube.com/embed/",
        "plugin://plugin.video.youtube/play/?video_id=",
    )

    def _stream_line(self, stream: Stream) -> str:
        # Override YouTube streams for usage with Kodi's YouTube plugin.
        return stream.url.replace(*self._YOUTUBE_REPLACE)

    def _group_title(self, stream: Stream) -> str:
        # Override group title with Kodi specific group.
        return stream.group_title_kodi


class PipeLineWriter(LineWriter):
    """A LineWrite subclass for writing lines for use with FFmpeg.

    This class inherits from the LineWriter class and overrides certain
    methods to provide stream lines that can be used in Tvheadend where
    piping streams through FFmpeg is required. Modifications include
    replacing special characters and adding codec information to the
    stream URL.
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

    def _stream_line(self, stream: Stream) -> str:
        # Override stream line for pipe usage.
        # The stream URL includes several required attributes for FFmpeg.
        codec_part = "radio" if stream.radio else f"{stream.quality}tv"
        service_name = reduce(
            lambda s, kv: s.replace(*kv), self._REPLACE_CHARS, stream.name
        )

        return f"""
        pipe://ffmpeg
        -loglevel fatal
        -i {stream.url}
        -vcodec copy
        -acodec copy
        -metadata service_name={service_name}
        -metadata service_provider={stream.group_title}
        -mpegts_service_type advanced_codec_digital_{codec_part}
        -f mpegts
        pipe:1
        """


class AutoLineWriter:
    """TODO."""

    __MAPPING: dict[ListType, Any] = {
        ListType.CLEAN: LineWriter,
        ListType.KODI: KodiLineWrite,
        ListType.PIPE: PipeLineWriter,
    }

    @classmethod
    def from_list_type(cls, list_type: ListType, logo_base_path: str) -> LineWriter:
        """Return an instance of LineWriter class based on list type.

        Parameters
        ----------
        list_type
            The type of list that is required.

        Returns
        -------
        LineWriter
            An instance of the appropriate LineWriter.
        """
        return next(
            writer_class(logo_base_path)
            for lt_key, writer_class in cls.__MAPPING.items()
            if lt_key == list_type
        )
