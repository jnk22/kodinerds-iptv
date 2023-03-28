#!/usr/bin/env python3

import glob
import re
import yaml

category_ids = { "radio" : 2, "tv" : 1 }

subcategory_ids = {
    "tv" :
    {
        "atch" : 6,
        "extra" : 5,
        "international" : 8,
        "local" : 4,
        "main" : 1,
        "regional" : 3,
        "shop" : 2,
        "usuk" : 7
    },
    "radio":
    {
        "at" : 2,
        "ch" : 3,
        "de" : 1,
        "fr" : 5,
        "nl" : 6,
        "pl" : 7,
        "uk" : 4
    }
}


streams = {}

# read .m3u
m3u_files = glob.glob("iptv/clean/clean_*_*.m3u")
for filename in m3u_files:
    m = re.search("clean_(.*)_(.*).m3u", filename)
    category = m[1]
    if category not in streams:
        category_id = 0
        if category in category_ids:
            category_id = category_ids[category]
        else:
            print("WARNING: could not determine category ID for \"" + category + "\"")
        streams[category] = { "id" : category_id, "subcategories" : {} }
    subcategory = m[2]
    if subcategory not in streams[category]["subcategories"]:
        subcategory_id = 0
        if (
            category in subcategory_ids
            and subcategory in subcategory_ids[category]
        ):
            subcategory_id = subcategory_ids[category][subcategory]
        if subcategory_id == 0:
            print("WARNING: could not determine subcategory ID for \"" + subcategory + "\"")
        streams[category]["subcategories"][subcategory] = { "id" : subcategory_id, "streams" : [] }

    extinf_found = False
    with open(filename) as m3u:
        for line in m3u:
            if line.startswith("#EXTINF"):
                m = re.search("tvg-name=\"(.*?)\"", line)
                tvg_name = m[1]
                m = re.search("tvg-id=\"(.*?)\"", line)
                tvg_id = m[1] if m else ""
                m = re.search("group-title=\"(.*?)\"", line)
                group_title = m[1]
                m = re.search("tvg-logo=\"(.*?)\"", line)
                tvg_logo = m[1]
                m = re.search(".*,(.*)", line)
                name = m[1].strip()
                extinf_found = True
            elif extinf_found:
                url = line.strip()
                if name in streams[category]["subcategories"][subcategory]:
                    print("WARNING: duplicate name \"" + name + "\". Ignoring.")
                else:
                    stream = {
                        "name": name,
                        "tvg_id": tvg_id,
                        "tvg_name": tvg_name,
                        "group_title": group_title,
                        "group_title_kodi": "",
                        "tvg_logo": tvg_logo,
                        "url": url,
                        "quality": "",
                        "radio": category == "radio",
                    }
                    streams[category]["subcategories"][subcategory]["streams"].append(stream)
                extinf_found = False

# read .m3u for Kodi (uses different group titles)
m3u_files = glob.glob("iptv/kodi/kodi_*_*.m3u")
for filename in m3u_files:
    m = re.search("kodi_(.*)_(.*).m3u", filename)
    category = m[1]
    if category not in streams:
        print("WARNING: category \"" + category + "\" exists only in Kodi list. Ignoring.")
        continue
    subcategory = m[2]
    if subcategory not in streams[category]["subcategories"]:
        print("WARNING: category \"" + category + "\", subcategory \"" + subcategory + "\" exists only in Kodi list. Ignoring.")
        continue
    with open(filename) as m3u:
        for line in m3u:
            if line.startswith("#EXTINF"):
                m = re.search("group-title=\"(.*?)\"", line)
                group_title = m[1]
                m = re.search(".*,(.*)", line)
                name = m[1].strip()
                found = False
                for stream in streams[category]["subcategories"][subcategory]["streams"]:
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
    category = m[1]
    if category not in streams:
        print("WARNING: category \"" + category + "\" exists only in pipe list. Ignoring.")
        continue
    subcategory = m[2]
    if subcategory not in streams[category]["subcategories"]:
        print("WARNING: category \"" + category + "\", subcategory \"" + subcategory + "\" exists only in pipe list. Ignoring.")
        continue
    with open(filename) as m3u:
        for line in m3u:
            if line.startswith("#EXTINF"):
                m = re.search(".*,(.*)", line)
                name = m[1].strip()
                extinf_found = True
            elif extinf_found:
                if m := re.search("advanced_codec_digital_(.*)tv", line):
                    quality = m[1]
                    found = False
                    for stream in streams[category]["subcategories"][subcategory]["streams"]:
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
