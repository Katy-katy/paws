import abc
import re
from collections import OrderedDict

import optools

class Operation(object):
    __metaclass__ = abc.ABCMeta
    """
    Abstract class template for implementing slacx operations.
    """

    def __init__(self,input_names,output_names):
        """
        The input_names and output_names (lists of strings)
        are used to specify names for the parameters 
        that will be used to perform the operation.
        When loading the operation into the workspace,
        each name in input_names becomes a variable 
        which must be assigned some value.
        Meanwhile, the output_names specification is used to build
        workflow connections with results that are not yet computed.
        The categories attribute is a list that indicates
        where the operation can be found in the OpManager tree.
        The Operation will be listed under each category in the list.
        Subcategories are indicated by a ".", for example:
        self.categories = ['CAT1','CAT2.SUBCAT','CAT3']
        """
        self.inputs = OrderedDict()
        self.input_src = {}
        self.input_type = {}
        self.input_doc = {}
        self.input_locator = {}
        self.outputs = OrderedDict() 
        self.output_doc = {}
        # For each of the var names, assign to None 
        for name in input_names: 
            self.input_src[name] = optools.no_input
            self.input_type[name] = optools.none_type
            self.inputs[name] = None
            self.input_doc[name] = None
            self.input_locator[name] = None
        for name in output_names: 
            self.outputs[name] = None
            self.output_doc[name] = None
        # Set default category to be 'MISC'
        self.categories = ['MISC']


    @abc.abstractmethod
    def run(self):
        """
        Operation.run() should use all of the items in Operation.inputs
        and set values for all of the items in Operation.outputs.
        """
        pass

    def description(self):
        """
        self.description() returns a string 
        documenting the input and output structure 
        and usage instructions for the Operation
        """
        return str(
        "Operation description: "
        + self.doc_as_string()
        + "\n\n--- Input ---"
        + self.input_description() 
        + "\n\n--- Output ---"
        + self.output_description())

    def doc_as_string(self):
        if self.__doc__:
            return re.sub("\s\s+"," ",self.__doc__.replace('\n','')) 
        else:
            return "no documentation found"

    def input_description(self):
        a = ""
        inp_indx = 0
        for name,val in self.inputs.items(): 
            if self.input_locator[name]:
                display_val = self.input_locator[name].val
            else:
                display_val = val 
            a = a + str("\n\nInput {}:\n".format(inp_indx) 
            + optools.parameter_doc(name,display_val,self.input_doc[name]))
            inp_indx += 1
        return a

    def output_description(self):
        a = ""
        out_indx = 0
        for name,val in self.outputs.items(): 
            a = a + str("\n\nOutput {}:\n".format(out_indx) 
            + optools.parameter_doc(name,val,self.output_doc[name]))
            out_indx += 1
        return a
                
    def set_outputs_to_none(self):
        for name,val in self.outputs.items(): 
            self.outputs[name] = None


class Batch(Operation):
    __metaclass__ = abc.ABCMeta
    """
    Abstract class template for implementing batch execution operations.
    """
    def __init__(self,input_names,output_names):
        super(Batch,self).__init__(input_names,output_names)

    @abc.abstractmethod
    def output_list(self):
        """
        Produce an ordered list of dicts representing the outputs for each batch input.
        Each dict should be populated with [input_uri:input_value] pairs.
        """
        pass
    @abc.abstractmethod
    def input_list(self):
        """
        Produce an ordered list of dicts representing each set of inputs for the Batch to run.
        Each dict should be populated with [input_uri:input_value] pairs.
        """
        pass

    def set_input_at_uri(self,uri,val):
        """
        Set an item in self.inputs, indicated by uri, to the value indicated by val.
        """
        path = uri.split('.')
        # assume path[0] is this operation's TreeItem tag().
        try:
            if not path[1] == 'Inputs':
                msg = 'path {} does not point to operation inputs'.format(uri)
                raise ValueError(msg)
            elif not path[2] in self.input_names:
                msg = 'path {} specifies a non-existent operation input field'.format(uri)
                raise ValueError(msg)
            else:
                self.inputs[name] = val
        except Exception as ex:
            msg = '-----\nbad path: {}\n-----'.format(path)
            raise ex(msg+ex.message)


