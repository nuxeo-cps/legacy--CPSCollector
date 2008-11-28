============
CPSCollector
============

:Author: Marc-Aurèle DARCHE
:Revision: $Id$

.. sectnum::    :depth: 4
.. contents::   :depth: 4


Presentation
============

The goal of Collector Document is to create HTML forms TTW.
The Collector Document takes care of the validation and error handling.
The action taken by the Collector is to store the inputs into a CollectorItem.
A Collector Document is folderish and contains its CollectorItems.
Of course ColletorsItems can be exported.

Here is a short list of features:

- Collector handles the following field types:
  title, separator, comment, string, email, identifier, string_ro, phone,
  date, url, password, int, float, text, file, checkbox, radio, selection,
  submit, reset, hidden
- You can configure the message displayed after a valid submission
- You can show statistics on data collected after a submission.
  This is like an instant survey
- You can limit the number of submissions to one per user
- You can create i18n form using label begining with '_'
- You can move fields up/down and display many fields on the same row
- You can modify the Form (add edit move delete fields) at any time without
  losing already collected data
- Collector can remember and pre fill the form with the latest valid inputs
  of the user
- You can download all collected data as a csv file
- You can erase all collected data

Note:

- for cps2 use: skins/cps
- for cps3 use: skins/cps3 then skins/cps


Upgrading old forms
===================

Forms created with older versions of CPSCollector may have problems, errors,
such as this one::
  File "/home/zope/cps/Products/CPSCollector/Form.py", line 407, in getRows
    nb_cols.append(self.getNbSlot(f))
  File "/home/zope/cps/Products/CPSCollector/Form.py", line 345, in getNbSlot
    t = self.fields[f_name]['type']
  KeyError: 'regexp__'


There is an `upgrade` method provided to upgrade those old forms and to fix the
problem. It's simple to apply: just visit the form by HTTP (for example with a
web browser) at its URL suffixed by ``/upgrade``. So for example if your form
has the URL  ``http://my.site.net/sections/vendor/myform``, visiting the URL
``http://my.site.net/sections/vendor/myform/upgrade`` will upgrade the form and
fix the problem.


.. Local Variables:
.. mode: rst
.. End:
.. vim: set filetype=rst:
