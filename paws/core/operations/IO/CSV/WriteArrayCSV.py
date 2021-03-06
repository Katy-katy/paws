from os.path import splitext
from os import linesep
import numpy as np

from ... import Operation as opmod 
from ...Operation import Operation

class WriteArrayCSV(Operation):
    """Write a 2d array to a csv file"""

    def __init__(self):
        input_names = ['array','headers','dir_path','filename','filetag']
        output_names = ['file_path']
        super(WriteArrayCSV, self).__init__(input_names, output_names)
        self.input_doc['array'] = 'any 2d array'
        self.input_doc['headers'] = 'list of string headers (optional)- one header for each column of array'
        self.input_doc['dir_path'] = 'the path to the destination directory'
        self.input_doc['filename'] = 'the name of the file to be saved- no extension is expected'
        self.input_doc['filetag'] = 'tag appended to filename- no extension is expected'
        self.output_doc['file_path'] = 'the path to the finished csv file: dir_path+filename+filetag+.csv'
        self.input_type['array'] = opmod.workflow_item
        self.inputs['filetag'] = ''

    def run(self):
        #import pdb; pdb.set_trace()
        h = self.inputs['headers']
        a = self.inputs['array']
        tag = ''
        if self.inputs['filetag']:
            tag = self.inputs['filetag']
        csv_path = self.inputs['dir_path']+'/'+self.inputs['filename']+tag+'.csv'
        self.outputs['file_path'] = csv_path
        if h is not None:
            h_str = ''
            for i in range(len(h)-1):
                h_str += h[i] + ', '
            h_str = h_str+h[-1]
            np.savetxt(csv_path, a, delimiter=',', newline=linesep, header=h_str)
        else:
            np.savetxt(csv_path, a, delimiter=',', newline=linesep)

