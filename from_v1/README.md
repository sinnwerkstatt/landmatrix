# How to migrate data from Landmatrix V1
Basically, look at `migrate.py` for examples. THe classes doing the migration are, somewhat inconsistently, called
`Map<class>`. 

Some migrations depend on other migrations being run first. If you want to run such a migration without running the
depended upon migration first, set the class variable `_done` in the depended upon class to `True`, as in 
`MapActivityAttributeGroup._done = True`.
  
 

# How to find activities where the coordinates are borked
Executed on the dataset I have for development. Before deployment, should be run on production data again.
```
$ python manage.py shell
```
```python
>>> from landmatrix.models import *
>>> def is_number(s):
...     try:
...         float(s)
...     except ValueError:
...         return False
...     return True
>>> def get_borked_coordinate_ids(field): 
...     return set([element['activity_identifier'] 
...          for element in A_Key_Value_Lookup.objects.filter(key=field).values('activity_identifier', 'value') 
...          if not is_number(element['value'])])
>>> get_borked_coordinate_ids('point_lat')) | set(get_borked_coordinate_ids('point_lon')
set([132L, 4261L, 3676L, 3117L])
```