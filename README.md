# Kodinerds IPTV
## Einleitung
Kodinerds IPTV ist eine Sammlung von frei empfangbaren Streams für TV- und Radiosender.

Eine ausführliche Anleitung und Beschreibung findet sich auf Kodinerds.net: [Kodinerds IPTV auf Kodinerds.net](https://www.kodinerds.net/index.php/Thread/56713/)

Dieses Angebot stellt ein Parallelangebot zu [Entertain IPTV](https://github.com/jnk22/entertain-iptv) für Telekom EntertainTV-Kunden dar.

## Beschreibung / Erklärung
Die Listen sind unterteilt in verschiedene Typen, hier gibt es folgende Typen:

* kodi - Für den optimalen Empfang in Kodi, mit Kategorien für TV-Kanäle. Zu benutzen mit beiden Versionen des PVR IPTV Simple Client.
* clean - Basisliste mit Kategorisierung nach Land. Zum Beispiel für den VLC media player optimal.
* pipe - Liste mit Streams für das PVR-Backend Tvheadend. Streams setzen ffmpeg voraus, installiert unter /usr/bin/ffmpeg.
* rtmp - Weitere Streams, hauptsächlich Lokalsender. Anderes Protokoll, daher als Extraliste.
* dash - Ein paar weitere Sender als DASH-Streams. Eher für Testzwecke gedacht.

Hinweis: Die Listen kodi, clean und pipe sind inhaltlich identisch.

Jede der Listen ist unterteilt in eine Struktur, die dem Benutzer ein individuelles Angebot ermöglichen soll. Dabei gilt folgende Struktur:

```
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

Hinweis: Alle Unterlisten zusammen beinhalten jeweils den gesamten Inhalt der Oberliste. So stellen beispielsweise die Listen kodi_tv und kodi_radio die Liste kodi dar. Die Benutzung von kodi oder weiteren Unterlisten würde daher keinen Mehrwert bringen.

## Links zu den Listen
### kodi - für PVR IPTV Simple Client mit Inhaltskategorien (Kodi)
* http://bit.ly/kn-kodi

  * http://bit.ly/kn-kodi-tv

    * http://bit.ly/kn-kodi-tv-main
    * http://bit.ly/kn-kodi-tv-shop
    * http://bit.ly/kn-kodi-tv-regional
    * http://bit.ly/kn-kodi-tv-local
    * http://bit.ly/kn-kodi-tv-extra
    * http://bit.ly/kn-kodi-tv-atch
    * http://bit.ly/kn-kodi-tv-usuk
    * http://bit.ly/kn-kodi-tv-international

  * http://bit.ly/kn-kodi-radio

    * http://bit.ly/kn-kodi-radio-de
    * http://bit.ly/kn-kodi-radio-at
    * http://bit.ly/kn-kodi-radio-ch
    * http://bit.ly/kn-kodi-radio-uk
    * http://bit.ly/kn-kodi-radio-fr
    * http://bit.ly/kn-kodi-radio-nl
    * http://bit.ly/kn-kodi-radio-pl1

### clean - Basisliste mit IPTV-Kanälen (VLC media player)
* http://bit.ly/kn-clean

  * http://bit.ly/kn-clean-tv

    * http://bit.ly/kn-clean-tv-main
    * http://bit.ly/kn-clean-tv-shop
    * http://bit.ly/kn-clean-tv-regional
    * http://bit.ly/kn-clean-tv-local
    * http://bit.ly/kn-clean-tv-extra
    * http://bit.ly/kn-clean-tv-atch
    * http://bit.ly/kn-clean-tv-usuk
    * http://bit.ly/kn-clean-tv-international

  * http://bit.ly/kn-clean-radio

    * http://bit.ly/kn-clean-radio-de
    * http://bit.ly/kn-clean-radio-at
    * http://bit.ly/kn-clean-radio-ch
    * http://bit.ly/kn-clean-radio-uk
    * http://bit.ly/kn-clean-radio-fr
    * http://bit.ly/kn-clean-radio-nl
    * http://bit.ly/kn-clean-radio-pl1

### pipe - Basisliste mit IPTV-Kanälen (Tvheadend)
* http://bit.ly/kn-pipe

  * http://bit.ly/kn-pipe-tv

    * http://bit.ly/kn-pipe-tv-main
    * http://bit.ly/kn-pipe-tv-shop
    * http://bit.ly/kn-pipe-tv-regional
    * http://bit.ly/kn-pipe-tv-local
    * http://bit.ly/kn-pipe-tv-extra
    * http://bit.ly/kn-pipe-tv-atch
    * http://bit.ly/kn-pipe-tv-usuk
    * http://bit.ly/kn-pipe-tv-international

  * http://bit.ly/kn-pipe-radio

    * http://bit.ly/kn-pipe-radio-de
    * http://bit.ly/kn-pipe-radio-at
    * http://bit.ly/kn-pipe-radio-ch
    * http://bit.ly/kn-pipe-radio-uk
    * http://bit.ly/kn-pipe-radio-fr
    * http://bit.ly/kn-pipe-radio-nl
    * http://bit.ly/kn-pipe-radio-pl1

### rtmp - RTMP-Streams
* http://bit.ly/kn-rtmp

  * http://bit.ly/kn-rtmp-tv

    * http://bit.ly/kn-rtmp-tv-main
    * http://bit.ly/kn-rtmp-tv-local
    * http://bit.ly/kn-rtmp-tv-international

### dash - DASH-Streams
* http://bit.ly/kn-dash

  * http://bit.ly/kn-dash-tv

    * http://bit.ly/kn-dash-tv-main
    * http://bit.ly/kn-dash-tv-regional
    * http://bit.ly/kn-dash-tv-extra

  * http://bit.ly/kn-dash-radio

    * http://bit.ly/kn-dash-radio-uk

## Stream URL ermitteln
Um die Stream URL für einen bestimmten Stream zu ermitteln, lässt sich z.B. Firefox nutzen:
1. Stream in Firefox abspielen
2. Entwicklertools öffnen (F12)
3. Netzwerkanalyse Tab öffnen
4. Stream Datei in der Liste suchen (typischerweise `.m3u8`)
5. Stream URL im Detailfenster (rechte Seite) unter "Kopfzeilen" finden

Hilfreich ist das Firefox-Add-On [The Stream Detector](https://addons.mozilla.org/de/firefox/addon/hls-stream-detector/).

## Weiterführende Links
* [Link zum direkten Abspielen der Liste](https://iptvnator.vercel.app/iptv?url=http:%2F%2Fbit.ly%2Fkn-kodi-tv)
* [Aktuelle To-Do Liste](https://github.com/jnk22/kodinerds-iptv/issues)
* [Kodinerds IPTV auf Kodinerds.net](https://www.kodinerds.net/index.php/Thread/56713/)
* [Entertain IPTV auf Kodinerds.net](https://www.kodinerds.net/index.php/Thread/58228/)
* [Entertain IPTV auf GitHub](https://github.com/jnk22/entertain-iptv)
