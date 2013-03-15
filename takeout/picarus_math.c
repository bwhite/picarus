#include "picarus_math.h"

#ifdef USE_BLAS
#include <cblas.h>
double dot_product(double *v0, double *v1, int size) {
    return cblas_ddot(size, v0, 1, v1, 1);
}
/*double ddot_(const int *N, const double *a, const int *inca, const double *b, const int *incb);
double dot_product(double *v0, double *v1, int size) {
    int inc = 1;
    return ddot_(&size, v0, &inc, v1, &inc);
    }*/
#else
double dot_product(double *v0, double *v1, int size) {
    double out = 0.;
    int i;
    for (i = 0; i < size; ++i)
        out += v0[i] * v1[i];
    return out;
}
#endif
