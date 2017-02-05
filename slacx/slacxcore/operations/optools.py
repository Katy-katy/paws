from collections import OrderedDict

from PySide import QtCore

import slacxop

##### TODO: the following but gracefully 
# definitions for operation input sources 
no_input = 0
user_input = 1
fs_input = 2
wf_input = 3
plugin_input = 4
batch_input = 5 
valid_sources = [no_input,user_input,fs_input,wf_input,plugin_input,batch_input]
input_sources = ['None','User Input','Filesystem','Workflow','Plugins','Batch'] 

# supported types for operation inputs
none_type = 0
auto_type = 1
str_type = 2
int_type = 3
float_type = 4
bool_type = 5
list_type = 6
valid_types = [none_type,auto_type,str_type,int_type,float_type,bool_type,list_type]
input_types = ['none','auto','string','integer','float','boolean','list']

# unsupported types for each source, keyed by source
invalid_types = {}                
invalid_types[no_input] = [auto_type,str_type,int_type,float_type,bool_type,list_type]
invalid_types[user_input] = [auto_type]
invalid_types[fs_input] = [auto_type,int_type,float_type,bool_type]
invalid_types[wf_input] = [int_type,float_type,bool_type]
invalid_types[plugin_input] = [str_type,int_type,float_type,bool_type]
invalid_types[batch_input] = [str_type,int_type,float_type,bool_type,list_type]

# tags and indices for inputs and outputs trees
inputs_tag = 'inputs'
outputs_tag = 'outputs'
inputs_idx = 0
outputs_idx = 1

def cast_type_val(tp,val):
    """
    Perform type casting for operation inputs.
    This should be called for source user_input,
    and should not be called for type auto_type.
    """
    if tp == none_type:
        val = None 
    elif tp == int_type:
        val = int(val)
    elif tp == float_type:
        val = float(val)
    elif tp == str_type:
        val = str(val)
    elif tp == bool_type:
        val = bool(eval(str(val)))
    elif tp == list_type:
        # val will be a list of strings, should be typecast on loading or by the list builder 
        val = list(val)
    else:
        msg = 'type selection {}, should be one of {}'.format(tp,valid_types)
        raise ValueError(msg)
    return val

def val_list(il):
    if il.tp == list_type:
        return il.val
    else:
        return [il.val]

def parse_plugin_input(plugman,il,op):
    itm, indx = plugman.get_from_uri(il.val)
    return itm.data

def parse_wf_input(wfman,il,op):
    """
    Input types supported for workflow source:
    optools.none_type: trivial case, return None
    optools.str_type: this input is assumed to be used as a key,
        used for fetching workflow output data for further processing
        It should be returned as is.
    optools.list_type: The listed inputs by val_list(il) are all treated as str_type
    optools.auto_type: Attempt to use il.val as a uri to fetch data 
        from the input workflow manager wfman
    """
    if il.tp == none_type:
        return None
    elif il.tp == str_type:
        return str(il.val)
    elif il.tp == list_type:
        return [str(val) for val in val_list(il)]
    elif il.tp == auto_type:
        itm, indx = wfman.get_from_uri(il.val)
        #TODO: fix the following hack
        # If this points to an input, an InputLocator will be returned.
        # Fetch its data.
        if isinstance(itm.data,InputLocator):
            return itm.data.data
        else:
            # itm.data should be actual data.
            return itm.data
    #uris = val_list(il)
    #rets = []
    #for uri in uris:
    #    uri_parts = uri.split('.')
        #if len(uri_parts) >= 3:
        #    io_type = uri_parts[1]
        #    if io_type == inputs_tag:
        #        input_route_flag = False
        #        if isinstance(op,slacxop.Batch) or isinstance(op,slacxop.Realtime):
        #            input_route_flag = uri in op.input_routes()
        #        if input_route_flag:
        #            rets.append(uri)
        #        else:
        #            itm, idx = wfman.get_from_uri(uri)
        #            il = itm.data 
        #            rets.append(il.data)
        #    else:
        #        itm, idx = wfman.get_from_uri(uri)
        #        rets.append(itm.data)
        #else:
        #    itm, indx = wfman.get_from_uri(uri)
        #    rets.append(itm.data)
    #if il.tp == list_type:
    #    return rets
    #else:
    #    return rets[0]

def op_dict(op):
    dct = OrderedDict() 
    dct['type'] = type(op).__name__ 
    dct[inputs_tag] = op_inputs_dict(op)
    return dct

def op_inputs_dict(op):
    dct = OrderedDict() 
    for name in op.inputs.keys():
        il = op.input_locator[name]
        dct[name] = {'src':il.src,'type':il.tp,'val':il.val}
    return dct

def plugin_dict(pgin):
    dct = OrderedDict()
    dct['type'] = type(pgin).__name__
    dct[inputs_tag] = pgin.inputs 
    return dct

#def outputs_dict(self,op):
#    #dct = {}
#    dct = OrderedDict() 
#    for name in op.outputs.keys():
#        dct[name] = str(op.outputs[name])
#    return dct

class InputLocator(object):
    """
    Objects of this class are used as containers for inputs to an Operation,
    and should by design contain the information needed to find the relevant input data.
    After the data is loaded, it should be stored in InputLocator.data.
    """
    def __init__(self,src=no_input,tp=none_type,val=None):
        #if src not in valid_sources: 
        #    msg = 'found input source {}, should be one of {}'.format(src, valid_sources)
        self.src = src
        self.tp = tp
        self.val = val 
        self.data = None 

def parameter_doc(name,value,doc):
    #if type(value).__name__ == 'InputLocator':
    if isinstance(value, InputLocator):
        src_str = input_sources[value.src]
        tp_str = input_types[value.tp]
        d = value.data
        return "- name: {} \n- source: {} \n- type: {} \n- value: {} \n- doc: {}".format(name,src_str,tp_str,d,doc) 
    else:
        val_str = str(value)
        tp_str = type(value).__name__
        return "- name: {} \n- type: {} \n- value: {} \n- doc: {}".format(name,tp_str,val_str,doc) 

#def loader_extensions():
#    return str(
#    "ALL (*.*);;"
#    + "TIFF (*.tif *.tiff);;"
#    + "RAW (*.raw);;"
#    + "MAR (*.mar*)"
#    )

