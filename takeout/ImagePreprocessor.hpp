#ifndef IMAGE_PREPROCESSOR
#define IMAGE_PREPROCESSOR
#include <string>
#include <vector>

class ImagePreprocessor {
private:
    const std::string method, compression;
    const int size;
    int method_code;
public:
    ImagePreprocessor(std::string method, int size, std::string compression);
    ~ImagePreprocessor();
    std::vector<char> asbinary(std::vector<char> binary_image);
    std::vector<unsigned char> asarray(std::vector<char> binary_image, int *height, int *width, int *channels);
};
#endif
