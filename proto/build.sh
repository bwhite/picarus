protoc -I=. --python_out=. picarus_search.proto
mv picarus_search_pb2.py ../picarus/api/_picarus_search_pb2.py