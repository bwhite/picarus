#ifndef IMAGE_FEATURE
#define IMAGE_FEATURE
#include <vector>

class ImageFeature {
public:
    ImageFeature();
    ~ImageFeature();
    virtual double* compute_feature(unsigned char *image, int height, int width, int *out_size) = 0;
protected:
    double *pyramid_histogram(unsigned int *label_image, int height, int width, int max_val, int levels, int *out_size);
};
#endif
