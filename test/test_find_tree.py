#!/usr/bin/env python
import requests
import json
import os
payload = {'taxa_uris': ['http://phylotastic.nescent.org/IDs/ID7.dog',
                   'http://phylotastic.nescent.org/IDs/ID1.bear']}

if os.environ.get('DEBUG_WITH_PHYLOTASTIC_SERVER'):
    domain_name = 'http://phylotastic.nescent.org'
else:
    domain_name = 'http://127.0.0.1:8000'
data = json.dumps(payload)
print data
resp = requests.post(domain_name + 'PhylotasticTreeStore/phylows/find/tree', data=data)
print resp.url
problem =  resp.raise_for_status()
if problem is None:
    print resp.text
else:
    print problem
