import hadoopy_hbase
c = hadoopy_hbase.connect()
for x, y in hadoopy_hbase.scanner(c, 'images', start_row='brandynlive:', stop_row='brandynlivf:'):
    assert x.startswith('brandynlive:')
    print(x)
    c.deleteAllRow('images', x)
#c.majorCompact('images')
