#!/usr/bin/env python
import time
import random
import xml.parsers.expat
import urllib2
import httplib
import hadoopy
import flickrapi
api_key = ''  # NOTE(brandyn): Include your flickr api key and secret here
api_secret = ''
try:
    from flickr_api_key import api_key, api_secret
except ImportError:
    if not api_key or not api_secret:
        print('Missing flickr API key')
        import sys
        sys.exit(1)


class Mapper(object):
    def __init__(self):
        self.api_key = api_key
        self.api_secret = api_secret
        self.earliest = 1167631200
        self.date_radius = 1296000  # seconds_in_month/2
        self.per_page = 500
        self.tag_iters = os.environ.get('TAG_ITERS', 1)
        self.sleep_penalty = 15
        self.sleep_penalty_orig = 15
        self.extras = 'description,license,date_upload,date_taken,owner_name,icon_server,original_format,last_update,geo,tags,machine_tags,o_dims,views,media,path_alias,url_sq,url_t,url_s,url_m,url_o'
        self.flickr = flickrapi.FlickrAPI(self.api_key)
        self.min_rnd_date = self.earliest + self.date_radius
        self.max_rnd_date = int(time.time()) - self.date_radius
        self.num_pages = 1

    def _query(self, value, dates=None, page=None):
        try:
            kw = {}
            if dates:
                kw['min_upload_date'] = dates[0]
                kw['max_upload_date'] = dates[1]
            if page:
                kw['page'] = page
            return self.flickr.photos_search(text=value,
                                             extras=self.extras,
                                             per_page=self.per_page,
                                             **kw)
            self.sleep_penalty = self.sleep_penalty_orig
        except (httplib.BadStatusLine,
                flickrapi.exceptions.FlickrError,
                xml.parsers.expat.ExpatError,
                urllib2.HTTPError):
            time.sleep(self.sleep_penalty)
            self.sleep_penalty *= 2

    def _get_data(self, res):
        if res:
            for photo in res.find('photos'):
                photo = dict(photo.items())
                try:
                    yield photo['url_m'], photo
                except KeyError:
                    return

    def map(self, key, value):
        for page in range(1, self.num_pages):
            for x in self._get_data(self._query(value, page=page)):
                yield x
        
        for i in range(self.tag_iters):
            print(i)
            cur_time_center = random.randint(self.min_rnd_date, self.max_rnd_date)
            min_date = cur_time_center - self.date_radius
            max_date = cur_time_center + self.date_radius
            for x in self._get_data(self._query(value, (min_date, max_date))):
                yield x


def reducer(key, values):
    yield key, values.next()


if __name__ == "__main__":
    if hadoopy.run(Mapper, reducer, reducer):
        hadoopy.print_doc_quit(__doc__)
