##parameters=
#$Id$
"""
the collector in CPSDocument
"""

collector_type = {
    'title': 'portal_type_CollectorDocument_title',
    'description': 'portal_type_CollectorDocument_description',
    'content_icon': 'CollectorDocument_icon.png',
    'product': 'CPSCollector',
    'factory': 'addCollectorDocument',
    'immediate_view': 'CollectorDocument_editProp',
    'allow_discussion': 0,
    'filter_content_types': 0,
    'cps_is_searchable': 1,
    'cps_display_as_document_in_listing': 1,
    'cps_proxy_type': 'folder',
    'schemas': ['metadata', 'common', 'collector'],
    'layouts': ['common'],
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'Form_view',
                 'permissions': ('View',)},
                {'id': 'view_stat',
                 'name': 'action_view_stat',
                 'action': 'CollectorDocument_viewStat',
                 'permissions': ('Modify portal content',)},
                {'id': 'edit',
                 'name': 'action_modify_prop',
                 'action': 'CollectorDocument_editProp',
                 'permissions': ('Modify portal content',)},
                {'id': 'edit_form',
                 'name': 'action_modify_form',
                 'action': 'Form_editForm',
                 'permissions': ('Modify portal content',)},
                {'id': 'export',
                 'name': 'action_export_csv',
                 'action': 'CollectorDocument_exportData',
                  'permissions': ('Modify portal content',)},
                {'id': 'erase',
                 'name': 'action_erase_data',
                 'action': 'Form_eraseDataPrompt',
                 'permissions': ('Modify portal content',)},
                )
    }

quiz_type = {
    'title': 'portal_type_QuizDocument_title',
    'description': 'portal_type_QuizDocument_description',
    'content_icon': 'QuizDocument_icon.png',
    'product': 'CPSCollector',
    'factory': 'addQuizDocument',
    'immediate_view': 'CollectorDocument_editProp',
    'allow_discussion': 0,
    'filter_content_types': 0,
    'cps_is_searchable': 1,
    'cps_display_as_document_in_listing': 1,
    'cps_proxy_type': 'folder',
    'schemas': ['metadata', 'common', 'collector'],
    'layouts': ['common'],
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'Form_view',
                 'permissions': ('View',)},
                {'id': 'check_results',
                 'name': 'action_view_results',
                 'action': 'QuizDocument_viewResults',
                 'permissions': ('View',)},
                {'id': 'view_stat',
                 'name': 'action_view_stat',
                 'action': 'CollectorDocument_viewStat',
                 'permissions': ('Modify portal content',)},
                {'id': 'edit',
                 'name': 'action_modify_prop',
                 'action': 'CollectorDocument_editProp',
                 'permissions': ('Modify portal content',)},
                {'id': 'edit_form',
                 'name': 'action_modify_form',
                 'action': 'Form_editQuizForm',
                 'permissions': ('Modify portal content',)},
                {'id': 'export',
                 'name': 'action_export_csv',
                 'action': 'exportData',
                  'permissions': ('Modify portal content',)},
                {'id': 'erase',
                 'name': 'action_erase_data',
                 'action': 'Form_eraseDataPrompt',
                 'permissions': ('Modify portal content',)},
                )
    }


return {'Collector Document': collector_type,
        'Quiz Document': quiz_type,
        }
