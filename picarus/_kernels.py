import kernels


def compute(kernel_name, x, y):
    if kernel_name == 'hik':
        return kernels.histogram_intersection(x, y)
    elif kernel_name == 'linear':
        return kernels.linear(x, y)
    elif kernel_name == 'chi2':
        return kernels.chi_square(x, y)
    else:
        raise ValueError(kernel_name)
