import os

import fabio

from ... import Operation as opmod 
from ...Operation import Operation

class FabIOOpen(Operation):
    """
    Takes a filesystem path and calls fabIO to load it. 
    """

    def __init__(self):
        input_names = ['path']
        output_names = ['image_data','FabioImage','dir_path','filename']
        super(FabIOOpen,self).__init__(input_names,output_names) 
        self.input_doc['path'] = 'string representing the path to a .tif image'
        self.output_doc['image_data'] = '2D array representing pixel values taken from the input file'
        self.output_doc['FabioImage'] = 'The object generated by fabio.open()'
        self.output_doc['dir_path'] = 'Path to the directory the image came from'
        self.output_doc['filename'] = 'The image filename, no path, no extension'
        
    def run(self):
        """
        Call on fabIO to extract image data
        """
        p = self.inputs['path']
        dir_path = os.path.split(p)[0]
        file_nopath = os.path.split(p)[1]
        file_noext = os.path.splitext(file_nopath)[0]
        self.outputs['dir_path'] = dir_path 
        self.outputs['filename'] = file_noext 
        self.outputs['image_data'] = fabio.open(p).data

