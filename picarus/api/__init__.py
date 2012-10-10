import zmq
from _picarus_search_pb2 import SearchIndex

class InternalServer(object):

    def __init__(self, remote=False):
        """
        Args:
            remote: If True, server 
        """
        super(InternalServer, self).__init__()


class FeatureServer(InternalServer):

    def __init__(self):
        super(FeatureServer, self).__init__()

    def __call__(image):
        return ''


class SearchServer(InternalServer):

    def __init__(self):
        super(SearchServer, self).__init__()

    def __call__(image):
        return ''
