##parameters=widget=None
# $Id$

"""returns the translation corresponding to a field type (for translation)"""

widget2msgid = {
    'submit': 'collector_field_button',
    'checkbox': 'collector_field_checkbox',
    'comment': 'collector_field_comment',
    'date': 'collector_field_date',
    'email': 'collector_field_email',
    'file': 'collector_field_file',
    'float': 'collector_field_float',
    'hidden': 'collector_field_hiddenstring',
    'identifier': 'collector_field_identifier',
    'int': 'collector_field_integer',
    'password': 'collector_field_password',
    'phone': 'collector_field_phonenumber',
    'radio': 'collector_field_radiobutton',
    'reset': 'collector_field_resetbutton',
    'selection': 'collector_field_selection',
    'separator': 'collector_field_separator',
    'string': 'collector_field_string',
    'string_ro': 'collector_field_string_ro',
    'text': 'collector_field_textarea',
    'title': 'collector_field_title',
    'url': 'collector_field_url',
    'vradio': 'collector_field_vradiobutton',
    }

if widget and widget2msgid.has_key(widget):
    mcat = context.Localizer.cpscollector
    return mcat(widget2msgid.get(widget))
else:
    return widget

