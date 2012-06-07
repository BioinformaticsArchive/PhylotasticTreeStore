#!/usr/bin/env python
import requests
import sys
tree_id = 'mytree'
if len(sys.argv) > 1:
    tree_id = sys.argv[1]
payload = {'query' : '''prefix cdao: <http://www.evolutionaryontology.org/cdao/1.0/cdao.owl#>
construct 
{
?node cdao:has_Parent ?parent_node . 
}
 where 
{
cdao:%s cdao:has_Root ?root .
?node cdao:has_Parent ?parent_node . 
?node cdao:has_Parent ?root option(transitive) . 
}''' % tree_id,
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

