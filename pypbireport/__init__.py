'''
Python 3.11.3
Developed by: Ismael Miranda
     E-mail : ismaelmiranda11@hotmail.com

 "I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it.", Bill Gates.
 Yeah, I was so lazy on build PBI report.

 Features:
    Use class PBIXReport to:
        1. Read layout json as a Python dictionary
        2. Resume pages, visuals and bookmarks in report
        3. Create groups of bookmarks with desired configurations
        4. Create bookmarks navigators for groups of bookmarks
        5. Insert groups of bookmarks and its navigator in pages
        6. Duplicate a page
        7. Save changes as a new report
'''

import os 
import sys
sys.path.append(os.path.dirname(__file__))

from .pbi.pbireport import PBIReport

from .constants import bookmarks
from .constants import charts
from .constants import shapes