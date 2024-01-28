# <img src="./docs/source/_static/icon.png" alt="image" width="10%" height="auto"></img> Coding Power BI with Python 

- [ Coding Power BI with Python](#-coding-power-bi-with-python)
  - [What](#what)
  - [Installation and use](#installation-and-use)
  - [Why?](#why)
  - [Features](#features)
  - [Licensing and Author](#licensing-and-author)
  - [Versions](#versions)

## What

With this package, you can edit Power BI through coding.

## Installation and use

To use this module in Python, just install it with pip in the command line.

```
pip install pypbireport
```

In a Jupyter notebook or Python script, import the module. Using `ppr` is just a recommendation.

```python
import pypbireport as ppr
```

Instantiate a `PBIReport` or a `PBIModel` object and follow examples in [documentation use cases](https://py-powerbi-report.readthedocs.io/en/latest/userguide.html).

```python
report = ppr.PBIReport(pbix_path)
model = ppr.PBIModel(pbix_path)
```

More [in the documenation](https://py-powerbi-report.readthedocs.io/en/latest/index.html).

## Why?

Power BI report developing can become boring sometime. Get visuals in right place, modify pages and settings a lot of bookmarks (buttons) behavior in report. Puffs 😣  

I was lazy about doing this in the Power BI user interface. 🦥

I wonder one day having some way to **coding PBI reports layout**, so that I run a script and *voilà*, everything in its place.

So, here we are. This module for python does some of this work. Import it from your script, point out an existing PBIX file and [check what you can do](#features) and [some examples](https://py-powerbi-report.readthedocs.io/en/latest/userguide.html).

## Features

- **Modify visuals** in a Power BI report. 
- **Add visuals** and customize them. 
- **Add bookmarks** in a report to show and hide visuals. 
- Access the Power BI model and **add measures** to the model.

## Licensing and Author 

Be free to use this module in your Power BI development and don't hesitate to contact me.

Ismael Miranda  
<ismaelmiranda11@hotmail.com>

## Versions

| Version | Comment                                         |
| :------ | :---------------------------------------------- |
| 0.1     | Release                                         |
| 0.1.1   | Bug fix in create_bookmark_slicer() function    |
| 0.2     | Power BI Model and Power BI visual manipulation |
| 0.2.1   | Power BI Report peformance improvements         |