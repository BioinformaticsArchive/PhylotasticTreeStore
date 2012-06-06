#!/usr/bin/env python
import sys
from rdflib.graph import Graph
from dendropy import Node, Tree, Edge

def rdf2dendropyTree(filepath):
    graph = Graph()
    graph.parse(filepath)
    tree = Tree()
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
            print str(parent)
        else:
            print '?', str(predicate)
    print parentless
    assert len(parentless) == 1
    tree.seed_node = list(parentless)[0]
    return tree


if __name__ == '__main__':
    t = rdf2dendropyTree(sys.argv[1])
    print t.write_to_stream(sys.stdout, schema="nexml")
            
