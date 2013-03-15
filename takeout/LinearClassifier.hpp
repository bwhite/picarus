#ifndef LINEAR_CLASSIFIER
#define LINEAR_CLASSIFIER
#include <vector>

class LinearClassifier {
private:
    std::vector<double> coefficients;
    double intercept;
public:
    LinearClassifier(std::vector<double> coefficients, double intercept);
    ~LinearClassifier();
    double decision_function(double *feature, int size);
};

#endif
