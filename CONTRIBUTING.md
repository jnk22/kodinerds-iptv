# Streams hinzufügen/ändern
Eine detaillierte Anleitung zum GitHub workflow findet sich [hier](https://git-scm.com/book/de/v2/GitHub-Mitwirken-an-einem-Projekt).
Es ist nicht erforderlich, das Repository auszuchecken. Alle Änderungen können im Browser vorgenommen werden.

1. Repository forken
2. Im Fork einen neuen Branch anlegen
3. Änderungen in `iptv/clean/clean.m3u` einbauen (z.B. URL ändern)
4. Änderungen in `iptv/clean/clean_<kategorie>.m3u` einbauen (z.B. `clean_tv.m3u`)
5. Änderungen in `iptv/clean/clean_<kategorie>_<unterkategorie>.m3u` einbauen (z.B. `clean_tv_local.m3u`)
6. Schritte 3-5 für `kodi`, `pipe` und `rtmp` wiederholen
7. Pull Reqeust erstellen (Titel z.B. "Fix ..." oder "Add ...")

# Links
- [GitHub - Mitwirken an einem Projekt](https://git-scm.com/book/de/v2/GitHub-Mitwirken-an-einem-Projekt)
