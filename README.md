# Kodinerds IPTV

[![CI](https://github.com/jnk22/kodinerds-iptv/actions/workflows/ci.yml/badge.svg)](https://github.com/jnk22/kodinerds-iptv/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/jnk22/kodinerds-iptv/branch/update-script/graph/badge.svg?token=hi6gqcnIPM)](https://codecov.io/gh/jnk22/kodinerds-iptv)
[![Maintainability](https://api.codeclimate.com/v1/badges/242bd9127abdaab359d6/maintainability)](https://codeclimate.com/github/jnk22/kodinerds-iptv/maintainability)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/885b3ad68d5d49688cd493861ab30a6c)](https://www.codacy.com/gh/jnk22/kodinerds-iptv/dashboard?utm_source=github.com&utm_medium=referral&utm_content=jnk22/kodinerds-iptv&utm_campaign=Badge_Grade)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jnk22/kodinerds-iptv/master.svg)](https://results.pre-commit.ci/latest/github/jnk22/kodinerds-iptv/master)

Kodinerds IPTV ist eine Sammlung von frei empfangbaren Streams für TV- und Radiosender.

Eine ausführliche Anleitung und Beschreibung findet sich auf Kodinerds.net:
[Kodinerds IPTV auf Kodinerds.net](https://www.kodinerds.net/index.php/Thread/56713/)

## Beschreibung / Erklärung

Die Listen sind unterteilt in verschiedene Typen, hier gibt es folgende Typen:

- kodi - Für den optimalen Empfang in Kodi, mit Kategorien für TV-Kanäle. Zu
  benutzen mit beiden Versionen des PVR IPTV Simple Client.
- clean - Basisliste mit Kategorisierung nach Land. Zum Beispiel für den
  VLC media player optimal.
- pipe - Liste mit Streams für das PVR-Backend Tvheadend. Streams setzen ffmpeg
  voraus, installiert under /usr/bin/ffmpeg.
- rtmp - Weitere Streams, hauptsächlich Lokalsender. Anderes Protokoll, daher
  also Extraliste.
- dash - Ein paar weitere Sender also DASH-Streams. Eher für Testzwecke gedacht.

Hinweis: Die Listen kodi, clean und pipe sind inhaltlich identisch.

Jede der Listen ist unterteilt in eine Struktur, die dem Benutzer ein
individuelles Angebot ermöglichen soll.
Dabei gilt folgende Struktur:

```text
- [typ] - beinhaltet alle TV- und Radiosender

- - [typ]_tv - beinhaltet nur TV-Sender

- - - [typ]_tv_main - nur deutsche Hauptsender
- - - [typ]_tv_shop - nur deutsche Teleshopping-Sender
- - - [typ]_tv_regional - nur deutsche Regionalsender
- - - [typ]_tv_local - nur deutsche Lokalsender
- - - [typ]_tv_extra - nur deutsche Extra-Sender (Online-Sender der Öffentlich-Rechtlichen)
- - - [typ]_tv_atch - nur TV-Sender aus Österreich und Schweiz
- - - [typ]_tv_usuk - nur TV-Sender aus Großbritannien und USA
- - - [typ]_tv_international - nur internationale Sender (außer Sender aus AT/CH/US/UK)

- - [typ]_radio - beinhaltet nur Radiosender

- - - [typ]_radio_de - nur Radiosender aus Deutschland
- - - [typ]_radio_at - nur Radiosender aus Österreich
- - - [typ]_radio_ch - nur Radiosender aus der Schweiz
- - - [typ]_radio_uk - nur Radiosender aus Großbritannien
- - - [typ]_radio_fr - nur Radiosender aus Frankreich
- - - [typ]_radio_nl - nur Radiosender aus den Niederlanden
- - - [typ]_radio_pl1 - nur Radiosender aus Polen
```

**Hinweis:**
Alle Unterlisten zusammen beinhalten jeweils den gesamten Inhalt der Oberliste.
So stellen beispielsweise die Listen kodi_tv und kodi_radio die Liste kodi dar.
Die Benutzung von kodi oder weiteren Unterlisten würde daher keinen Mehrwert bringen.

## Links zu den Listen

### kodi - für PVR IPTV Simple Client mit Inhaltskategorien (Kodi)

- <https://bit.ly/kn-kodi>
  - <https://bit.ly/kn-kodi-tv>
    - <https://bit.ly/kn-kodi-tv-main>
    - <https://bit.ly/kn-kodi-tv-shop>
    - <https://bit.ly/kn-kodi-tv-regional>
    - <https://bit.ly/kn-kodi-tv-local>
    - <https://bit.ly/kn-kodi-tv-extra>
    - <https://bit.ly/kn-kodi-tv-atch>
    - <https://bit.ly/kn-kodi-tv-usuk>
    - <https://bit.ly/kn-kodi-tv-international>
  - <https://bit.ly/kn-kodi-radio>
    - <https://bit.ly/kn-kodi-radio-de>
    - <https://bit.ly/kn-kodi-radio-at>
    - <https://bit.ly/kn-kodi-radio-ch>
    - <https://bit.ly/kn-kodi-radio-uk>
    - <https://bit.ly/kn-kodi-radio-fr>
    - <https://bit.ly/kn-kodi-radio-nl>
    - <https://bit.ly/kn-kodi-radio-pl1>

### clean - Basisliste mit IPTV-Kanälen (VLC media player)

- <https://bit.ly/kn-clean>
  - <https://bit.ly/kn-clean-tv>
    - <https://bit.ly/kn-clean-tv-main>
    - <https://bit.ly/kn-clean-tv-shop>
    - <https://bit.ly/kn-clean-tv-regional>
    - <https://bit.ly/kn-clean-tv-local>
    - <https://bit.ly/kn-clean-tv-extra>
    - <https://bit.ly/kn-clean-tv-atch>
    - <https://bit.ly/kn-clean-tv-usuk>
    - <https://bit.ly/kn-clean-tv-international>
  - <https://bit.ly/kn-clean-radio>
    - <https://bit.ly/kn-clean-radio-de>
    - <https://bit.ly/kn-clean-radio-at>
    - <https://bit.ly/kn-clean-radio-ch>
    - <https://bit.ly/kn-clean-radio-uk>
    - <https://bit.ly/kn-clean-radio-fr>
    - <https://bit.ly/kn-clean-radio-nl>
    - <https://bit.ly/kn-clean-radio-pl1>

### pipe - Basisliste mit IPTV-Kanälen (Tvheadend)

- <https://bit.ly/kn-pipe>
  - <https://bit.ly/kn-pipe-tv>
    - <https://bit.ly/kn-pipe-tv-main>
    - <https://bit.ly/kn-pipe-tv-shop>
    - <https://bit.ly/kn-pipe-tv-regional>
    - <https://bit.ly/kn-pipe-tv-local>
    - <https://bit.ly/kn-pipe-tv-extra>
    - <https://bit.ly/kn-pipe-tv-atch>
    - <https://bit.ly/kn-pipe-tv-usuk>
    - <https://bit.ly/kn-pipe-tv-international>
  - <https://bit.ly/kn-pipe-radio>
    - <https://bit.ly/kn-pipe-radio-de>
    - <https://bit.ly/kn-pipe-radio-at>
    - <https://bit.ly/kn-pipe-radio-ch>
    - <https://bit.ly/kn-pipe-radio-uk>
    - <https://bit.ly/kn-pipe-radio-fr>
    - <https://bit.ly/kn-pipe-radio-nl>
    - <https://bit.ly/kn-pipe-radio-pl1>

### rtmp - RTMP-Streams

- <https://bit.ly/kn-rtmp>
  - <https://bit.ly/kn-rtmp-tv>
    - <https://bit.ly/kn-rtmp-tv-main>
    - <https://bit.ly/kn-rtmp-tv-local>
    - <https://bit.ly/kn-rtmp-tv-international>

### dash - DASH-Streams

- <https://bit.ly/kn-dash>
  - <https://bit.ly/kn-dash-tv>
    - <https://bit.ly/kn-dash-tv-main>
    - <https://bit.ly/kn-dash-tv-regional>
    - <https://bit.ly/kn-dash-tv-extra>
  - <https://bit.ly/kn-dash-radio>
    - <https://bit.ly/kn-dash-radio-uk>

## Stream URL ermitteln

Um die Stream URL für einen bestimmten Stream zu ermitteln, lässt sich z.B.
Firefox nutzen:

1. Stream in Firefox abspielen
2. Entwicklertools öffnen (F12)
3. Netzwerkanalyse Tab öffnen
4. Stream Datei in der Liste suchen (typischerweise `.m3u8`)
5. Stream URL im Detailfenster (rechte Seite) under "Kopfzeilen" finden

Hilfreich ist das Firefox-Add-On [The Stream Detector](https://addons.mozilla.org/de/firefox/addon/hls-stream-detector/).

## Weiterführende Links

- [Aktuelle To-Do Liste](https://github.com/jnk22/kodinerds-iptv/issues)
- [Kodinerds IPTV auf Kodinerds.net](https://www.kodinerds.net/index.php/Thread/56713/)
- [Entertain IPTV auf Kodinerds.net](https://www.kodinerds.net/index.php/Thread/58228/)
- [Entertain IPTV auf GitHub](https://github.com/jnk22/entertain-iptv)
