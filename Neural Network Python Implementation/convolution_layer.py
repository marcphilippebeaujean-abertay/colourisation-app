import numpy as np
from network_layer import NetworkLayer
from utils import Stride, Filter
from scipy.stats import truncnorm


class ConvLayer(NetworkLayer):
    def __init__(self,
                 filter_depth,
                 filter_width,
                 filter_height,
                 stride_horizontal,
                 stride_vertical,
                 input_width,
                 input_height,
                 kernel_size,
                 output_function):
        self.stride = Stride(stride_horizontal,
                             stride_vertical)
        self.filter = Filter(filter_height,
                             filter_width,
                             filter_depth)
        output_dim = (
            (input_height - filter_height) / stride_vertical + 1,
            (input_width - filter_width) / stride_horizontal + 1,
            filter_depth)
        super().__init__(output_dim, (input_width, input_height))
        self.kernel = kernel_size
        self.filters = np.zeros((input_width,
                                 input_height,
                                 filter_depth))
        # initialise values from normal distribution for faster convergence
        self.filters = np.random.normal(0.5, 0.25, self.filters.shape)
        self.output_function = output_function

    def input_pass(self, input):
        output = np.zeros(self.output_dim)
        for filt in self.filter.filter_depth



ConvLayer(1,
          (2, 2),
          (32, 32),
          (3, 3))