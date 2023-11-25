'''pypbireport version 0.3

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

__version__ = '0.3'

import os 
import sys
sys.path.append(os.path.dirname(__file__))

from .pbi.pbifile import (
    PBIXFile
)

from .pbi.pbireport import (
    PBIReport
)

from .pbi.pbivisual import (
    Visual,
    create_new_visual
)

from .pbi.pbibookmark import (
    Bookmark,
    BookmarkGroup
)

from .pbi.pbimodel import (
    PBIModel,
    Measure,
    Column,
    Table
)

from .constants import (
    bookmarks,
    charts,
    shapes,
    dax_code
)

from .functions.functions import export_dict_as_file
from .functions.pprlist import PPRList