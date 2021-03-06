import copy
from collections import OrderedDict

from .TreeItem import TreeItem
from .DictTree import DictTree

class TreeModel(object):
    """
    This class indexes a DictTree with a set of TreeItems.
    TreeItems keep track of their lineage in the DictTree,
    and can be modified for additional functionality
    in subclasses of TreeModel by adding TreeItem.flags.
    """

    def __init__(self,default_flags={}):
        super(TreeModel,self).__init__()
        # a TreeItem with no parent is the root of the tree
        self._root_item = TreeItem(None,'ROOT')
        # the underlying data are stored in a DictTree. 
        self._tree = DictTree()
        # any TreeItems will be given these default_flags,
        # unless subclasses override TreeModel.create_tree_item()
        self.default_flags = default_flags

    def __getitem__(self,uri):
        return self.get_from_uri(uri)

    def __setitem__(self,uri,val):
        self.set_item(uri,val)
    
    def n_children(self,parent_uri=''):
        itm = self.get_from_uri(parent_uri)
        return itm.n_children()

    def set_item(self,itm_uri,itm_data=None):
        try:
            if '.' in itm_uri:
                parent_uri = itm_uri[:itm_uri.rfind('.')]
                parent_itm = self.get_from_uri(parent_uri)
                itm_tag = itm_uri.split('.')[-1]
            else:
                parent_itm = self._root_item
                itm_tag = itm_uri
            # add TreeItems to index the new TreeModel content 
            treedata = self.build_tree(itm_data)
            self.tree_update(parent_itm,itm_tag,treedata)
            # store the data 
            self._tree.set_uri(itm_uri,itm_data)
        except Exception as ex:
            msg = str('[{}] Encountered an error while trying to set uri {}: \n'
            .format(__name__,itm_uri) + ex.message)
            raise KeyError(msg) 

    def remove_item(self,itm_uri):
        self._tree.delete_uri(itm_uri)
        # remove the corresponding subtree or TreeItem.
        itm = self.get_from_uri(itm_uri)
        parent_itm = itm.parent 
        child_keys = [c.tag for c in parent_itm.children]
        rm_row = child_keys.index(itm.tag)
        parent_itm.children.pop(rm_row)

    def tree_update(self,parent_itm,itm_tag,itm_data):
        """
        Update the tree structure 
        rooted at parent_itm.children[itm_tag],
        such that TreeItems get built 
        to index all of the items in itm_data 
        that are supported by self.build_tree().
        Assume build_tree was called on itm_data
        before passing it as an argument,
        so only need to recurse if itm_data is a dict.
        """
        child_keys = [c.tag for c in parent_itm.children]
        if itm_tag in child_keys:
            # Find the row of existing itm_tag under parent,
            itm_row = child_keys.index(itm_tag)
            itm = parent_itm.children[itm_row]
            # Remove any grandchildren that do not represent the new data
            new_keys = []
            if isinstance(itm_data,dict):
                new_keys = itm_data.keys()
            for gc_row in range(itm.n_children())[::-1]:
                gc_itm = itm.children[gc_row]
                if not gc_itm.tag in new_keys:
                    itm.children.pop(gc_row) 
        else:
            # Put a new TreeItem at the end row
            itm_row = parent_itm.n_children()
            itm = self.create_tree_item(parent_itm,itm_tag)
            parent_itm.children.insert(itm_row,itm)
        # If needed, recurse on itm_data.
        if isinstance(itm_data,dict):
            for tag,val in itm_data.items():
                self.tree_update(itm,tag,val)

    def build_tree(self,x):
        """
        TreeModel.build_tree is called on some object x
        before x is stored in the tree.
        For subclasses of TreeModel to build tree data
        for data types other than dicts and lists,
        build_tree should be reimplemented.
        If data types other than dicts and lists have child items 
        that should be accessible by TreeModel uris,
        they should implement __getitem__(tag).
        """
        if isinstance(x,dict):
            d = OrderedDict()
            for k,v in x.items():
                d[k] = self.build_tree(v) 
            return d
        elif isinstance(x,list):
            d = OrderedDict(zip([str(i) for i in range(len(x))],x)) 
            for k,v in d.items():
                d[k] = self.build_tree(v)
            return d
        else:
            return x

    def get_from_uri(self,uri):
        try:
            path = uri.split('.')
            itm = self._root_item
            for k in path[:-1]:
                child_keys = [c.tag for c in itm.children]
                itm = itm.children[child_keys.index(k)]
            k = path[-1]
            if k:
                child_keys = [c.tag for c in itm.children]
                return itm.children[child_keys.index(k)]
            elif k == '':
                return itm 
        except Exception as ex:
            msg = '\n[{}] Encountered an error while fetching uri {}\n'.format(__name__,uri)
            ex.message = msg + ex.message
            raise ex

    def get_data_from_uri(self,uri):
        return self._tree.get_from_uri(uri)

    def root_tags(self):
        return self._tree.root_keys()

    def tag_error_message(self,tag):
        return self._tree.tag_error_message(tag)

    def is_uri_valid(self,uri):
        return self._tree.is_uri_valid(uri)

    def is_tag_valid(self,tag):
        return self._tree.is_tag_valid(tag)

    def make_unique_uri(self,prefix):
        return self._tree.make_unique_uri(prefix)

    def contains_uri(self,uri):
        return self._tree.contains_uri(uri)

    def build_uri(self,itm):
        """
        Build a URI for TreeItem itm by combining the tags 
        of the lineage of itm, with '.' as a delimiter.
        """
        if itm == self._root_item:
            return ''
        else:
            uri = itm.tag
            while not itm.parent == self._root_item:
                itm = itm.parent
                uri = itm.tag+"."+uri
            return uri

    def create_tree_item(self,parent_itm,itm_tag):
        """
        Build a TreeItem for use in this tree.
        Reimplement create_tree_item() in subclasses of TreeModel
        to add features to TreeItems, such as default values for TreeItem.flags.
        TreeModel implementation returns TreeItem(parent_itm,itm_tag).
        """
        itm = TreeItem(parent_itm,itm_tag)
        itm.flags = copy.copy(self.default_flags)
        return itm
