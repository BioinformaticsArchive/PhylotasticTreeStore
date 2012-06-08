#!/usr/bin/env python
import requests

payload = {'taxa_uris': ['http://phylotastic.nescent.org/IDs/ID7.dog']}

resp = requests.post('http://127.0.0.1:8000/PhylotasticTreeStore/phylows/find/tree',
                     params=payload)
problem =  resp.raise_for_status()
if problem is None:
    print resp.text
else:
    print problem
results = resp.json
for tree_uri in results.keys():
    print tree_uri
    tree_resp = requests.get('http://127.0.0.1:8000/PhylotasticTreeStore/phylows/tree', params={'tree_uri':tree_uri})
    print "Result:", tree_resp.content
