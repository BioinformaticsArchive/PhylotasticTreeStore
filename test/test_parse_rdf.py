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
    mrdf = Namespace(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    parentless = set()
    dendro_nd_to_rdf = {}
    for s, p, o in graph.triples((None, OBO[HAS_PARENT_PREDICATE], None)):
        print type(s), type(p), type(o)
        print s, p, o
#        o_res = rdflib.Resource(graph, o)
        parent = nd_dict.get(o)
        
        if parent is None:
            #print 'Parent o.value = ', o.value(rdflib.RDF.nodeID)
            
            raw_o = o
            o = rdflib.resource.Resource(graph, o)
            print 'Parent nodeID = ', graph.value(raw_o, rdflib.RDF.nodeID)
            o_tu = o.value(OBO[REPRESENTS_TU_PREDICATE])
            if o_tu:
                o_label = o_tu.value(rdflib.RDFS.label)
                parent = Node(label=o_label)
            else:
                parent = Node()
            print 'adding parent', id(parent), 'from', raw_o
            
            nd_dict[raw_o] = parent
            dendro_nd_to_rdf[parent] = raw_o
            parentless.add(parent)
        child = nd_dict.get(s)
        if child is None:
            raw_s = s
            s = rdflib.resource.Resource(graph, s)
            print 'Parent nodeID = ', s.value(rdflib.RDF.nodeID)
            s_tu = s.value(OBO[REPRESENTS_TU_PREDICATE])
            if s_tu:
                print s_tu
                s_label = s_tu.value(rdflib.RDFS.label)
                print s_label
                child = Node(label=s_label)
            else:
                child = Node()
            print 'adding child', id(child), ' from', raw_s
            nd_dict[raw_s] = child
            dendro_nd_to_rdf[child] = raw_s
        else:
            if parent in parentless:
                print 'Removing', id(parent)
                parentless.remove(parent)
        parent.add_child(child)
            
        print 'len(parentless) =', len(parentless)
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
            
