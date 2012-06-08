#!/usr/bin/env python
import requests, os

payload = {'taxa_uris': ['http://phylotastic.nescent.org/IDs/ID7.dog']}

if os.environ.get('DEBUG_WITH_PHYLOTASTIC_SERVER'):
    domain_name = 'http://phylotastic.nescent.org'
else:
    domain_name = 'http://127.0.0.1:8000'

resp = requests.post(domain_name + '/PhylotasticTreeStore/phylows/find/tree',
                     params=payload)
print resp.url
problem =  resp.raise_for_status()
if problem is None:
    print resp.text
else:
    print problem
results = resp.json
for tree_uri in results.keys():
    print tree_uri
    tree_resp = requests.get(domain_name + '/PhylotasticTreeStore/phylows/tree', params={'tree_uri':tree_uri})
    print "Result:", tree_resp.content
