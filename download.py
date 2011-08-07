import feedparser
import urllib
import os
import time

flickr_url = 'http://api.flickr.com/services/feeds/photos_public.gne?tags=coscup'
picasa_url = 'https://picasaweb.google.com/data/feed/base/all?alt=rss&kind=photo&access=public&filter=1&q=coscup&hl=en_US'

def download():
    print "fetching flickr feed"
    flickr = feedparser.parse(flickr_url)

    print "fetching picasa feed"
    picasa = feedparser.parse(picasa_url)

    migration = sorted(flickr['entries'] + picasa['entries'], \
        key=lambda item: item['updated'],reverse=True)[:10]

    for item in migration:
        filename = 'images/' + item['updated'] + '.jpg';
        url = None
        if os.path.exists(filename):
            print "%s exist" % filename
            continue
        links = [n for n in item['links'] if n['type'] == 'image/jpeg']
        if len(links) > 0:
	    url = links[0]['href']
        if item.has_key('enclosures'):
            enclosures = [n for n in item['enclosures'] if n['type'] == 'image/jpeg']
            if len(enclosures) > 0:
                url = enclosures[0]['href']

        if url == None: continue
        print "download %s" % filename
        remote = urllib.urlopen(url)
        file = open(filename, 'w')
        file.write(remote.read())
        remote.close()
        file.close()

def main():
    if not os.path.exists ('images'):
        os.mkdirs('images')
    sleep_time = 30
    while(True):
        download()
        print "sleep %s secs" % sleep_time
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()


