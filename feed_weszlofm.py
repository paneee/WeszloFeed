import datetime
import PyRSS2Gen
import os
from os import listdir
from os.path import isfile, isdir, join, islink
from eyed3.id3 import Tag
import unidecode

root_path = os.getcwd() + "/"
only_folders_from_root_path = [f for f in listdir(
    root_path) if isdir(join(root_path, f))]

items = []
tag = Tag()

for path_folder in only_folders_from_root_path:
    path_files = root_path + path_folder
    only_files = [f for f in listdir(
        path_files) if isfile(join(path_files, f)) and not islink(join(path_files, f))]
    for path in only_files:
        tag.parse(path_files + "/" + path)
        item = PyRSS2Gen.RSSItem(
            title=unidecode.unidecode(tag.artist),
            link=("https://www.simx.mobi/weszlo/" + path_folder + "/" + path),
            description=unidecode.unidecode(tag.title),
            guid=PyRSS2Gen.Guid("https://www.simx.mobi/weszlo/" + path_folder + "/" + path),
            pubDate=datetime.datetime(2018, 9, 5, 2, 00),
        )
        items.append(item)

rss = PyRSS2Gen.RSS2(
    title="WESZLO FM",
    link="https://www.simx.mobi/weszlo/feed.rss",
    description="Nieoficjalne archiwum WESZLO FM",
    lastBuildDate=datetime.datetime.now(),
    items=items)

rss.write_xml(open("feed.xml", "w"))
