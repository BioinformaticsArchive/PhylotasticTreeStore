# -*- coding: utf-8 -*-
### required - do no delete

def rdf2dendropyTree(file_obj=None, data=None):
    '''
    Parses the content (a `file_obj` file object or `data` as a) into a dendropyTree.
    
    Uses the 'has_Parent' term in http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#
    to construct and return a rooted dendropy.Tree object
    
    Relies on rdflib and dendropy.
    Raises ValueError if the graph does not imply exactly 1 root node
    '''
    
    from rdflib.graph import Graph
    from dendropy import Node, Tree, Edge
    graph = Graph()
    if file_obj:
        graph.parse(file=file_obj)
    else:
        graph.parse(data=data)
    nd_dict = {}
    has_parent_predicate = u'http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#has_Parent'
    identifier_prefix = u'http://www.evolutionaryontology.org/cdao/1.0/&localspace;'
    suff_ind = len(identifier_prefix)
    parentless = set()
    for subject_o, predicate, obj_o in graph:
        if unicode(predicate) == has_parent_predicate:
            subject = unicode(subject_o)
            obj_ = unicode(obj_o)
            assert subject.startswith(identifier_prefix)
            assert obj_.startswith(identifier_prefix)
            s_suffix = subject[suff_ind:]
            o_suffix = obj_[suff_ind:]
            parent = nd_dict.get(o_suffix)
            if parent is None:
                parent = Node(label=o_suffix)
                nd_dict[o_suffix] = parent
                parentless.add(parent)
            child = nd_dict.get(s_suffix)
            if child is None:
                child = Node(label=s_suffix)
                nd_dict[s_suffix] = child
            else:
                parentless.remove(child)
            parent.add_child(child)

    if len(parentless) != 1:
        message = "Expecting to find exactly Node (an object of a has_Parent triple) in the graph without a parent. Found %d" % len(parentless)
        CUTOFF_FOR_LISTING_PARENTLESS_NODES = len(parentless) # we might want to put in a magic number here to suppress really long output
        if len(parentless) > 0 and len(parentless) < CUTOFF_FOR_LISTING_PARENTLESS_NODES:
            message += ":\n  "
            message += "\n  ".join([i.label for i in parentless])
        else:
            message += "."
        raise ValueError(message)
    tree = Tree()
    tree.seed_node = list(parentless)[0]
    tree.is_rooted = True
    return tree


def _get_tree(tree_id):
    '''
    Need to add the db connection stuff here...
    '''
    tree = """<?xml version="1.0" encoding="utf-8" ?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_3"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_14"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_9"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_11"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_5"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_6"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_11"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_12"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_10"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_11"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_1"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_3"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_7"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_9"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_4"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_6"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_6"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_12"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_8"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_9"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_2"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_3"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_13"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_14"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_12"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/&amp;localspace;Node_14"/></rdf:Description>
</rdf:RDF>
"""
    return rdf2dendropyTree(data=tree);

# query URIs of the form phylows/tree/<identifier>
def tree():
    if len(request.args) < 1:
        raise HTTP(400, 'Tree ID required')
    if len(request.args) > 1:
        raise HTTP(400, 'Only one tree ID can be supplied')
    tree_id = request.args[0]
    tree_obj = _get_tree(tree_id)
    if tree_obj is None:
        raise HTTP(404, 'Tree %s not found' % tree_id)
    
    # temp
    from cStringIO import StringIO
    b = StringIO()
    tree_obj.write_to_stream(b, schema="nexml")
    return T(b.getvalue())

# query URIs of the form phylows/find/<query>
def find():
    # form phylows/find/tree/
    # returns list of URIs
    if "tree" in request.args:
        x = request.vars.get('uri')
        if x is None:
            raise HTTP(400, 'no URI specified')
        # magic involving sparql
        # takes list of URIs and queries treestore for trees that contain those URIs
        treedict = {"http://example.com/tree10" : { "label" : "something", "author": ""}, 
  "http://example.com/tree34": { "label" : "something", "author": ""} }
        return response.json(treedict)
    else:
        raise HTTP(400, 'query not yet implemented')

def index():
    if request.vars.tree_id:
        redirect(URL(c='phylows', f='tree', args=[request.vars.tree_id]))
    return dict()
