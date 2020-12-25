#!/usr/bin/env python

import glob
import re
import yaml

streams = {}

# read .m3u
m3u_files = glob.glob("iptv/clean/clean_*_*.m3u")
for filename in m3u_files:
    m = re.search("clean_(.*)_(.*).m3u", filename)
    category = m.group(1)
    if not category in streams:
        streams[category] = {}
    subcategory = m.group(2)
    if not subcategory in streams[category]:
        streams[category][subcategory] = []

    extinf_found = False
    with open(filename) as m3u:
        for line in m3u:
            if line.startswith("#EXTINF"):
                m = re.search("tvg-name=\"(.*?)\"", line)
                tvg_name = m.group(1)
                m = re.search("tvg-id=\"(.*?)\"", line)
                if m:
                    tvg_id = m.group(1)
                else:
                    tvg_id = ""
                m = re.search("group-title=\"(.*?)\"", line)
                group_title = m.group(1)
                m = re.search("tvg-logo=\"(.*?)\"", line)
                tvg_logo = m.group(1)
                m = re.search(".*,(.*)", line)
                name = m.group(1).strip()
                extinf_found = True
            else:
                if extinf_found:
                    url = line.strip()
                    if name in streams[category][subcategory]:
                        print("WARNING: duplicate name \"" + name + "\". Ignoring.")
                    else:
                        stream = {"name": name, "tvg_id": tvg_id, "tvg_name": tvg_name, "group_title": group_title, "group_title_kodi": "", "tvg_logo": tvg_logo, "url": url, "quality": ""}
                        stream["radio"] = (category == "radio")
                        streams[category][subcategory].append(stream)
                    extinf_found = False

# read .m3u for Kodi (uses different group titles)
m3u_files = glob.glob("iptv/kodi/kodi_*_*.m3u")
for filename in m3u_files:
    m = re.search("kodi_(.*)_(.*).m3u", filename)
    category = m.group(1)
    if not category in streams:
        print("WARNING: category \"" + category + "\" exists only in Kodi list. Ignoring.")
        continue
    subcategory = m.group(2)
    if not subcategory in streams[category]:
        print("WARNING: category \"" + category + "\", subcategory \"" + subcategory + "\" exists only in Kodi list. Ignoring.")
        continue
    with open(filename) as m3u:
        for line in m3u:
            if line.startswith("#EXTINF"):
                m = re.search("group-title=\"(.*?)\"", line)
                group_title = m.group(1)
                m = re.search(".*,(.*)", line)
                name = m.group(1).strip()
                found = False
                for stream in streams[category][subcategory]:
                    if stream["name"] == name:
                        stream["group_title_kodi"] = group_title
                        found = True
                        break
                if not found:
                    print("WARNING: category \"" + category + "\", subcategory \"" + subcategory + "\", name \"" + name + "\" exists only in Kodi list. Ignoring.")

# read .m3u for pipe (find out if SD/HD)
m3u_files = glob.glob("iptv/pipe/pipe_*_*.m3u")
for filename in m3u_files:
    m = re.search("pipe_(.*)_(.*).m3u", filename)
    category = m.group(1)
    if not category in streams:
        print("WARNING: category \"" + category + "\" exists only in pipe list. Ignoring.")
        continue
    subcategory = m.group(2)
    if not subcategory in streams[category]:
        print("WARNING: category \"" + category + "\", subcategory \"" + subcategory + "\" exists only in pipe list. Ignoring.")
        continue
    with open(filename) as m3u:
        for line in m3u:
            if line.startswith("#EXTINF"):
                m = re.search(".*,(.*)", line)
                name = m.group(1).strip()
                extinf_found = True
            else:
                if extinf_found:
                    m = re.search("advanced_codec_digital_(.*)tv", line)
                    if m:
                        quality = m.group(1)
                        found = False
                        for stream in streams[category][subcategory]:
                            if stream["name"] == name:
                                stream["quality"] = quality
                                found = True
                                break
                        if not found:
                            print("WARNING: category \"" + category + "\", subcategory \"" + subcategory + "\", name \"" + name + "\" exists only in pipe list. Ignoring.")
                    extinf_found = False

# write yaml
with open("iptv/source.yaml", 'w') as file:
    try:
        documents = yaml.dump(streams, file, allow_unicode=True)
    except yaml.YAMLError as exc:
        print(exc)
