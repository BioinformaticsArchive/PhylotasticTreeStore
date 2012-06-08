#!/usr/bin/env python
import requests
import json

payload = {'taxa_uris': ['http://phylotastic.nescent.org/IDs/ID7.dog',
                   'http://phylotastic.nescent.org/IDs/ID1.bear']}

resp = requests.post('http://127.0.0.1:8000/PhylotasticTreeStore/phylows/find/tree',
                     data=json.dumps(payload))
print resp.url
problem =  resp.raise_for_status()
if problem is None:
    print resp.text
else:
    print problem
