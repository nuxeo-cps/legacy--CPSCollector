##parameters=
#$Id$

collector_schema = {
    'submit_msg': {
        'type': 'CPS String Field',
        'data': {'is_searchabletext': 1,}},
    'submit_msg_stat': {
        'type': 'CPS Int Field',
        'data': {'default_expr': 'python:0',
                 'is_searchabletext': 0,}},
    'unique_submit': {
        'type': 'CPS Int Field',
        'data': {'default_expr': 'python:1',
                 'is_searchabletext': 0,}},
    'persistent_data': {
        'type': 'CPS Int Field',
        'data': {'default_expr': 'python:0',
                 'is_searchabletext': 0,}},
    }

return {'collector': collector_schema}
