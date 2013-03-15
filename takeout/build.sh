rm *.o main pyramid_histogram_sanity_test picarus_takeout
#PARAMS="-pg -Wall -Wextra -g"
PARAMS="-Wall -Wextra -g -DUSE_BLAS -lblas"
g++ -o picarus_takeout picarus_takeout.cpp cJSON.c  ImagePreprocessor.cpp HistogramImageFeature.cpp ImageFeature.cpp picarus_math.c LinearClassifier.cpp pyramid_histogram_aux.c bovw_aux.c -l opencv_highgui -l opencv_core -l opencv_imgproc ${PARAMS}
#g++ -o main main.cpp features.cc HistogramMask.cpp bovw_aux.c pyramid_histogram_aux.c ImagePreprocessor.cpp -l opencv_highgui -l opencv_core -l opencv_imgproc ${PARAMS}

#g++ -o pyramid_histogram_sanity_test pyramid_histogram_sanity_test.cpp features.cc HistogramMask.cpp bovw_aux.c pyramid_histogram_aux.c ImagePreprocessor.cpp -Wall -Wextra -l opencv_highgui -l opencv_core -l opencv_imgproc -g
