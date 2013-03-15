#include "ImageFeature.hpp"
#include "bovw_aux.h"

ImageFeature::ImageFeature() {
}
ImageFeature::~ImageFeature() {
}

static int buckets_per_side(int level) {
    return 1 << level;
}

static int bins_per_level(int level, int max_val) {
    int b = buckets_per_side(level);
    return b * b * max_val;
}

static void normalize_histogram(unsigned int *hist, double *hist_norm, int start, int stop, double scale) {
    double normalize_sum = 0.;
    for (int i = start; i < stop; ++i)
        normalize_sum += hist[i];
    for (int i = start; i < stop; ++i)
        hist_norm[i] = (hist[i] / normalize_sum) * scale;           
}

double *ImageFeature::pyramid_histogram(unsigned int *label_image, int height, int width, int max_val, int levels, int *out_size) {
    int num_bins = 0;
    for (int i = 0; i < levels; ++i)
        num_bins += bins_per_level(i, max_val);
    unsigned int *out = new unsigned int[num_bins];
    double *out_norm = new double[num_bins];
    *out_size = num_bins;
    bovw_fast_hist(label_image, &out[0], height, width, max_val, levels - 1);
    int offset = 0;
    for (int i = 0; i < levels - 1; ++i) {
        int coarse_offset = offset + bins_per_level(levels - i - 1, max_val);
        double scale = 1 << (levels - i);
        normalize_histogram(out, out_norm, offset, coarse_offset, scale);
        bovw_fast_sum(out + offset, out + coarse_offset, buckets_per_side(levels - i - 1), buckets_per_side(levels - i - 1), max_val);
        offset = coarse_offset;
    }
    normalize_histogram(out, out_norm, offset, num_bins, 1.);
    delete [] out;
    return out_norm;
}
