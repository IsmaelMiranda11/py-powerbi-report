<!-- .. pypbireport documentation master file, created by
   sphinx-quickstart on Sat Oct 14 18:01:54 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive. -->



# Python Power BI Report libary

<img src="./_static/icon.png" alt="image" width="10%" height="auto"></img>
Welcome to `pypbireport` documentation.  

## Quick start:

```
pip install pypbireport
```
```python
import pypbireport as ppr
report = ppr.PBIReport(pbix_path)
model = ppr.PBIModel(pbix_path)
```

## What

With **pypbireport**, you can:  
- **Modify visuals** in a Power BI report. 
- **Add visuals** and customize them. 
- **Add bookmarks** in a report to show and hide visuals. 
- Access the Power BI model and **add measures** to the model.  

All of this can be done with Python scripting in plain text or in Jupyter notebooks.

This python package provides an interface for Power BI developing by python.

[Get started](#getstarted) and check some [uses case](#userguide).

## Why

Power BI report developing can become boring sometime. Get visuals in right place, modify pages and settings a lot of bookmarks (buttons) behavior in report. Puffs 😣  

I was lazy about doing this in the Power BI user interface. 🦥

I wonder one day having some way to **coding PBI reports layout in python**, so that I run a script and *voilà*, everything in its place. This package is the result of my willing.

## Licensing and Author 

Be free to use this module in your Power BI development and don't hesitate to contact me. Ismael Miranda (<ismaelmiranda11@hotmail.com>)

## Versions

| Version | Comment                                                       |
| :------ | :------------------------------------------------------------ |
| 0.1     | Release                                                       |
| 0.1.1   | Bug fix in create_bookmark_slicer() function                  |
| 0.2     | Power BI model acess and new objects for visual and bookmarks |
| 0.2.1   | Power BI Report peformance improvements                       |


## Contents:

```{toctree}
:maxdepth: 3

getstarted
userguide.ipynb
reference
```

Indice
--------

[Index](#genindex)