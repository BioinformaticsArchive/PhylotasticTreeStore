Phylotastic TreeStore
=====================
This is not quite working yet.

This web app provides an adaptor that exposes some aspects of the SPARQL 
endpoint (powered by Virtuoso) running at:
    http://phylotastic.nescent.org/sparql
via the PhyloWS API
    https://www.nescent.org/wg_evoinfo/PhyloWS/REST

An example instance is running at:
    http://phylotastic.nescent.org/PhylotasticTreeStore/phylows/


Installation
------------
If you have installed pip ( http://pypi.python.org/packages/source/p/pip/pip-1.1.tar.gz#md5=62a9f08dd5dc69d76734568a6c040508 ),
which may require setuptools ( http://pypi.python.org/pypi/setuptools ).

Then, from bash prompt, you should be able to:

    wget http://www.web2py.com/examples/static/web2py_src.zip
    unzip web2py_src.zip
    virtualenv vdev
    source vdev/bin/activate
    pip install rdflib
    pip install requests
    pip install dendropy
    git clone git://github.com/phylotastic/PhylotasticTreeStore.git
    ln -s "$PWD/PhylotasticTreeStore" web2py/applications/PhylotasticTreeStore
    python web2py/web2py.py --nogui

Enter an admin's password for web2py and then visit:
    http://127.0.0.1:8000/PhylotasticTreeStore/phylows
in your browser.
    
Notes
-----
To see the RDF representation of a tree enter the following query at
 http://phylotastic.nescent.org/sparql
 
<pre>
prefix obo: <http://purl.obolibrary.org/obo/>
prefix cdao: <http://purl.obolibrary.org/obo/cdao.owl#>
construct 
{
?node obo:CDAO_0000179 ?parent_node . 
?node obo:CDAO_0000187 ?otu .
?otu rdfs:label ?otu_label .
}
 where 
{
<http://phylotastic.nescent.org/trees/Treemytree3> obo:CDAO_0000148 ?root .
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
</pre>

Or see the N-triples at http://phylotastic.nescent.org/sparql?default-graph-uri=&query=prefix+obo%3A+%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F%3E%0D%0Aprefix+cdao%3A+%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fcdao.owl%23%3E%0D%0Aconstruct+%0D%0A%7B%0D%0A%3Fnode+obo%3ACDAO_0000179+%3Fparent_node+.+%0D%0A%3Fnode+obo%3ACDAO_0000187+%3Fotu+.%0D%0A%3Fotu+rdfs%3Alabel+%3Fotu_label+.%0D%0A%7D%0D%0A+where+%0D%0A%7B%0D%0A%3Chttp%3A%2F%2Fphylotastic.nescent.org%2Ftrees%2FTreemytree3%3E+obo%3ACDAO_0000148+%3Froot+.%0D%0A%3Fnode+obo%3ACDAO_0000179+%3Fparent_node+.+%0D%0A%3Fnode+obo%3ACDAO_0000179+%3Froot+option%28transitive%29+.+%0D%0AOPTIONAL+%7B+%0D%0A++++%3Fnode+obo%3ACDAO_0000187+%3Fotu+.+%0D%0A++++%3Fotu+rdfs%3Alabel+%3Fotu_label+.%0D%0A%7D%0D%0AOPTIONAL+%7B+%0D%0A++++%3Froot+obo%3ACDAO_0000187+%3Fotu+.+%0D%0A++++%3Fotu+rdfs%3Alabel+%3Fotu_label+.%0D%0A%7D%0D%0A%7D%0D%0A&format=text%2Fplain&timeout=0&debug=on
