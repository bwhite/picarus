#!/usr/bin/env python
"""Web-scale Mosaic Maker

Files:
    target.jpg: JPEG file of the target image.
"""
import hadoopy
import numpy as np
import re
import cv2
import cStringIO as StringIO
import imfeat
import distpy

_subtile_length = 16
_tile_length = 256
_levels = 4
_initial_image_size = _subtile_length * 2 ** (_levels - 1)
_subtiles_per_tile_length = _tile_length / _subtile_length
_subtiles_per_tile = _subtiles_per_tile_length * _subtiles_per_tile_length
# NOTE(brandyn): Don't let a subtile span more than a single tile at the highest
# zoom level as the code is not currently written for that case.
assert _subtiles_per_tile_length / 2 ** _levels >= 1


class Mapper(object):

    def __init__(self):
        _target_image = cv2.imread('target.jpg')
        _target_image = cv2.resize(_target_image, (_target_image.shape[1] // _tile_length * _tile_length,
                                                   _target_image.shape[0] // _tile_length * _tile_length))
        self.target_tiles = {}
        ytiles = _target_image.shape[0] / _tile_length
        xtiles = _target_image.shape[1] / _tile_length
        print('Xtiles[%d] Ytiles[%d]' % (xtiles, ytiles))
        assert xtiles > 0 and ytiles > 0
        xsubtiles = xtiles * _subtiles_per_tile_length
        ysubtiles = ytiles * _subtiles_per_tile_length
        self.min_dists = {}
        self.dist = lambda x, y: np.sum(np.abs(x - y))  # distpy.L2Sqr().dist
        for y in xrange(ysubtiles):
            for x in xrange(xsubtiles):
                # Defines which tile the subtile is in
                #'%.6d_%.6d' %
                tile_id = (x / _subtiles_per_tile_length,
                           y / _subtiles_per_tile_length)
                # Defines which position it is in within the tile
                #'%.6d_%.6d' % 
                subtile_id = (x % _subtiles_per_tile_length,
                              y % _subtiles_per_tile_length)
                #'\t'.join(
                key = (tile_id[0], tile_id[1], subtile_id[0], subtile_id[1])
                yp = ysubtiles - y - 1  # NOTE(brandyn): Flip coordinates for y axis
                tile = _target_image[(yp * _subtile_length):((yp + 1) * _subtile_length), (x * _subtile_length): (x + 1) * _subtile_length, :]
                self.target_tiles[key] = np.asfarray(tile)

    @staticmethod
    def _crop_image_from_str(s):
        """Load from string, crop to a square, resize to _initial_image_size

        Args:
            s: String of bytes representing a JPEG image

        Returns:
            RGB Image with height/width as _initial_image_size

        Raises:
            ValueError: Image is height/width too small (< _initial_image_size)
                or mode isn't RGB
            IOError: Image is unreadable
        """
        if isinstance(s, tuple):
            s = s[0]
        try:
            img = imfeat.image_fromstring(s)
        except IOError, e:
            hadoopy.counter('Stats', 'IMG_BAD')
            raise e
        min_side = min(img.shape[:2])
        if min_side < _initial_image_size:
            hadoopy.counter('Stats', 'IMG_TOO_SMALL')
            raise ValueError
        if img.ndim != 3:
            hadoopy.counter('Stats', 'IMG_WRONG_MODE')
            raise ValueError
        return imfeat.resize_image(img, _initial_image_size, _initial_image_size)

    def _image_distance(self, img0, img1):
        """
        Args:
            img0: Numpy array
            img1: Numpy array

        Returns:
            Float valued distance where smaller means they are closer
        """
        return self.dist(img0.ravel(), img1.ravel())

    def map(self, key, value):
        """
        Args:
            key: Unused
            value: JPEG Image Data
        """
        print(key)
        try:
            images = [self._crop_image_from_str(value)]
        except (ValueError, IOError, AttributeError):
            return
        # Keep resizing until we get one for each layer, save them for later use
        prev_size = _initial_image_size
        for layer in range(1, _levels):
            prev_size /= 2
            images.append(cv2.resize(images[-1], (prev_size, prev_size)))
        scoring_tile = np.asfarray(images[-1])
        # Compute dist for each tile position, emit for each
        # Optimize by only emitting when we know the value is smaller than
        # we have seen in the close method)
        for key, target_tile in self.target_tiles.items():
            dist = self._image_distance(target_tile, scoring_tile)
            if key not in self.min_dists or dist < self.min_dists[key][0]:
                self.min_dists[key] = [dist, images]

    def close(self):
        """
        Yields:
            Tuple of (key, value) where
            key: tile_id\tsubtile_id (easily parsable by the
                KeyFieldBasedPartitioner)
            value: [dist, images] where images are power of 2 JPEG images
                in descending order by size
        """
        assert sorted(self.target_tiles.keys()) == sorted(self.min_dists.keys())
        for key, (dist, images) in self.min_dists.items():  # sorted(
            images_jpg = [imfeat.image_tostring(x, 'jpg') for x in images]  # JPEG's are much smaller
            yield key, [dist, images_jpg]


def combiner(key, values):
    """
    Args:
        key: (tile_id, subtile_id)
        values: Iterator of [dist, images] where images are power of 2 JPEG
            images in descending order by size

    Yields:
        Tuple of (key, value) where
        key: (tile_id, subtile_id)
        value: [dist, images] where images are power of 2 JPEG images
            in descending order by size
    """
    yield key, min(values, key=lambda x: x[0])


class Reducer(object):

    def __init__(self):
        self._sub_tiles = {}
        _parse_key_re = re.compile('([0-9]+)_([0-9]+)\t([0-9]+)_([0-9]+)')
        self._parse_key = lambda x: x  # map(int, _parse_key_re.search(x).groups())
        _target_image = cv2.imread('target.jpg')
        _target_image = cv2.resize(_target_image, (_target_image.shape[1] // _tile_length * _tile_length,
                                                   _target_image.shape[0] // _tile_length * _tile_length))
        self.num_ytiles = _target_image.shape[0] / _tile_length
        self.num_xtiles = _target_image.shape[1] / _tile_length

    def _find_output(self, key, scale, subtiles_per_tile_len, subtile_len):
        xtile, ytile, xsubtile, ysubtile = self._parse_key(key)
        xouttile = xtile * scale + xsubtile / subtiles_per_tile_len
        youttile = ytile * scale + ysubtile / subtiles_per_tile_len
        xoffset = (xsubtile % subtiles_per_tile_len) * subtile_len
        # NOTE(brandyn): Flip coordinates for y axis
        yoffset = (subtiles_per_tile_len - (ysubtile % subtiles_per_tile_len) - 1) * subtile_len
        return xouttile, youttile, xoffset, yoffset

    def _verify_subtile_keys(self):
        subtile_keys = map(lambda x: self._parse_key(x)[:2], self._sub_tiles.keys())
        assert len(self._sub_tiles) == _subtiles_per_tile
        for x in subtile_keys[1:]:
            assert subtile_keys[0] == x

    def reduce(self, key, values):
        """

        For this to work we need a modified partitioner on the substring before the first tab.
        This method operates on a single tile at level 0, and more tiles at higher zoom levels (4x each level).
        
        Args:
        key: (tile_id, subtile_id)
        values: Iterator of [dist, images] where images are power of 2 JPEG
            images in descending order by size

        Yields:
            Tuple of (key, value) where
            key: Tile name
            value: JPEG Image Data
        """
        # Select minimum distance image, throw away score, and order images from smallest to largest powers of 2
        self._sub_tiles[key] = min(values, key=lambda x: x[0])[1][::-1]
        # As the images were JPEG, we need to make them arrays again
        self._sub_tiles[key] = [imfeat.image_fromstring(x) for x in self._sub_tiles[key]]
        # If we don't have all of the necessary subtiles.
        if len(self._sub_tiles) != _subtiles_per_tile:
            return
        self._verify_subtile_keys()
        for level in range(_levels):
            # Each image is smaller than the tile
            scale = 2 ** level
            num_tiles = scale * scale
            subtiles_per_tile_len = _subtiles_per_tile_length / scale
            subtiles_per_tile = subtiles_per_tile_len ** 2
            subtile_len = _subtile_length * scale
            cur_subtiles = [(self._find_output(key, scale, subtiles_per_tile_len, subtile_len), images[level])
                         for key, images in self._sub_tiles.items()]
            cur_subtiles.sort(key=lambda x: x[0])
            cur_tile = np.zeros((_tile_length, _tile_length, 3), dtype=np.uint8)
            assert len(cur_subtiles) / subtiles_per_tile == num_tiles
            cur_outtile = None
            for subtile_ind, ((xouttile, youttile, xoffset, yoffset), image) in enumerate(cur_subtiles):
                if cur_outtile is None:
                    cur_outtile = (xouttile, youttile)
                assert cur_outtile == (xouttile, youttile)
                #cur_tile.paste(image, (xoffset, yoffset))  # TODO Suspect
                cur_tile[yoffset:yoffset + image.shape[0], xoffset:xoffset + image.shape[1], :] = image
                if not (subtile_ind + 1) % subtiles_per_tile:
                    tile_name = '%d_%d_%d.jpg' % (level, xouttile, youttile)
                    yield tile_name, imfeat.image_tostring(cur_tile, 'jpg')
                    cur_tile = np.zeros((_tile_length, _tile_length, 3), dtype=np.uint8)
                    cur_outtile = None
        self._sub_tiles = {}


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
