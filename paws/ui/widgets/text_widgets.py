"""Widgets for displaying text"""

from ...core.operations import optools 
from ...core.operations.Operation import Operation
from ...core.pawstools import FileSystemIterator

unit_indent='&nbsp;&nbsp;&nbsp;&nbsp;'

def display_text(itm,indent=unit_indent):
    if type(itm).__name__ in ['str','unicode']:
        t = '(str) <br>' + indent + '{}'.format(itm)
    elif isinstance(itm,dict):
        t = '(dict)'
        for k,v in itm.items():
            t += '<br>' + indent + '{}: {}'.format(k,display_text(v,indent+unit_indent))
    elif isinstance(itm,list):
        t = '(list)'
        for i in range(len(itm)):
            t += '<br>' + indent + '{}: {}'.format(i,display_text(itm[i],indent+unit_indent))
    elif isinstance(itm,optools.InputLocator):
        t = '(InputLocator)'
        t += '<br>' + indent + 'src: {}'.format(optools.input_sources[itm.src])
        t += '<br>' + indent + 'type: {}'.format(optools.input_types[itm.tp])
        t += '<br>' + indent + 'val: {}'.format(itm.val)
        t += '<br>' + indent + 'data: {}'.format(type(itm.data).__name__)
    elif isinstance(itm,FileSystemIterator):
        t = '(FileSystemIterator)'
        for ip,p in zip(range(len(itm.paths_done)),itm.paths_done):
            t += '<br>' + indent + '{}: {}'.format(ip,p)
    else:
        t = '('+type(itm).__name__+')' + '<br>' + indent + '{}'.format(itm)
    return t
    
def display_text_fast(itm,indent=unit_indent):
    # TODO: Make ndarrays display truncated but without importing numpy?
    if type(itm).__name__ in ['str','unicode']:
        t = '(str) <br>' + indent + '{}'.format(itm)
    elif isinstance(itm,dict):
        t = '(dict)'
        if len(itm) > 4:
            suffix = '<br>'+indent+'ETC ...'
            ndisp = 4
        else:
            suffix = ''
            ndisp = len(itm)
        for k,v in itm.items()[:ndisp]:
            t += '<br>' + indent + '{}: {}'.format(k,display_text_fast(v,indent+unit_indent))
        t += suffix 
    elif isinstance(itm,list):
        t = '(list)'
        if len(itm) > 4:
            suffix = '<br>'+indent+'ETC ...'
            ndisp = 4
        else:
            suffix = ''
            ndisp = len(itm)
        for i in range(len(itm))[:ndisp]:
            t += '<br>' + indent + '{}: {}'.format(i,display_text_fast(itm[i],indent+unit_indent))
        t += suffix 
    elif isinstance(itm,optools.InputLocator):
        t = '(InputLocator)'
        t += '<br>' + indent + 'src: {}'.format(optools.input_sources[itm.src])
        t += '<br>' + indent + 'type: {}'.format(optools.input_types[itm.tp])
        t += '<br>' + indent + 'val: {}'.format(itm.val)
        t += '<br>' + indent + 'data: {}'.format(type(itm.data).__name__)
    elif isinstance(itm,FileSystemIterator):
        t = '(FileSystemIterator)'
        for ip,p in zip(range(len(itm.paths_done)),itm.paths_done):
            t += '<br>' + indent + '{}: {}'.format(ip,p)
    else:
        t = '('+type(itm).__name__+')' + '<br>' + indent + '{}'.format(itm)
    return t
    

