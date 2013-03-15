#include "ImagePreprocessor.hpp"
#include <opencv2/opencv.hpp>
#include <iostream>

ImagePreprocessor::ImagePreprocessor(std::string method, int size, std::string compression) : method(method), size(size), compression(compression) {
    if (!method.compare("max_side")) {
        this->method_code = 0;
    } else if (!method.compare("force_max_side")) {
        this->method_code = 1;
    } else if (!method.compare("force_square")) {
        this->method_code = 2;
    } else {
        this->method_code = 255; // "original"  Don't change the size
    }
}


ImagePreprocessor::~ImagePreprocessor() {
}

std::vector<char> ImagePreprocessor::asbinary(std::vector<char> binary_image) {
    int height, width, channels;
    //std::vector<unsigned char> asarray(binary_image, &height, &width, &channels);
    //cv::imencode();
    //bool imencode(const string& ext, InputArray img, vector<uchar>& buf, const vector<int>& params=vector<int>())
    // TODO: Convert
}



std::vector<unsigned char> ImagePreprocessor::asarray(std::vector<char> binary_image, int *height, int *width, int *channels) {
    cv::Mat image = cv::imdecode(binary_image, CV_LOAD_IMAGE_COLOR);
    const int orig_height = image.rows, orig_width = image.cols;
    int new_height = orig_height, new_width = orig_width;
    switch (this->method_code) {
    case 0: // max_side
        if (orig_height <= this->size && orig_width <= this->size)
            break;
    case 1: // force_max_side
        if (orig_height >= orig_width) {
            new_height = this->size;
            new_width = this->size * (double)orig_width / orig_height + .5;
        } else {
            new_width = this->size;
            new_height = this->size * (double)orig_height / orig_width + .5;
        }
        break;
    case 2: // force_square
        new_height = new_width = this->size;
        break;
    default:
        break;
    }
    if (orig_width != new_width || orig_height != new_height) {
        int interpolation = CV_INTER_LINEAR;
        if ((double)new_width / orig_width < .5 || (double)new_height / orig_height < .5)
            interpolation = CV_INTER_AREA;
        std::cout << "NewHeight " << new_height << " NewWidth " << new_width << std::endl;
        cv::resize(image, image, cv::Size(new_width, new_height), interpolation);
    }
    const unsigned char *p = image.ptr<unsigned char>(0);
    std::vector<unsigned char> vec(p, p  + image.cols * image.rows * image.channels());
    *height = image.rows;
    *width = image.cols;
    *channels = image.channels();
    return vec;
}
