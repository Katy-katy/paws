import os
import pkgutil
import importlib

import yaml

from operation import Operation
from .. import pawstools

def save_cfg(cfg_data,cfg_file):
    cfg = open(cfg_file,'w')
    yaml.dump(cfg_data,cfg)
    cfg.close()

def load_cfg(cfg_file):
    cfg = open(cfg_file,'r')
    cfg_data = yaml.load(cfg)
    cfg.close()
    if not cfg_data:
        cfg_data = {}
    return cfg_data

# check for an ops.cfg file
cfg_file = pawstools.rootdir+'/core/operations/ops.cfg'
if os.path.exists(cfg_file):
    op_load_flags = load_cfg(cfg_file)
else:
    op_load_flags = {}

# list to keep track of keys that get loaded in this run
# these keys are later used to maintain a lean, sane cfg file
op_load_keys = []

def load_ops_from_path(path_,pkg,cat_root='MISC'):
    ops = []
    cats = []
    # pkgutil.iter_modules returns module_loader, module_name, ispkg forall modules in path
    mods = pkgutil.iter_modules(path_)
    mods = [mod for mod in mods if mod[1] not in ['__init__','operation','op_manager','optools','DMZ']]
    for modloader, modname, ispkg in mods:
        if modname in op_load_flags.keys():
            if op_load_flags[modname]:
                load_mod = True
            else:
                load_mod = False 
        else:
            mod = importlib.import_module('.'+modname,pkg)
            load_mod = True
        # if it is a package, recurse
        if load_mod and ispkg:
            pkg_path = [path_[0]+'/'+modname]
            if cat_root == 'MISC':
                pkg_cat_root = modname 
            else:
                pkg_cat_root = cat_root+'.'+modname
            pkg_ops, pkg_cats = load_ops_from_path(pkg_path,pkg+'.'+modname,pkg_cat_root)
            pkg_ops = [op for op in pkg_ops if not op in ops]
            pkg_cats = [cat for cat in pkg_cats if not cat in cats]
            ops = ops + pkg_ops
            cats = cats + pkg_cats
        else:
            new_ops, new_cats = load_ops_from_module(mod,cat_root)
            new_ops = [op for op in new_ops if not op in ops]
            new_cats = [cat for cat in new_cats if not cat in cats]
            ops = ops + new_ops
            cats = cats + new_cats
    return ops, cats

def load_ops_from_module(mod,cat_root):
    # iterate through the module's __dict__, find Operations 
    ops = []
    cats = []
    for nm, itm in mod.__dict__.items():
        try:
            # is it a class?
            if isinstance(itm,type):
                # is it a non-abstract subclass of Operation?
                if issubclass(itm,Operation) and not nm in ['Operation','Realtime','Batch']:
                    op = getattr(mod,nm)
                    #op_cats = [cat_root]
                    ops.append( (cat_root,op) )
                    #for cat in op_cats:
                    if not cat_root in cats:
                        cats.append(cat_root)
                        op_load_flags[cat_root] = True
                        op_load_keys.append(cat_root)
                    cat = cat_root
                    parent_cats_done = False
                    while not parent_cats_done:
                        if not cat.rfind('.') == -1:
                            parcat = cat[:cat.rfind('.')]
                            if not parcat in cats:
                                cats.append(parcat)
                                op_load_keys.append(parcat)
                            cat = parcat
                        else:
                            parent_cats_done = True
                    op_load_flags[nm] = True
                    op_load_keys.append(nm)
        except ImportError as ex:
            print '[{}] had trouble dealing with {}: {}'.format(__name__,name,item)
            print 'Error text: {}'.format(ex.message)
            pass 
    return ops, cats

cat_op_list, cat_list = load_ops_from_path(__path__,__name__)

# remove any keys from op_load_flags that are not in op_load_keys
# this serves to update the cfg file if ops or directories are removed
for k in op_load_flags.keys():
    if not k in op_load_keys:
        op_load_flags.pop(k)


