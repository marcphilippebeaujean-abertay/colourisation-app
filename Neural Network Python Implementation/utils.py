from collections import namedtuple


Stride = namedtuple('Stride',
                    ['stride_horizontal',
                     'stride_vertical'])
Filter = namedtuple('Filter',
                    ['filter_height',
                     'filter_width',
                     'filter_depth'])
