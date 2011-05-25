import hadoopy
import imfeat
import Image
import cStringIO as StringIO


def mapper(name, image_data):
    image = Image.open(StringIO.StringIO(image_data))
    feat = imfeat.Histogram('rgb', style='planar')
    yield name, imfeat.compute(feat, image)[0]


if __name__ == '__main__':
    hadoopy.run(mapper)
