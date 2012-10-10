import zmq
from _picarus_search_pb2 import SearchIndex


class InternalServer(object):

    def __init__(self):
        super(InternalServer, self).__init__()

    def listen(self, sock):
        while True:
            sock.send(self.output_tostring(self(self.input_fromstring(sock.recv()))))

    @classmethod
    def send(cls, sock, data):
        sock.send(cls.input_tostring(data))
        return cls.output_fromstring(sock.recv())


class PBInternalServer(InternalServer):

    def __init__(self):
        super(PBInternalServer, self).__init__()

    @classmethod
    def _data_tostring(cls, pb_cls, data):
        assert isinstance(data, dict)
        pb = pb_cls()
        for k, v in data.items():
            if isinstance(v, list):
                getattr(pb, k).extend(v)
            else:
                setattr(pb, k, v)
        return pb.SerializeToString()

    @classmethod
    def input_tostring(cls, data):
        return cls._data_tostring(cls.input_pb_cls, data)

    @classmethod
    def input_fromstring(cls, string):
        return cls.input_pb_cls.ParseFromString(string)

    @classmethod
    def output_tostring(cls, data):
        return cls._data_tostring(cls.output_pb_cls, data)

    @classmethod
    def output_fromstring(cls, string):
        return cls.output_pb_cls.ParseFromString(string)


class FeatureServer(PBInternalServer):

    def __init__(self):
        super(FeatureServer, self).__init__()

    def __call__(image):
        return ''


class SearchServer(PBInternalServer):

    def __init__(self):
        super(SearchServer, self).__init__()

    def __call__(image):
        return ''
