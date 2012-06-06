# -*- coding: utf-8 -*-
### required - do no delete
def _get_tree(tree_id):
    '''
    Need to add the db connection stuff here...
    '''
    tree = "((whale,hippo),carlzimmer);"
    return tree;

# query URIs of the form phylows/tree/<identifier>
def tree():
    if len(request.args) < 1:
        raise HTTP(400, 'Tree ID required')
    if len(request.args) > 1:
        raise HTTP(400, 'Only one tree ID can be supplied')
    tree_id = request.args[0]
    tree_obj = _get_tree(tree_id)
    if tree_obj is None:
        raise HTTP(404, 'Tree %s not found' % tree_id)
    return T(tree_obj);

# query URIs of the form phylows/find/<query>
def find():
    # form phylows/find/tree/
    # returns list of URIs
    if "tree" in request.args:
        x = request.vars.get('uri')
        if x is None:
            raise HTTP(400, 'no URI specified')
        # magic involving sparql
        # takes list of URIs and queries treestore for trees that contain those URIs
        treedict = {"http://example.com/tree10" : { "label" : "something", "author": ""}, 
  "http://example.com/tree34": { "label" : "something", "author": ""} }
        return response.json(treedict)
    else:
        raise HTTP(400, 'query not yet implemented')

