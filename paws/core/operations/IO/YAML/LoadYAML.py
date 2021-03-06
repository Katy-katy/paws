import numpy as np

import yaml
from ... import Operation as opmod 
from ...Operation import Operation

class LoadYAML(Operation):
    """
    Read a YAML file containing population flags for saxs data. 
    """

    def __init__(self):
        input_names = ['file_path']
        output_names = ['yaml_output']
        super(LoadYAML, self).__init__(input_names, output_names)
        self.input_doc['file_path'] = 'path to YAML-formatted data file'
        self.output_doc['yaml_output'] = 'the result of yaml.load(file_path)' 

    def run(self):
        p = self.inputs['file_path']
        f = open(p,'r')
        ds = yaml.load(f)
        f.close()
        self.outputs['yaml_output'] = ds 


