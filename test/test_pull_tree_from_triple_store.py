#!/usr/bin/env python
import requests

payload = {'query' : '''prefix cdao: <http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#>
construct 
{
?node cdao:has_Parent ?parent_node . 
}
 where 
{
<http://www.evolutionaryontology.org/cdao/1.0/&localspace;mytree> cdao:has_Root ?root .
 ?node cdao:has_Parent ?parent_node . 
?node cdao:has_Parent ?root option(transitive) . 
}''',
    'default-graph-uri' : '',
    'named-graph-uri' : '',
    'format' : 'application/sparql-results+xml',

}

resp = requests.get('http://phylotastic.nescent.org/sparql',
                     params=payload)
print resp.url
problem =  resp.raise_for_status()
if problem is None:
    print resp.text
else:
    print problem

