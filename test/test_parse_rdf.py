#!/usr/bin/env python
OBO_PREFIX = u'http://purl.obolibrary.org/obo/'
CDAO_PREFIX = u'http://purl.obolibrary.org/obo/cdao.owl#'
TNRS_PREFIX = u'http://tnrs.evoio.org/terms/'
HAS_PARENT_PREDICATE = u'CDAO_0000179'
HAS_ROOT_PREDICATE = u'CDAO_0000148'
REPRESENTS_TU_PREDICATE = u'CDAO_0000187'
_DEBUGGING = True



from rdflib import Literal, BNode, Namespace
from rdflib import RDF
import rdflib


def rdf2dendropyTree(filepath):
    from rdflib.graph import Graph
    from dendropy import Node, Tree, Edge
    graph = Graph()
    graph.parse(filepath)
    nd_dict = {}
    has_parent_predicate = OBO_PREFIX + HAS_PARENT_PREDICATE
    if _DEBUGGING:
        out = open('parse_rdf.txt', 'w')
    
    
    OBO = Namespace(u"http://purl.obolibrary.org/obo/")
    
    parentless = set()
    for s, p, o in graph.triples((None, OBO[HAS_PARENT_PREDICATE], None)):
        parent = nd_dict.get(id(o))
        
        if parent is None:
            #print 'Parent o.value = ', o.value(rdflib.RDF.nodeID)
            
            raw_o = o
            o = rdflib.resource.Resource(graph, o)
            o_tu = o.value(OBO[REPRESENTS_TU_PREDICATE])
            if o_tu:
                o_label = o_tu.value(rdflib.RDFS.label)
                parent = Node(label=o_label)
            else:
                parent = Node()
            
            nd_dict[id(raw_o)] = parent
            parentless.add(parent)
        child = nd_dict.get(id(s))
        if child is None:
            raw_s = s
            s = rdflib.resource.Resource(graph, s)
            s_tu = s.value(OBO[REPRESENTS_TU_PREDICATE])
            if s_tu:
                s_label = s_tu.value(rdflib.RDFS.label)
                child = Node(label=s_label)
            else:
                child = Node()
            nd_dict[id(raw_s)] = child
        else:
            if child in parentless:
                parentless.remove(child)
        parent.add_child(child)
            
        if _DEBUGGING:
            out.write('%s %s %s\n' % ( str(s), p, o))
            out.write('%s\n' % ( str(parentless)))
    if _DEBUGGING:
        out.close()
    if len(parentless) != 1:
        message = "Expecting to find exactly Node (an object of a has_Parent triple) in the graph without a parent. Found %d" % len(parentless)
        CUTOFF_FOR_LISTING_PARENTLESS_NODES = 1 + len(parentless) # we might want to put in a magic number here to suppress really long output
        if len(parentless) > 0 and len(parentless) < CUTOFF_FOR_LISTING_PARENTLESS_NODES:
            message += ":\n  "
            for i in parentless:
                if i.label:
                    message += "\n  " + i.label
                else:
                    message += "\n  <unlabeled>" + str(id(i))
            raise ValueError(message)
        else:
            sys.exit('no parentless')
            return None
    tree = Tree()
    tree.seed_node = list(parentless)[0]
    tree.is_rooted = True
    return tree

if __name__ == '__main__':
    import sys
    t = rdf2dendropyTree(sys.argv[1])
    print t.write_to_stream(sys.stdout, schema="nexml")
            
