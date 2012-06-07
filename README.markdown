Phylotastic TreeStore
=====================




Installation
------------
From the bash:

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
your browser.
    
