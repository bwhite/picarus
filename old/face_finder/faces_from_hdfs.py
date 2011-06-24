import hadoopy
import os
import Image
import cv
import cStringIO as StringIO

def pil2cv(pil_image):
    channels = 1 if pil_image.mode == 'L' else 3
    cv_im = cv.CreateImageHeader(pil_image.size, cv.IPL_DEPTH_8U, channels)
    cv.SetData(cv_im, pil_image.tostring())
    if channels == 3:
        cv_im_cvt = cv.CreateImage(pil_image.size, cv.IPL_DEPTH_8U, channels)
        cv.CvtColor(cv_im, cv_im_cvt, cv.CV_RGB2BGR)
        cv_im = cv_im_cvt
    return cv_im

def str2pil(image_data):
    return Image.open(StringIO.StringIO(image_data))

def cvcrop(cv_image, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    cropped = cv.CreateImage((w, h), 8, cv_image.channels)
    src_region = cv.GetSubRect(image, (x, y, w, h))
    cv.Copy(src_region, cropped)
    return cropped

#key: Image name
#value: (image, faces) where image is the input value and faces is
#       a list of ((x, y, w, h), n)
run_time = '1306607174.041919'
out_path = '/mnt/nfsdrives/shared/facefinder/run-%s/' % run_time
chip_out_path = '/mnt/nfsdrives/shared/facefinder/run-%s/chips' % run_time
os.makedirs(chip_out_path)
for image_name, (image, faces) in hadoopy.cat('/user/brandyn/tp/facefinder/run-%s' % run_time):
    image = pil2cv(str2pil(image))
    for num, ((x, y, w, h), n) in enumerate(faces):
        cv.SaveImage('%s/%s-%d.jpg' % (chip_out_path, image_name, num), cvcrop(image, x, y, w, h))
    for (x, y, w, h), n in faces:
        pt1 = (int(x), int(y))
        pt2 = (int((x + w)), int((y + h)))
        cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
    cv.SaveImage('%s/%s.jpg' % (out_path, image_name), image)
