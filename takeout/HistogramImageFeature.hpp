#ifndef HISTOGRAM_IMAGE_FEATURE
#define HISTOGRAM_IMAGE_FEATURE
#include <string>
#include <vector>
#include "ImageFeature.hpp"


class HistogramImageFeature: public ImageFeature {
private:
    std::string mode;
    std::vector<int> num_bins;
    int levels;
    int code;
    int skip_cvt_color;
    float min_vals[3];
    float max_vals[3];
public:
    HistogramImageFeature(std::string mode, std::vector<int> num_bins, int levels);
    ~HistogramImageFeature();
    double *compute_feature(unsigned char *image, int height, int width, int *out_size);
protected:
    void color_mode_to_code();
    float *convert_color(unsigned char *image, int height, int width);
    unsigned int *histogram_label_image(unsigned char *image, int height, int width, int *out_max_val);
    
};
#endif
