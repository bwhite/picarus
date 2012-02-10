import kernels


def compute(kernel_name, x, y):
    if kernel_name == 'hik':
        return kernels.histogram_intersection(x, y)
    else:
        raise ValueError(kernel_name)
