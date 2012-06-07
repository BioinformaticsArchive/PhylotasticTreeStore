# -*- coding: utf-8 -*-
### required - do no delete
import requests

OBO_PREFIX = u'http://purl.obolibrary.org/obo/'
CDAO_PREFIX = u'http://purl.obolibrary.org/obo/cdao.owl#'
TNRS_PREFIX = u'http://tnrs.evoio.org/terms/'
HAS_PARENT_PREDICATE = u'CDAO_0000179'
HAS_ROOT_PREDICATE = u'CDAO_0000148'
REPRESENTS_TU_PREDICATE = u'CDAO_0000187'
SPARQL_SERVER_GET_URL = 'http://phylotastic.nescent.org/sparql'

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
    has_parent_predicate = OBO_PREFIX + HAS_PARENT_PREDICATE
    parentless = set()
    for subject_o, predicate, obj_o in graph:
        if unicode(predicate) == has_parent_predicate:
            subject = unicode(subject_o)
            obj_ = unicode(obj_o)
            s_suffix = subject
            o_suffix = obj_
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
            raise ValueError(message)
        else:
            return None
    tree = Tree()
    tree.seed_node = list(parentless)[0]
    tree.is_rooted = True
    return tree

SKIP_QUERY = False
def _get_tree_rdf(tree_id):
    '''
    Need to add the db connection stuff here...
    '''
    if SKIP_QUERY:
        return """<?xml version="1.0" encoding="utf-8" ?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_3"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_14"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_9"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_11"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_5"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_6"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_11"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_12"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_10"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_11"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_1"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_3"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_7"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_9"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_4"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_6"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_6"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_12"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_8"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_9"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_2"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_3"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_13"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_14"/></rdf:Description>
<rdf:Description rdf:about="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_12"><n0pred:has_Parent xmlns:n0pred="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#" rdf:resource="http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#Node_14"/></rdf:Description>
</rdf:RDF>
"""
    
    cleaned_id = tree_id # TEMP we need to protect against SPARQL injection attact?
    query = u'prefix obo: <' + OBO_PREFIX + u'''>
prefix cdao: <''' + CDAO_PREFIX + u'''>
construct 
{
?node obo:CDAO_0000179 ?parent_node . 
}
 where 
{
''' + cleaned_id + ''' obo:CDAO_0000148 ?root .
?node obo:CDAO_0000179 ?parent_node . 
?node obo:CDAO_0000179 ?root option(transitive) . 
}'''

    payload = {'query' : query,
               'default-graph-uri' : '',
               'named-graph-uri' : '',
               'format' : 'application/sparql-results+xml',
    }
    o = open('req', 'w')
    o.write('\n'.join([(k + ' : ' + v) for k, v in payload.iteritems()]))
    o.close()
    resp = requests.get(SPARQL_SERVER_GET_URL, params=payload)
    resp.raise_for_status()
    return resp.content


def _get_tree_list(taxa_uri_list):
    query = '''prefix obo: <http://purl.obolibrary.org/obo/>
prefix tnrs: <http://tnrs.evoio.org/terms/>

select distinct ?tree 
 where 
{
?tree obo:CDAO_0000148 ?root .
?node obo:CDAO_0000179 ?root option(transitive) . 
{ ?node obo:CDAO_0000187 ?otu . } UNION { ?root obo:CDAO_0000187 ?otu .}
?otu tnrs:match ?match .
%s
}''' % '\n UNION '.join(['{?match tnrs:reference <' + i + '> . }' for i in taxa_uri_list])
    payload = {'query' : query,
               'default-graph-uri' : '',
               'named-graph-uri' : '',
               'format' : 'application/sparql-results+xml',
    }
    o = open('req2', 'w')
    o.write('\n'.join([(k + ' : ' + v) for k, v in payload.iteritems()]))
    o.close()
    try:
        resp = requests.get(SPARQL_SERVER_GET_URL, params=payload)
        resp.raise_for_status()
    except Exception, x:
        o = open('req2', 'a')
        o.write('\nError:' + str(x))
        o.close()
        raise
    return [resp.content]


# query URIs of the form phylows/tree/<identifier>
def tree():
    ''' routed to here: <hostname>/PhylotasticTreeStore/phylows/tree/tree_id
    '''
    if len(request.args) > 1:
        raise HTTP(400, 'Only one tree ID can be supplied')
    if len(request.args) < 1:
        tree_id = request.vars.get('uri')
        if not tree_id:
            raise HTTP(400, 'Tree ID required')
    else:
        # If we we get an id through phyloWS, we make the uri by adding the obo: prefix
        tree_id = 'cdao:' + request.args[0]
    try:
        tree_rdf = _get_tree_rdf(tree_id)
        
        tree_obj = rdf2dendropyTree(data=tree_rdf)
    except:
        raise
    if tree_obj is None:
        raise HTTP(404, 'Tree %s not found' % tree_id)
    
    # temp
    from cStringIO import StringIO
    b = StringIO()
    tree_obj.write_to_stream(b, schema="nexml")
    return T(b.getvalue())

# query URIs of the form phylows/find/<query>
def find():
    # post to  phylows/find/tree/
    # returns list of URIs
    if "tree" in request.args:
        taxa_uris = request.vars.get('taxa_uris')
        if taxa_uris is None:
            raise HTTP(400, 'no URI specified')
        # magic involving sparql
        # takes list of URIs and queries treestore for trees that contain those URIs
        tree_id_list = _get_tree_list(taxa_uris)
        ret = {}
        for el in tree_id_list:
            ret[el] = { "label" : "something", "author": ""}
        return response.json(ret)
    else:
        raise HTTP(400, 'query not yet implemented')

def index():
    if request.vars.tree_id:
        redirect(URL(c='phylows', f='tree', args=[request.vars.tree_id]))
    return dict()
