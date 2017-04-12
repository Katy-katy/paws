import numpy as np

from ..Operation import Operation
from .. import optools

class Zip(Operation):
    """
    Zip two 1d arrays together.
    """

    def __init__(self):
        input_names = ['x', 'y']
        output_names = ['x_y']
        super(Zip, self).__init__(input_names, output_names)
        self.input_doc['x'] = '1d array'
        self.input_doc['y'] = '1d array, same size as x'
        self.output_doc['x_y'] = 'n x 2 array containing x and y'
        # source & type
        self.input_src['x'] = optools.wf_input
        self.input_src['y'] = optools.wf_input
        self.input_type['x'] = optools.ref_type
        self.input_type['y'] = optools.ref_type

    def run(self):
        x = self.inputs['x']
        y = self.inputs['y']
        if (x.shape != y.shape):
            raise ValueError("x and y must have the same shape")
        xy = np.array(zip(x, y))
        self.outputs['x_y'] = xy

