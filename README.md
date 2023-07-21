# Coding Power BI Report Layout with Python

- [Coding Power BI Report Layout with Python](#coding-power-bi-report-layout-with-python)
  - [Installation and use](#installation-and-use)
  - [Why?](#why)
  - [Features](#features)
  - [Use case](#use-case)
  - [Licensing and Author](#licensing-and-author)


## Installation and use

To use this module in Python, just install it with pip in the command line.

```
pip install pypbireport
```

Inside a jupyter notebook or python script, import the module. `ppr` is just a recommendation. 

```
import pypbireport as ppr
```

Instantiate a PBIReport object and follow examples in [use case](#use-case).

```
report = ppr.PBIReport(pbix_path)
```




## Why?

Power BI report developing can become boring sometime. Get visuals in right place, modify pages and settings a lot of bookmarks (buttons) behavior in report. Puffs 😣  

I was lazy about doing this in the Power BI user interface. 🦥

I wonder one day having some way to **coding PBI reports layout**, so that I run a script and *voilà*, everything in its place.

So, here we are. This module for python does some of this work. Import it from your script, point out an existing PBIX file and [check what you can do](#features) and [some examples](#use-case).

## Features

Version 0.1  
1. Read PBI **report json** as a **python dictionary**
2. **Resume** pages, visuals and bookmarks in report
3. Create **groups of bookmarks** with desired configurations
4. **Create bookmarks navigators** for groups of bookmarks
5. **Insert** groups of bookmarks and its navigator in pages
6. Duplicate a page
7. Save changes **as a new report**

## Use case

0. The first thing to do is to instantiate a `PBIReport` object with desired PBIX file path

```python
pbix_file_path = r'path\to\your\report.pbix'

report = ppr.PBIReport(pbix_path=pbix_path)
```

After `PBIReport` object defined features can be used:

1. Read PBI report json as a python dictionary     
After reading the PBIX file, the ``layout_pbi_dict`` stores all Power BI layout settings as a python dictionary. Besides exploring the keys, all modification done in this dict could be consolidate as a new report.

```python
>>> print(report.layout_pbi_dict.keys())
dict_keys(['id', 'resourcePackages', 'sections', 'config', 'layoutOptimization'])

>>> for key in report.layout_pbi_dict.keys():
        print(type(report.layout_pbi_dict.get(key)))
<class 'int'>
<class 'list'>
<class 'list'>
<class 'str'>
<class 'int'>
```

2. Resume pages, visuals and bookmarks in report  
There are three methods to capture information on PBI report: ``resume_report_pages()``, ``resume_report_visuals()``, and ``resume_report_bookmarks()``. I would say that ``resume_report_visuals`` is the most important. This returns a pandas dataframe that could be filtered.

```python
>>> df_visuals = report.resume_report_visuals('Cover')
>>> print(tabulate(df_visuals))
+------------+----------------------+---------+---------------+----------------------+-------------------------------+--------+------------+----------+-------------+-----------+---------------+
| pagename   | visualid             | type    | displaymode   | position             | size                          | title  | subtitle   | fields   | groupname   | groupid   | pageid        |
|------------+----------------------+---------+---------------+----------------------+-------------------------------+--------+------------+----------+-------------+-----------+---------------|
| Cover      | ba11b203b4ce6a5c7490 | textbox | show          | {'x': 110, 'y': 56}  | {'width': 318, 'height': 56}  |        |            | {}       |             |           | ReportSection |
| Cover      | dfb0ef76dbaad8215b35 | shape   | show          | {'x': 110, 'y': 97}  | {'width': 357, 'height': 14}  |        |            | {}       |             |           | ReportSection |
| Cover      | 86673bea6b52652fd0e8 | image   | show          | {'x': 549, 'y': 126} | {'width': 180, 'height': 246} |        |            | {}       |             |           | ReportSection |
+------------+----------------------+---------+---------------+----------------------+-------------------------------+--------+------------+----------+-------------+-----------+---------------+
>>> df_filtered = df_visuals[df_visuals.type == 'shape']
>>> print(tabulate(df_filtered))
+------------+----------------------+--------+---------------+---------------------+------------------------------+--------+------------+----------+-------------+-----------+---------------+
| pagename   | visualid             | type   | displaymode   | position            | size                         | tile   | subtitle   | fields   | groupname   | groupid   | pageid        |
|------------+----------------------+--------+---------------+---------------------+------------------------------+--------+------------+----------+-------------+-----------+---------------|
| Cover      | dfb0ef76dbaad8215b35 | shape  | show          | {'x': 110, 'y': 97} | {'width': 357, 'height': 14} |        |            | {}       |             |           | ReportSection |
+------------+----------------------+--------+---------------+---------------------+------------------------------+--------+------------+----------+-------------+-----------+---------------+
```

3. Create groups of bookmarks with desired configurations  
Most part of the time, the buttons in Power BI report are created in pairs or groups of them. The function `create_group_of_bookmarks()` allows to create bookmarks in report just passing a dict of setting. For this, we should use `visualid` information delivered by `resume_report_visuals()`. After creation, it must be using insertion methods to really pass this to report layout dict.

```python
>>> button_group = {
...     'Button A':{
...         ppr.bookmarks.SHOW:['86673bea6b52652fd0e8'],
...         ppr.bookmarks.HIDE:['ba11b203b4ce6a5c7490']
...     },
...     'Button B':{
...         ppr.bookmarks.HIDE:['ba11b203b4ce6a5c7490'],
...         ppr.bookmarks.SHOW:['86673bea6b52652fd0e8']
...     }
... }
>>> bookgroup = report.create_group_of_bookmarks('Buttons A and B', book_group_config_dict=button_group)
>>> print(bookgroup)
('Bookmark4644f2b71269f48b63b6', {'displayName': 'Buttons A and B', 'name': 'Bookmark4644f2b71269f48b63b6', 'children':... )
```

5. Insert groups of bookmarks and its navigator in pages  
   After bookmarks or bookmarks navigator are created, it should be put in Power BI layout dict.

```python
>>> print(len(report.resume_report_bookmarks())) # bookmarks before
1 
>>> bookgroup = report.create_group_of_bookmarks('Buttons A and B', book_group_config_dict=button_group)
>>> report.insert_bookmark_in_page(ppr_bookmark=bookgroup)
>>> print(len(report.resume_report_bookmarks())) # bookmarks after
2
```

6. Save changes as a new report  
Is work done? Save it as a new report. Use the method `save_report()` to create and visualize your changes in a new file.

```python
>>> report.save_report()
'Sample Report ppr_out.pbix created in folder'
```

Explores more example in example folder.

## Licensing and Author 

Be free to use this module in your Power BI development and don't hesitate to contact me.

Ismael Miranda  
<ismaelmiranda11@hotmail.com>
