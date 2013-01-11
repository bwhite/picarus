import hadoopy_hbase
c = hadoopy_hbase.connect()


def delete_rows(prefix):
    assert ord(prefix[-1]) != 255
    stop_row = prefix[:-1] + chr(ord(prefix[-1]) + 1)
    for x, y in hadoopy_hbase.scanner(c, 'images', start_row=prefix, stop_row=stop_row):
        assert x.startswith(prefix)
        print(repr(x))
        c.deleteAllRow('images', x)
    #c.majorCompact('images')
delete_rows('landmarks:flickr')
