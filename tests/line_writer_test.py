"""Unit tests for the `LineWriter` module."""

import pytest

from kodinerds_iptv import AutoLineWriter, LineWriter, ListType, Stream


@pytest.fixture()
def line_writer(list_type: ListType) -> LineWriter:
    """TODO."""
    return AutoLineWriter.from_list_type(
        list_type, logo_base_path="https://example.com/logos/"
    )


@pytest.fixture()
def m3u8_streams() -> list[Stream]:
    """TODO."""
    return [
        Stream(
            name="Das Erste HD",
            tvg_name="Das Erste HD",
            quality="hd",
            radio=False,
            tvg_id="daserste.de",
            group_title="IPTV-DE",
            group_title_kodi="Vollprogramm",
            tvg_logo="tv/daserste.png",
            url="https://daserste.m3u8",
        ),
        Stream(
            name="ZDF",
            tvg_name="ZDF",
            quality="sd",
            radio=False,
            tvg_id="zdf.de",
            group_title="IPTV-DE",
            group_title_kodi="Vollprogramm",
            tvg_logo="tv/zdf.png",
            url="https://zdf.m3u8",
        ),
        Stream(
            group_title="Radio-DE",
            group_title_kodi="Deutschland",
            name="Deutschlandfunk",
            quality="",
            radio=True,
            tvg_id="dlf.de",
            tvg_logo="radio/deutschlandfunk.png",
            tvg_name="Deutschlandfunk",
            url="https://deutschlandfunk.aac",
        ),
    ]


@pytest.fixture()
def dash_streams() -> list[Stream]:
    """TODO."""
    return [
        Stream(
            name="Das Erste HD",
            tvg_name="Das Erste HD",
            quality="hd",
            radio=False,
            tvg_id="daserste.de",
            group_title="IPTV-DE",
            group_title_kodi="Vollprogramm",
            tvg_logo="tv/daserste.png",
            url="https://daserste.mpd",
        ),
        Stream(
            name="ZDF",
            tvg_name="ZDF",
            quality="sd",
            radio=False,
            tvg_id="zdf.de",
            group_title="IPTV-DE",
            group_title_kodi="Vollprogramm",
            tvg_logo="tv/zdf.png",
            url="https://zdf.mpd",
        ),
        Stream(
            group_title="Radio-DE",
            group_title_kodi="Deutschland",
            name="Deutschlandfunk",
            quality="",
            radio=True,
            tvg_id="dlf.de",
            tvg_logo="radio/deutschlandfunk.png",
            tvg_name="Deutschlandfunk",
            url="https://deutschlandfunk.mpd",
        ),
    ]


@pytest.mark.parametrize("list_type", [ListType.CLEAN])
def test_get_default_lines(line_writer: LineWriter, m3u8_streams: list[Stream]) -> None:
    """TODO."""
    expected = [
        [
            '#EXTINF:-1 tvg-name="Das Erste HD" tvg-id="daserste.de" group-title="IPTV-DE" tvg-logo="https://example.com/logos/tv/daserste.png",Das Erste HD',  # noqa: E501
            "https://daserste.m3u8",
        ],
        [
            '#EXTINF:-1 tvg-name="ZDF" tvg-id="zdf.de" group-title="IPTV-DE" tvg-logo="https://example.com/logos/tv/zdf.png",ZDF',  # noqa: E501
            "https://zdf.m3u8",
        ],
        [
            '#EXTINF:-1 tvg-name="Deutschlandfunk" group-title="Radio-DE" radio="true" tvg-logo="https://example.com/logos/radio/deutschlandfunk.png",Deutschlandfunk',  # noqa: E501
            "https://deutschlandfunk.aac",
        ],
    ]

    actual = [line_writer.get_lines(stream) for stream in m3u8_streams]

    assert actual == expected


@pytest.mark.parametrize("list_type", [ListType.KODI])
def test_get_kodi_lines(line_writer: LineWriter, m3u8_streams: list[Stream]) -> None:
    """TODO."""
    expected = [
        [
            '#EXTINF:-1 tvg-name="Das Erste HD" tvg-id="daserste.de" group-title="Vollprogramm" tvg-logo="https://example.com/logos/tv/daserste.png",Das Erste HD',  # noqa: E501
            "https://daserste.m3u8",
        ],
        [
            '#EXTINF:-1 tvg-name="ZDF" tvg-id="zdf.de" group-title="Vollprogramm" tvg-logo="https://example.com/logos/tv/zdf.png",ZDF',  # noqa: E501
            "https://zdf.m3u8",
        ],
        [
            '#EXTINF:-1 tvg-name="Deutschlandfunk" group-title="Deutschland" radio="true" tvg-logo="https://example.com/logos/radio/deutschlandfunk.png",Deutschlandfunk',  # noqa: E501
            "https://deutschlandfunk.aac",
        ],
    ]

    actual = [line_writer.get_lines(stream) for stream in m3u8_streams]

    assert actual == expected


@pytest.mark.parametrize("list_type", [ListType.PIPE])
def test_get_pipe_lines(line_writer: LineWriter, m3u8_streams: list[Stream]) -> None:
    """TODO."""
    expected = [
        [
            '#EXTINF:-1 tvg-name="Das Erste HD" tvg-id="daserste.de" group-title="IPTV-DE" tvg-logo="https://example.com/logos/tv/daserste.png",Das Erste HD',  # noqa: E501
            "pipe://ffmpeg -loglevel fatal -i https://daserste.m3u8 -vcodec copy -acodec copy -metadata service_name=Das\\ Erste\\ HD -metadata service_provider=IPTV-DE -mpegts_service_type advanced_codec_digital_hdtv -f mpegts pipe:1",  # noqa: E501
        ],
        [
            '#EXTINF:-1 tvg-name="ZDF" tvg-id="zdf.de" group-title="IPTV-DE" tvg-logo="https://example.com/logos/tv/zdf.png",ZDF',  # noqa: E501
            "pipe://ffmpeg -loglevel fatal -i https://zdf.m3u8 -vcodec copy -acodec copy -metadata service_name=ZDF -metadata service_provider=IPTV-DE -mpegts_service_type advanced_codec_digital_sdtv -f mpegts pipe:1",  # noqa: E501
        ],
        [
            '#EXTINF:-1 tvg-name="Deutschlandfunk" group-title="Radio-DE" radio="true" tvg-logo="https://example.com/logos/radio/deutschlandfunk.png",Deutschlandfunk',  # noqa: E501
            "pipe://ffmpeg -loglevel fatal -i https://deutschlandfunk.aac -vcodec copy -acodec copy -metadata service_name=Deutschlandfunk -metadata service_provider=Radio-DE -mpegts_service_type advanced_codec_digital_radio -f mpegts pipe:1",  # noqa: E501
        ],
    ]

    actual = [line_writer.get_lines(stream) for stream in m3u8_streams]

    assert actual == expected


@pytest.mark.parametrize("list_type", [ListType.DASH])
def test_get_dash_lines(line_writer: LineWriter, dash_streams: list[Stream]) -> None:
    """TODO."""
    expected = [
        [
            '#EXTINF:-1 tvg-name="Das Erste HD" tvg-id="daserste.de" group-title="Vollprogramm" tvg-logo="https://example.com/logos/tv/daserste.png",Das Erste HD',  # noqa: E501
            "#KODIPROP:inputstreamaddon=inputstream.adaptive",
            "#KODIPROP:inputstream.adaptive.manifest_type=mpd",
            "https://daserste.mpd",
        ],
        [
            '#EXTINF:-1 tvg-name="ZDF" tvg-id="zdf.de" group-title="Vollprogramm" tvg-logo="https://example.com/logos/tv/zdf.png",ZDF',  # noqa: E501
            "#KODIPROP:inputstreamaddon=inputstream.adaptive",
            "#KODIPROP:inputstream.adaptive.manifest_type=mpd",
            "https://zdf.mpd",
        ],
        [
            '#EXTINF:-1 tvg-name="Deutschlandfunk" group-title="Deutschland" radio="true" tvg-logo="https://example.com/logos/radio/deutschlandfunk.png",Deutschlandfunk',  # noqa: E501
            "#KODIPROP:inputstreamaddon=inputstream.adaptive",
            "#KODIPROP:inputstream.adaptive.manifest_type=mpd",
            "https://deutschlandfunk.mpd",
        ],
    ]

    actual = [line_writer.get_lines(stream) for stream in dash_streams]

    assert actual == expected
