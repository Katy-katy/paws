from collections import OrderedDict
import glob
import os

from ...Operation import Operation
from ... import Operation as opmod 
from ... import optools

class BatchFromDirectory(Operation):
    """
    Read a directory and filter its contents with a regular expression
    to form  a list of file paths to be used as inputs
    for the repeated execution of a specified Workflow.
    Specify, by workflow uri, where this file path will be fed to the workflow.
    Collect outputs from the Workflow for each of the input files.
    """

    def __init__(self):
        input_names = ['dir_path','regex','workflow','input_name']
        output_names = ['batch_inputs','batch_outputs']
        super(BatchFromDirectory,self).__init__(input_names,output_names)
        self.input_doc['dir_path'] = 'path to directory containing batch of files to be used as input'
        self.input_doc['regex'] = 'string with * wildcards that will be substituted to indicate input files'
        self.input_doc['workflow'] = 'the Workflow to be executed'
        self.input_doc['input_name'] = 'name of the workflow input where the file paths will be used'
        self.output_doc['batch_inputs'] = 'list of dicts of [input_name:input_value]'
        self.output_doc['batch_outputs'] = 'list of dicts of [output_name:output_value] for all Workflow outputs'
        self.input_type['workflow'] = opmod.entire_workflow
        self.inputs['regex'] = '*.tif' 
        
    def run(self):
        wf = self.inputs['workflow']
        dirpath = self.inputs['dir_path']
        rx = self.inputs['regex']
        inpname = self.inputs['input_name']
        batch_list = glob.glob(os.path.join(dirpath,rx))
        input_dict_list = []
        output_dict_list = []
        n_batch = len(batch_list)
        wf.write_log('STARTING BATCH')
        for i,filename in zip(range(n_batch),batch_list):
            inp_dict = OrderedDict() 
            inp_dict[inpname] = filename
            wf.set_wf_input(inpname,filename)
            wf.write_log('BATCH RUN {} / {}'.format(i+1,n_batch))
            wf.execute()
            input_dict_list.append(inp_dict)
            output_dict_list.append(wf.wf_outputs_dict())
        wf.write_log('BATCH FINISHED')
        self.outputs['batch_inputs'] = input_dict_list
        self.outputs['batch_outputs'] = output_dict_list 

