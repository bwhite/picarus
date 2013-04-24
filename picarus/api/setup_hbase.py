import hadoopy_hbase
import argparse


def main():
    parser = argparse.ArgumentParser(description='Picarus user operations')
    parser.add_argument('--thrift_server', default='localhost')
    parser.add_argument('--thrift_port', default='9090')
    ARGS = parser.parse_args()
    hb = hadoopy_hbase.connect(ARGS.thrift_server, ARGS.thrift_port)
    hb.createTable('models', [hadoopy_hbase.ColumnDescriptor('data:', maxVersions=1, compression='SNAPPY'),
                              hadoopy_hbase.ColumnDescriptor('meta:', maxVersions=1),
                              hadoopy_hbase.ColumnDescriptor('user:', maxVersions=1)])
    hb.createTable('images', [hadoopy_hbase.ColumnDescriptor('data:', maxVersions=1),
                              hadoopy_hbase.ColumnDescriptor('meta:', maxVersions=1),
                              hadoopy_hbase.ColumnDescriptor('pred:', maxVersions=1),
                              hadoopy_hbase.ColumnDescriptor('thum:', maxVersions=1),
                              hadoopy_hbase.ColumnDescriptor('feat:', maxVersions=1, compression='SNAPPY'),
                              hadoopy_hbase.ColumnDescriptor('hash:', maxVersions=1)])

if __name__ == '__main__':
    main()
