# -*- coding: utf-8 -*-
### required - do no delete
import requests
import json

OBO_PREFIX = u'http://purl.obolibrary.org/obo/'
CDAO_PREFIX = u'http://purl.obolibrary.org/obo/cdao.owl#'
TNRS_PREFIX = u'http://tnrs.evoio.org/terms/'
HAS_PARENT_PREDICATE = u'CDAO_0000179'
HAS_ROOT_PREDICATE = u'CDAO_0000148'
REPRESENTS_TU_PREDICATE = u'CDAO_0000187'
SPARQL_SERVER_GET_URL = 'http://phylotastic.nescent.org/sparql'
import os
_DEBUGGING = os.environ.get('PHYLOTASTIC_TREE_STORE_DEBUGGING') == '1'
import rdflib


def rdf2dendropyTree(file_obj=None, data=None):
    '''
    Parses the content (a `file_obj` file object or `data` as a) into a dendropyTree.
    
    Uses the 'has_Parent' term in http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#
    to construct and return a rooted dendropy.Tree object
    
    Relies on rdflib and dendropy.
    Raises ValueError if the graph does not imply exactly 1 root node
    '''
    
    from dendropy import Node, Tree, Edge, TaxonSet, Taxon
    graph = rdflib.Graph()
    if file_obj:
        graph.parse(file=file_obj)
    else:
        graph.parse(data=data, format='xml')
    nd_dict = {}
    has_parent_predicate = OBO_PREFIX + HAS_PARENT_PREDICATE
    if _DEBUGGING:
        out = open('parse_rdf.txt', 'w')
    taxon_set = TaxonSet()
    OBO = rdflib.Namespace(u"http://purl.obolibrary.org/obo/")
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
                t = Taxon(label=o_label)
                taxon_set.append(t)
                parent = Node(taxon=t)
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
                t = Taxon(label=s_label)
                taxon_set.append(t)
                child = Node(taxon=t)
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
            return None
    tree = Tree(taxon_set=taxon_set)
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
<rdf:Description rdf:nodeID="b10830"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10829"/></rdf:Description>
<rdf:Description rdf:nodeID="b10832"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10830"/></rdf:Description>
<rdf:Description rdf:nodeID="b10818"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10817"/></rdf:Description>
<rdf:Description rdf:nodeID="b10834"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10830"/></rdf:Description>
<rdf:Description rdf:nodeID="b10826"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10824"/></rdf:Description>
<rdf:Description rdf:nodeID="b10824"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10823"/></rdf:Description>
<rdf:Description rdf:nodeID="b10822"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10818"/></rdf:Description>
<rdf:Description rdf:nodeID="b10838"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10817"/></rdf:Description>
<rdf:Description rdf:nodeID="b10828"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10824"/></rdf:Description>
<rdf:Description rdf:nodeID="b10836"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10829"/></rdf:Description>
<rdf:Description rdf:nodeID="b10823"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10817"/></rdf:Description>
<rdf:Description rdf:nodeID="b10820"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10818"/></rdf:Description>
<rdf:Description rdf:nodeID="b10829"><n0pred:CDAO_0000179 xmlns:n0pred="http://purl.obolibrary.org/obo/" rdf:nodeID="b10823"/></rdf:Description>
</rdf:RDF>
"""
    
    cleaned_id = tree_id # TEMP we need to protect against SPARQL injection attact?
    query = u'prefix obo: <' + OBO_PREFIX + u'''>
prefix cdao: <''' + CDAO_PREFIX + u'''>
construct 
{
?node obo:CDAO_0000179 ?parent_node . 
?node obo:CDAO_0000187 ?otu .
?otu rdfs:label ?otu_label .
}
 where 
{
''' + cleaned_id + ''' obo:CDAO_0000148 ?root .
?node obo:CDAO_0000179 ?parent_node . 
?node obo:CDAO_0000179 ?root option(transitive) . 
OPTIONAL { 
    ?node obo:CDAO_0000187 ?otu . 
    ?otu rdfs:label ?otu_label .
}
OPTIONAL { 
    ?root obo:CDAO_0000187 ?otu . 
    ?otu rdfs:label ?otu_label .
}
}
'''

    payload = {'query' : query,
               'default-graph-uri' : '',
               'named-graph-uri' : '',
               'format' : 'application/sparql-results+xml',
    }
    if _DEBUGGING:
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
               'format' : 'application/sparql-results+json',
    }
    if _DEBUGGING:
        o = open('req2', 'w')
        o.write('\n'.join([(k + ' : ' + v) for k, v in payload.iteritems()]))
        o.close()
    try:
        resp = requests.get(SPARQL_SERVER_GET_URL, params=payload)
        resp.raise_for_status()
        results = resp.json
        trees = [binding["tree"]["value"] for binding in results['results']['bindings']]
    except Exception, x:
        if _DEBUGGING:
            o = open('req2', 'a')
            o.write('\nError:' + str(x))
            o.close()
        raise
    return trees


# query URIs of the form phylows/tree/<identifier>
def tree():
    ''' routed to here: <hostname>/PhylotasticTreeStore/phylows/tree/tree_id
    '''
    if len(request.args) > 1:
        raise HTTP(400, 'Only one tree ID can be supplied')
    if len(request.args) < 1:
        tree_id = request.vars.get('tree_uri')
        if tree_id is None:
            tree_id = request.vars.get('uri')
        if not tree_id:
            raise HTTP(400, 'Tree ID required')
        tree_id = '<' + tree_id + '>'
    else:
        # If we we get an id through phyloWS, we make the uri by adding the obo: prefix
        tree_id = '<' + request.args[0] + '>'
    
    format = request.vars.get('format', 'nexml')
    try:
        tree_rdf = _get_tree_rdf(tree_id)
        if format.lower() == 'rdfxml':
            response.headers['Content-Type']='application/xml'
            return tree_rdf
        tree_obj = rdf2dendropyTree(data=tree_rdf)
    except:
        raise
    if tree_obj is None:
        raise HTTP(404, 'Tree %s not found' % tree_id)
    
    # temp
    from cStringIO import StringIO
    b = StringIO()
    tree_obj.write_to_stream(b, schema="nexml")
    response.headers['Content-Type']='application/xml'
    return b.getvalue()

# query URIs of the form phylows/find/<query>
def find():
    # post to  phylows/find/tree/
    # returns list of URIs
    if "tree" in request.args:
        result = request.body.read()
        try:
            taxa_json = json.loads(result)
            taxa_uris = taxa_json.get(u'taxa_uris')
            if taxa_uris is None:
                taxa_uris = taxa_json.get('taxa_uris')
        except:
            taxa_uris = None
        if taxa_uris is None:
            taxa_uris = request.vars.get('taxa_uris')
        if taxa_uris is None:
            raise HTTP(400, 'no URI specified')
        if isinstance(taxa_uris, (str, unicode)):
            taxa_uris = [taxa_uris]
        # magic involving sparql
        # takes list of URIs and queries treestore for trees that contain those URIs
        tree_id_list = _get_tree_list(taxa_uris)
        ret = {}
        for el in tree_id_list:
            ret[el] = { "label" : "", "author": ""}
        return response.json(ret)
    else:
        raise HTTP(400, 'query not yet implemented')

def index():
    if request.vars.tree_id:
        redirect(URL(c='phylows', f='tree', args=[request.vars.tree_id]))
    return dict()
