import feedparser
import urllib
import os
import time
import flickrapi
from datetime import datetime
import params
from xml.etree.ElementTree import Element, dump 

limit = 50
tag = 'coscup2010'
picasa_url = 'https://picasaweb.google.com/data/feed/base/all?alt=rss&kind=photo&access=public&q=%s&hl=en_US' % tag

def normalize(data):
    ret = []
    if type(data) is Element:
        photos = list(data.find('photos'))
        for p in photos:
            photo = {}
            photo['url'] = p.get('url_m')
            photo['time'] = datetime.fromtimestamp(float(p.get('dateupload'))).isoformat()
            ret.append(photo)
    else:
        photos = data['entries']
        for i in range(len(photos)):
            p = photos[i]
            photo = {}
            links = [n for n in p['links'] if n['type'] == 'image/jpeg']
            if len(links) > 0:
                photo['url'] = links[0]['href']
                photo['time'] = p['updated']
                ret.append(photo)
    return ret
        

def download():
    print "fetching flickr feed"
    flickr = flickrapi.FlickrAPI(params.flick_key)
    flickr_photos = flickr.photos_search(tags=tag, extras='date_upload,url_m')
    print "fetching picasa feed"
    picasa_photos = feedparser.parse(picasa_url)

    migration = sorted(normalize(flickr_photos) + normalize(picasa_photos), \
            key=lambda item: item['time'], reverse=True)[:limit]

    for item in migration:
        filename = 'images/' + item['time'] + '.jpg';
        if os.path.exists(filename):
            print "%s exist" % filename
            continue
        print "download %s" % filename
        remote = urllib.urlopen(item['url'])
        file = open(filename, 'w')
        file.write(remote.read())
        remote.close()
        file.close()

def main():
    if not os.path.exists ('images'):
        os.makedirs('images')
    sleep_time = 30
    while(True):
        download()
        print "sleep %s secs" % sleep_time
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()


