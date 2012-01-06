#!/usr/bin/env python
import urllib2
import socket
import hadoopy


def download_file(url):
    num_attempts = 3
    socket.setdefaulttimeout(3)
    for attempt in range(num_attempts):
        try:
            data = urllib2.urlopen(url).read()
            break
        except Exception, e:
            if attempt == (num_attempts - 1):  # If last attempt
                raise e
    return data


def mapper(key, value):
    print(key)
    url = key
    try:
        data = download_file(url)
    except Exception:
        hadoopy.counter('FILE_DOWNLOADER', 'Exception')
    else:
        yield url, data


if __name__ == "__main__":
    hadoopy.run(mapper)
