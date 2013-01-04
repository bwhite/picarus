import hadoopy_hbase
import glob
import os
import json

c = hadoopy_hbase.connect()
table_name = 'images'
#c.createTable(table_name, [hadoopy_hbase.ColumnDescriptor('data:'),
#                           hadoopy_hbase.ColumnDescriptor('meta:')])
for x in glob.glob('/mnt/brandyn_extra/goodlogo_entity_images/*'):
    entity = os.path.basename(x)
    for y in glob.glob(x + '/*'):
        fn = os.path.basename(y)
        print((entity, fn))
        ms = [hadoopy_hbase.Mutation(column='data:image', value=open(y).read()),
              hadoopy_hbase.Mutation(column='meta:class', value=entity),
              hadoopy_hbase.Mutation(column='meta:file', value=fn)]
        entity_fn = '%s/%s' % (entity, fn)
        row = hadoopy_hbase.hash_key(entity_fn, prefix='logos:good', suffix=entity_fn, hash_bytes=4)
        c.mutateRow(table_name, row, ms)
#c.majorCompact(table_name)
