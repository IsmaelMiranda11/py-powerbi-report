'''
version 0.1
Python 3.11.3

Developed by: Ismael Miranda
     E-mail : ismaelmiranda11@hotmail.com

Features:
    Use class PBIReport to:
        1. Read layout json as a Python dictionary
        2. Resume pages, visuals and bookmarks in report
        3. Create groups of bookmarks with desired configurations
        4. Create bookmarks navigators for groups of bookmarks
        5. Insert groups of bookmarks and its navigator in pages
        6. Duplicate a page
        7. Save changes as a new report
'''

__version__ = '0.1'

import os 
import sys
sys.path.append(os.path.dirname(__file__))

from .pbi.pbireport import PBIReport

from .constants import bookmarks
from .constants import charts
from .constants import shapes
from .functions.functions import export_dict_as_file