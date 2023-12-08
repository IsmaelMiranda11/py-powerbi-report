==============
Code Reference
==============

Here is the documentation of py-powerbi-report code.

There are two parts of power bi objects, one that works with the report (visuals and bookmarks) and another to work with the model (measures).


Power BI Report classes
=======================

PBIXFile
---------

.. automodule:: pypbireport.pbi.pbifile
    :members:
    :member-order: bysource
    :undoc-members:

PBIReport
---------

.. automodule:: pypbireport.pbi.pbireport
    :members:
    :member-order: bysource
    :undoc-members:

PBIVisual
---------

.. autoclass:: pypbireport.pbi.pbivisual.Visual
    :members: 
    :member-order: 
    :undoc-members:

.. automethod:: pypbireport.pbi.pbivisual.create_new_visual

.. automethod:: pypbireport.pbi.pbivisual.copy_visual

Specific Visuals
^^^^^^^^^^^^^^^^

.. automodule:: pypbireport.pbi.pbivisual
    :members: BaseVisual, Card, Column, Slicer, BookmarkSlicer
    :member-order: bysource
    :undoc-members:
    :no-index:

Power BI Model classes
=======================

.. automodule:: pypbireport.pbi.pbimodel
    :members:
    :member-order: bysource
    :undoc-members: