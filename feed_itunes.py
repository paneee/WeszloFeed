#!/usr/bin/python

from feedgen.feed import FeedGenerator
from urllib import urlencode
import datetime
import os
from os import listdir
from os.path import isfile, isdir, join, islink
from eyed3.id3 import Tag
import platform
from mutagen.mp3 import MP3
import time 

def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

fg = FeedGenerator()
fg.load_extension('podcast')
fg.title('Weszlo FM') 
fg.podcast.itunes_author('Weszlo FM')
fg.link(href='http://weszlo.com//', rel='alternate')
fg.subtitle('Nieoficjalny podcast Weszlo FM')
fg.language('en')
fg.copyright('cc-by-Weszlo')
fg.podcast.itunes_summary('Podcast Weszlo')
fg.podcast.itunes_owner('Krzysztof Stanowski', 'krzysztof.stanowski@weszlo.com')
fg.link(href='https://www.simx.mobi/weszlo/', rel='self')
fg.podcast.itunes_explicit('no')
fg.image('https://i1.sndcdn.com/avatars-000421118988-38c4cq-t200x200.jpg')
fg.podcast.itunes_image('https://i1.sndcdn.com/avatars-000421118988-38c4cq-t200x200.jpg')
fg.podcast.itunes_category('Sport', 'Sport News')


root_path = os.getcwd() + "/"
only_folders_from_root_path = [f for f in listdir(
    root_path) if isdir(join(root_path, f))]

items = []

for path_folder in only_folders_from_root_path:
    path_files = root_path + path_folder
    only_files = [f for f in listdir(
        path_files) if isfile(join(path_files, f)) and not islink(join(path_files, f))]
    for p in only_files:
        path = p.decode('utf-8')
        tag = Tag()
        tag.parse(path_files + "/" + path) 
        
        item = fg.add_entry()
        item.id("https://www.simx.mobi/weszlo/")
        item.title(tag.title)
        item.podcast.itunes_summary(tag.artist + " " + tag.title)
        item.podcast.itunes_subtitle(tag.artist + " " + tag.title)
        item.podcast.itunes_author(tag.artist)
        item.enclosure(u"https://www.simx.mobi/weszlo/" + path_folder + "/" + path, 0, 'audio/mpeg')
        
        audio = MP3(path_files + "/" + path)  
        normTime = time.strftime('%H:%M:%S', time.gmtime(audio.info.length))
        item.podcast.itunes_duration(normTime)
        
        dat = creation_date(path_files + "/" + path) 
        item.pubdate(str(datetime.datetime.fromtimestamp(dat)) + "-0000")
        items.append(item)

fg.rss_file('./feed.xml', pretty=True)
