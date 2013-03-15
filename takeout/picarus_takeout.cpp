#include <cstdio>
#include <cstdlib>
#include "cJSON.h"
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <streambuf>
#include <cstring>
#include "ImagePreprocessor.hpp"
#include "HistogramImageFeature.hpp"
#include "LinearClassifier.hpp"

/*
  Operating Modes:
  
  JSON Config, STDIN/STDOUT JSON
  Provide a command line argument to the JSON config

  
  Functions Needed:
  picarus_takeout_factory(JSON): Instantiate first module, read data from STDIN

 */


void read_file(const char *fn, std::string *str) {
    std::ifstream t(fn);
    t.seekg(0, std::ios::end);   
    str->reserve(t.tellg());
    t.seekg(0, std::ios::beg);
    str->assign((std::istreambuf_iterator<char>(t)),
                std::istreambuf_iterator<char>());
}

void read_file(const char *fn, std::vector<char> *str) {
    std::ifstream t(fn);
    t.seekg(0, std::ios::end);   
    str->reserve(t.tellg());
    t.seekg(0, std::ios::beg);
    str->assign((std::istreambuf_iterator<char>(t)),
                std::istreambuf_iterator<char>());
}


ImagePreprocessor* picarus_image_preprocessor_factory(cJSON *cjs) {
    cJSON *kw = cJSON_GetObjectItem(cjs, "kw");
    cJSON *val;

    val = cJSON_GetObjectItem(kw, "method");
    if (!val || val->type != cJSON_String)
        return NULL;
    std::string method(val->valuestring);
    
    val = cJSON_GetObjectItem(kw, "compression");
    if (!val || val->type != cJSON_String)
        return NULL;
    std::string compression(val->valuestring);

    val = cJSON_GetObjectItem(kw, "size");
    if (!val || val->type != cJSON_Number)
        return NULL;
    int size = val->valueint;
    return new ImagePreprocessor(method, size, compression);
}


HistogramImageFeature* picarus_histogram_image_feature_factory(cJSON *cjs) {
    cJSON *kw = cJSON_GetObjectItem(cjs, "kw");
    cJSON *val;

    val = cJSON_GetObjectItem(kw, "mode");
    if (!val || val->type != cJSON_String)
        return NULL;
    std::string mode(val->valuestring);
    
    val = cJSON_GetObjectItem(kw, "levels");
    if (!val || val->type != cJSON_Number)
        return NULL;
    int levels = val->valueint;

    val = cJSON_GetObjectItem(kw, "num_bins"); // 3 ints
    if (!val || val->type != cJSON_Array || cJSON_GetArraySize(val) != 3)
        return NULL;
    std::vector<int> num_bins(3);
    for (int i = 0; i < 3; ++i) {
        cJSON *array_val = cJSON_GetArrayItem(val, i);
        if (!array_val || array_val->type != cJSON_Number)
            return NULL;
        num_bins[i] = array_val->valueint;
    }
    return new HistogramImageFeature(mode, num_bins, levels);
}

LinearClassifier* picarus_linear_classifier_factory(cJSON *cjs) {
    cJSON *kw = cJSON_GetObjectItem(cjs, "kw");
    cJSON *val;
    
    val = cJSON_GetObjectItem(kw, "intercept");
    if (!val || val->type != cJSON_Number)
        return NULL;
    int intercept = val->valuedouble;

    val = cJSON_GetObjectItem(kw, "coefficients");
    if (!val || val->type != cJSON_Array)
        return NULL;
    int num_coefficients = cJSON_GetArraySize(val);
    std::vector<double> coefficients(num_coefficients);
    for (int i = 0; i < num_coefficients; ++i) {
        cJSON *array_val = cJSON_GetArrayItem(val, i);
        if (!array_val || array_val->type != cJSON_Number)
            return NULL;
        coefficients[i] = array_val->valuedouble;
    }
    return new LinearClassifier(coefficients, intercept);
}


int main(int argc, char **argv) {
    if (argc != 3) {
        std::cout << argc << std::endl;
        std::cerr << "Usage: " << argv[0] << " <config_json_path> <input_path>" << std::endl;
        return 1;
    }
    std::string json_config;
    read_file(argv[1], &json_config);
    std::vector<char> input_data;
    read_file(argv[2], &input_data);
    cJSON *cjs = cJSON_Parse(json_config.c_str());
    cJSON *name = cJSON_GetObjectItem(cjs, "name");

    if (name && strcmp("picarus.ImagePreprocessor", name->valuestring) == 0) {
        ImagePreprocessor* ip = picarus_image_preprocessor_factory(cjs);
        int width, height, channels;
        ip->asarray(input_data, &height, &width, &channels);
        std::cout << "Height: " << height << " Width: " << width << " Channels: " << channels << std::endl;
        delete ip;
    } else if (name && strcmp("picarus.HistogramImageFeature", name->valuestring) == 0) {
        HistogramImageFeature* hif = picarus_histogram_image_feature_factory(cjs);
        delete hif;
    } else if (name && strcmp("picarus.LinearClassifier", name->valuestring) == 0) {
        double val[] = {3., 4.};
        LinearClassifier* lc = picarus_linear_classifier_factory(cjs);
        std::cout << "Val:" << lc->decision_function(val, 2) << std::endl;
        delete lc;
    }

    cJSON_Delete(cjs);
    return 0;
}
