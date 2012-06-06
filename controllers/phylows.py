# -*- coding: utf-8 -*-
### required - do no delete
def _get_tree(tree_id):
    '''
    Need to add the db connection stuff here...
    '''
    return None

def tree():
    if len(request.args) < 1:
        raise HTTP(400, 'Tree ID required')
    if len(request.args) > 1:
        raise HTTP(400, 'Only a one tree ID can be supplied')
    tree_id = request.args[0]
    tree_obj = _get_tree(tree_id)
    if tree_obj is None:
        raise HTTP(404, 'Tree %s not found' % tree_id)
    return T('hi from tree ' + str(request.args))


