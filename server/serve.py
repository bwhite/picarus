import gevent
from gevent import monkey
monkey.patch_all()
import bottle
import argparse
bottle.debug(True)


@bottle.put('/')
def take_data():
    print(bottle.request.json)
    return {'result': {'nouns': ['car', 'dog']}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
