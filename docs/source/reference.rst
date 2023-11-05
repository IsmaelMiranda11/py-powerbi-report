Code Reference
==============

Here is the documentation of py-powerbi-report code.  

PBIX File
---------

The first module is for to handle PBIX files.
The layout of a Power BI report comes from a JSON file name ``Layout`` inside the ``.pbix`` file.
This is an example of:

The class ``PBIXFile`` means capture the file and delivery it for ``PBIReport``
class to work with.

.. automodule:: pypbireport.pbi.pbifile
    :members:
    :member-order: bysource
    :undoc-members: