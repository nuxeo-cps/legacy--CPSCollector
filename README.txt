NuxCPSCollector


The goal of Collector Document is to create html form TTW
The Collector Document make the validation and error handling. 
The action taken by the Collector is to store the inputs into a CollectorItem.
Collector Document is folderish and contains its CollectorItems.
Of course ColletorsItems can be exported.

here is a short list of features:
- Collector handle the following field types:
  title, separator, comment, string, email, identifier, string_ro, phone,
  date, url, password, int, float, text, file, checkbox, radio, selection,
  submit, reset, hidden
- You can configure the message displayed after a valid submission
- You can show statistic on data collected after a submission 
  this is like an instant survey
- You can limit the number of submission to one per user
- You can create i18n form using label begining with '_'
- You can move fields up/down and display many fields on the same row
- You can modify the Form (add edit move delete fields) at any time without
  loosing already collected data
- Collector can remember and pre fill the form with the latest valid inputs 
  of the user
- You can download all collected data as a csv file
- You can erase all collected data

Note:
- for cps2 use:  skins/cps
- for cps3 use:  skins/cps3 then skins/cps