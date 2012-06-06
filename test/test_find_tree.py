#!/usr/bin/env python
import requests

payload = {'uri': ['http://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=180195',
                   'http://www.tropicos.org/Name/1300071']}
resp = requests.post('http://127.0.0.1:8000/PhylotasticTreeStore/phylows/find/tree',
                     params=payload)
problem =  resp.raise_for_status()
if problem is None:
    print resp.text
else:
    print problem
