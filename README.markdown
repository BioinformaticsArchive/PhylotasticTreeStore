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
From bash prompt:

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
    
