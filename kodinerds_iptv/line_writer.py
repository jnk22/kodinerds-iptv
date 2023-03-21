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

    logo_base_path: str | None = None

    def get_lines(self, stream: Stream) -> list[str]:
        """Return a tuple of the header and stream line for the provided stream.

        Parameters
        ----------
        stream
            Stream object containing information about the stream.

        Returns
        -------
        tuple[str, str]
            A tuple containing the header line and stream line for the provided stream.
        """
        lines = (*self._header_line(stream), self._stream_line(stream))
        return [" ".join(line.split()) for line in lines]

    def _header_line(self, stream: Stream) -> list[str]:
        # Return header line for stream.
        raw_lines = (
            "#EXTINF:-1",
            f'tvg-name="{stream.tvg_name}"',
            None if stream.radio else f'tvg-id="{stream.tvg_id}"',
            f'group-title="{self._group_title(stream)}"',
            'radio="true"' if stream.radio else None,
            (
                f'tvg-logo="{self.logo_base_path}{stream.tvg_logo}"'
                if self.logo_base_path
                else None
            ),
        )

        lines = " ".join(line for line in raw_lines if line)

        return [f"{lines},{stream.name}"]

    def _stream_line(self, stream: Stream) -> str:
        # Return stream line inclurding URL for stream.
        return f"{stream.url}"

    def _group_title(self, stream: Stream) -> str:
        # Return default group title for stream.
        return stream.group_title


class KodiLineWriter(LineWriter):
    """A LineWriter subclass for Kodi-specific stream lines.

    This class inherits from the LineWriter class and overrides certain
    methods to provide Kodi-specific stream lines. This includes
    modifying the group title and replacing URLs for YouTube streams to
    be compatible with Kodi's YouTube plugin.
    """

    __YOUTUBE_URL_REPLACE = (
        "https://www.youtube.com/embed/",
        "plugin://plugin.video.youtube/play/?video_id=",
    )

    def _stream_line(self, stream: Stream) -> str:
        # Override YouTube streams for usage with Kodi's YouTube plugin.
        return stream.url.replace(*self.__YOUTUBE_URL_REPLACE)

    def _group_title(self, stream: Stream) -> str:
        # Override group title with Kodi specific group.
        return stream.group_title_kodi


class PipeLineWriter(LineWriter):
    """A LineWriter subclass for writing lines for use with FFmpeg.

    This class inherits from the LineWriter class and overrides certain
    methods to provide stream lines that can be used in Tvheadend where
    piping streams through FFmpeg is required. Modifications include
    replacing special characters and adding codec information to the
    stream URL.
    """

    __REPLACE_ENCODING_CHARS = {
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
            lambda s, kv: s.replace(*kv), self.__REPLACE_ENCODING_CHARS, stream.name
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


class DashLineWriter(LineWriter):
    """A LineWriter subclass for writing Dash/MPD streams.

    TODO
    """  # TODO

    __KODI_PROPS = [
        "#KODIPROP:inputstreamaddon=inputstream.adaptive",
        "#KODIPROP:inputstream.adaptive.manifest_type=mpd",
    ]

    def _header_line(self, stream: Stream) -> list[str]:
        # Override stream line for pipe usage.
        # The stream URL includes several required attributes for FFmpeg.
        return [*super()._header_line(stream), *self.__KODI_PROPS]

    def _group_title(self, stream: Stream) -> str:
        # Override group title with Kodi specific group.
        return stream.group_title_kodi


class AutoLineWriter:
    """TODO."""

    __MAPPING: dict[ListType, Any] = {
        ListType.CLEAN: LineWriter,
        ListType.KODI: KodiLineWriter,
        ListType.PIPE: PipeLineWriter,
        ListType.DASH: DashLineWriter,
    }

    @classmethod
    def from_list_type(cls, list_type: ListType, **kwargs: str | None) -> LineWriter:
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
            writer_class(**kwargs)
            for lt_key, writer_class in cls.__MAPPING.items()
            if lt_key == list_type
        )
