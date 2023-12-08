'''Module for class to work with visualization in PBI

'''

import json
import pandas as pd
import copy

from ..functions.functions import hex_code
from ..functions.pprlist import PPRList
from ..constants.structures import *
from ..constants import bookmarks

from .pbifile import PBIXFile
from .pbivisual import *
from .pbibookmark import Bookmark, BookmarkGroup


class PBIReport(PBIXFile):    
    '''Class to represent a Power BI report

    Args:
        pbix_path (str): Path of the Power BI report file.
    
    Attributes:
        pbix_path (str): Path of the Power BI report file.
        layout_pbi_dict (dict): A python dict from report layout JSON
        layout_pbi_str (str): A string from report layout JSON
        pages_list (list): List of dicts representing report pages
        visuals (list): List of Visual objects of report
        pages_visuals (dict): A dict with the key as page name and the value as
            list of Visual objects of each page
        bookmark (list): List of Bookmark objects of the report
        bookmark_groups (list): List of BookmarkGroup objects of the report

    '''

    def __init__(self, pbix_path:str) -> None: 
        super().__init__(pbix_path=pbix_path)

        self.layout_pbi_dict : dict = (
            json.loads
                (
                    self.extract_layout_and_encoding()
                )
        )
        self.layout_pbi_str = json.dumps(self.layout_pbi_dict)

        # Get pages
        self.pages_list : list[dict] = self.__list_pages()

        # Get visuals
        self.visuals : PPRList = PPRList()
        self.pages_visuals : dict = {}
        self.__list_visuals()

        # Get bookmarks
        self.bookmarks : PPRList = PPRList()
        self.bookmark_groups : PPRList = PPRList()
        self.__list_bookmarks()

    def __repr__(self) -> str:
        _ = f"""
        {self.report_name}: 
        {len(self.pages_list)} pages and 
        {len(self.visuals)} visuals
        """
        return ' '.join(_.split())

    def __list_pages(self) -> list[dict]:
        ''''''
        self.pages_list = self.layout_pbi_dict.get('sections', [{}])

        return self.pages_list

    def __list_visuals(self)-> None:
        ''''''

        info_dict : dict = {}
        
        self.visuals : PPRList = PPRList()
        
        for page in self.pages_list:
            page_name = page.get('displayName')
            page_id = page.get('name')
            info_dict.setdefault(page_name, PPRList())
        
            visuals_list = PPRList()
            
            for visual_dict in page.get('visualContainers', {}):
                visual = VisualInitializer(
                    Visual(visual_dict, page_name, page_id)
                )
                self.visuals.append(visual)
                visuals_list.append(visual)
            
            info_dict.get(page_name).extend(visuals_list) # type: ignore
        
        self.pages_visuals = info_dict

        return None

    def __list_bookmarks(self):
        '''Method to initiate bookamrks list in class

        Bookmarks are placed in the `config` field of the layout dict. The key 
        `bookmarks` contains both single bookmaks and bookmark groups.

        Returns:
            None. Assign Bookmakrs object to bookmarks_list variable.
        '''

        def _create_bookmark_obj(bookmark_dict:dict) -> Bookmark:           
            '''Method to create a Bookmark object from report layout JSON

            Starting from config.bookmarks path that came from report layout 
            dict, this function extract main informations from bookmarks in 
            oder to generate a Bookmark object. 

            Args:
                bookmark_dict (dict): Bookmark key from report layout dict

            Returns:
                Bookmark: A Bookmark object
            '''            
            active_section = (
                bookmark_dict
                .get('explorationState', {})
                .get('activeSection')
            )
            visual_containers_dict = (
                bookmark_dict
                .get('explorationState', {})
                .get('sections', {})
                .get(active_section, {})
                .get('visualContainers')
            )
            targets = (
                bookmark_dict
                .get("options", {})
                .get("targetVisualNames", [])
            )
            
            show_visuals = PPRList()
            hide_visuals = PPRList()
            for visual_id, visual_dict in visual_containers_dict.items():
                if visual_id in targets:
                    mode = ( 
                        visual_dict
                        .get('singleVisual', {})
                        .get('display', {'mode': bookmarks.SHOW}) #if none,show
                        .get('mode')
                    )
                    if mode == bookmarks.SHOW:
                        show_visuals.append(self.visuals[visual_id])
                    elif mode == bookmarks.HIDE:
                        hide_visuals.append(self.visuals[visual_id])
            
            return Bookmark(
                    bookmark_name=bookmark_dict.get('displayName', ''),
                    id=bookmark_dict.get('name', ''),
                    show_visuals=show_visuals,
                    hide_visuals=hide_visuals
                )
        
        # Both single bookmarks and group are present in the bookmarks key
        report_bookmarks_list = (
            json.loads( #config is a string as came from JSON
                self.layout_pbi_dict
                .get("config", "{}") #avoid errors for clean reports
            )
            .get('bookmarks', []) #get bookmarks key from there
        )

        # Initiate the lists
        self.bookmarks = PPRList()
        self.bookmark_groups = PPRList()

        # Run over the dicts of bookmarks in bookmark list
        for report_bookmark_dict in report_bookmarks_list:
            # If there is a children key, then it is a group of bookmarks
            if report_bookmark_dict.get('children'):
                # Run over the inner bookmarks and get their dicts
                group_children = PPRList()
                for book_dict_inner in report_bookmark_dict.get('children'):
                    self.bookmarks.append(
                        _create_bookmark_obj(book_dict_inner)
                    )
                    group_children.append(
                        _create_bookmark_obj(book_dict_inner)
                    )
                self.bookmark_groups.append(
                    BookmarkGroup(
                    bookmark_group_name=report_bookmark_dict.get('displayName')
                    ,id=report_bookmark_dict.get('name'),
                    children_list=group_children
                    )
                )
            else:    
                # If it`s not a group, just append it to list
                self.bookmarks.append(
                    _create_bookmark_obj(report_bookmark_dict)
                )
        
        return None

    def __filter_page(self, page_name:str):
        '''Return a list of unique value with dict page from report
        
        Args:
            page_name (str): Page name which want to retrieve
        
        Returns:
            page_filter_list (list): List of page filtered
            
        '''
        # List of pages with page_name filtered
        page_filter_list = [
            page 
            for page in self.pages_list 
            if page.get('displayName', '')==page_name 
        ]

        if len(page_filter_list) == 0:
            raise ValueError(f'{page_name} was not found in report')
        else:
            return page_filter_list

    '''
    Resume methods.

    These methods don't modify report content, just give information on report
    pages, visuals and bookmarks.
    '''
    def resume_report_pages(self):
        '''This method return a dict with page information
        
        Returns:
            info_dict (dict): A dict with page position, display name and id.
        '''

        self.__list_pages()
        info_dict = {}

        for page_dict in self.pages_list:
            position = page_dict.get('ordinal')
            display_name = page_dict.get('displayName')
            name = page_dict.get('name')
            
            info_dict.update({position: [display_name,name]})
        
        return info_dict

    def resume_report_visuals(self, page_name : str ='') -> pd.DataFrame:        
        '''Method to return a dataframe of information of visuals in report
        
        Args:
            page_name (str): The page name that desire retrieve visuals of. 
            
        Returns:
            pd.DataFrame: A dataframe with all report visuals
            
        '''
        self.__list_pages()

        info_dict = {} # page is the key, list of visuals are the values

        if page_name:
            page_list = self.__filter_page(page_name)
        else:
            page_list = self.pages_list

        for page in page_list:
            pagename_ = page.get('displayName')
            pageid_ = page.get('name')
            
            visual_info_list = [] #list of visual info dicts
            visual_group_dict = {} #group id is the key,group name is the value
            visual_list = page.get('visualContainers', [])

            # 1. Get groups in page
            for visual_dict in visual_list:
                # visual_config_dict = get_str_dict(visual_dict, 'config')
                visual_config_dict = visual_dict['config']
                is_a_group = visual_config_dict.get('singleVisualGroup', False)
                if is_a_group:
                    group_id_ = (
                        visual_config_dict
                        .get('name')
                    )
                    group_name_ = (
                        visual_config_dict
                        .get('singleVisualGroup')
                        .get('displayName')
                    )
                    visual_group_dict.update({group_id_:group_name_})

            # 2. Run over all visual
            for visual_dict in visual_list:
                                 
                # visual_config_dict = json.loads(visual_dict.get('config'))
                visual_config_dict = visual_dict.get('config')
                visual_id_ = visual_config_dict.get('name')
                type_ = (
                    visual_config_dict
                    .get('singleVisual', {})
                    .get('visualType', None) 
                )
                position_ = {
                    k:int(val) 
                    for k,val in 
                        (
                            visual_config_dict
                            .get('layouts', [{}])
                            [0]
                            .get('position', None) 
                        ).items() 
                    if k in ('x','y')
                }
                size_ = {
                    k:int(val) 
                    for k,val in 
                        (
                            visual_config_dict
                            .get('layouts', [{}])
                            [0]
                            .get('position', None) 
                        ).items() 
                    if k in ('width','height')
                }
                title_ = (
                    visual_config_dict
                    .get('singleVisual', {})
                    .get('vcObjects', {}) 
                    .get('title', [{}])
                    [0]
                    .get('properties', {})
                    .get('text', {})
                    .get('expr', {})
                    .get('Literal', {})
                    .get('Value', '')
                    [1:-1]
                )
                subtitle_ = (
                    visual_config_dict
                    .get('singleVisual', {})
                    .get('vcObjects', {}) 
                    .get('subTitle', [{}])
                    [0]
                    .get('properties', {})
                    .get('text', {})
                    .get('expr', {})
                    .get('Literal', {})
                    .get('Value', '')
                    [1:-1]
                )             
                

                group_id_ = (
                    visual_config_dict
                    .get('parentGroupName', '')
                )

                group_name_ = visual_group_dict.get(group_id_, '')
                
                projections_dict = (
                    visual_config_dict
                    .get('singleVisual', {})
                    .get('projections', {})
                )

                fields_ = {
                    k: 
                        [
                            cat.get('queryRef', '')
                            for cat in projections_dict.get(k, [{}])
                        ]
                    
                    for k in projections_dict
                }

                displaymode_ = (
                    visual_config_dict
                    .get('singleVisual', {})
                    .get('display', {})
                    .get('mode', 'show')
                )

                visual_info_dict = {
                        # 'py_tag':''
                        'visualid':str(visual_id_)
                        ,'type':type_
                        ,'displaymode':displaymode_
                        ,'position':position_
                        ,'size':size_
                        ,'title':title_
                        ,'subtitle':subtitle_
                        ,'fields':fields_
                        ,'groupname':group_name_
                        ,'groupid':group_id_
                        ,'pagename':pagename_
                        ,'pageid':pageid_
                    } 
            
                visual_info_list.extend([visual_info_dict])

                          

            info_dict.update(
                {
                    pagename_:visual_info_list
                }
            )


        _df = (
            (
                pd.json_normalize(
                    pd.DataFrame([info_dict]) # type: ignore
                    .T
                    .rename(columns={0:'data'})
                    .explode('data').data
                    , 
                    max_level = 0 
                )
            )
            .set_index('pagename')
        )

        return _df

    
    '''
    Creation methods of class.

    These methods create report objects in dict forms. 
    The default returns of these methods are id and dict, witch should be
    insert into report through insertion methods.
    '''

    def create_duplicate_page(self,page_to_duplicate:str, 
        page_name:str = 'ppr copy') -> None:
        '''This method duplicates a page in report

        Args:
            page_name (str): The page to duplicate.

        '''
                
        page_to_duplicate_dict = self.__filter_page(page_to_duplicate)[0]
        
        copy_of_page_dict = copy.deepcopy(page_to_duplicate_dict)

        # Update values in copy
        copy_of_page_dict.update(
            {
             'name':hex_code('ReportSection'), 
             'displayName':page_name,
             'ordinal': copy_of_page_dict.get('ordinal', None) + 1
             }
        )

        # Update visuals ids
        for visual in copy_of_page_dict.get('visualContainers', {}):
            Visual(visual).id = hex_code()

        # Update ordinal of pages after page_to_duplicate
        for page_dict in self.pages_list :
            ordinal_to_copy = page_to_duplicate_dict.get('ordinal')
            if page_dict.get('ordinal', None) > ordinal_to_copy:
                page_dict.update(
                    {
                        'ordinal': page_dict.get('ordinal', None) + 1
                    }
                )

        # Append new page in page list
        self.pages_list.append(copy_of_page_dict)
        
        return None   
    
    '''
    Insertion methods.

    All visual or bookmarks created in class should be insert into layout dict.
    Just the objects inserted through theses method will reflected in report
    after save_changes runs.
    '''
    def insert_visual_in_page(self, page_name:str, visual: tuple | Visual):
        '''Insert a visual in a page.

        Args:
            page_name (str): The page name where the visual will be.
            visual (tuple | Visual): A tuple of __id__ and __dict__ from a 
                visual created with this class.
        '''

        if isinstance(visual, tuple):
            _ppr_visual = visual[1] 
        elif isinstance(visual, Visual.__bases__):
            _ppr_visual = visual.visual
        else:
            _ppr_visual = None


        page_dict = self.__filter_page(page_name=page_name)[0]

        (
            page_dict
            .get('visualContainers', {})
            .append(_ppr_visual)
        )  

        self.__list_visuals()

        return None
    
    def insert_bookmark(self, 
        ppr_bookmark: tuple | Bookmark | BookmarkGroup
        ):
        '''Insert a bookmark into report.

        Insert a created bookmark.
        Different from others parameters in layout JSON of PBI, the bookmarks 
        are placed at 'config' key at the end of JSON. It is a kind of
        overall configuration of report.

        Args:
            bookmark (tuple): a tuple with (id, dict) of a bookmark create 
            in class.
        
        Returns:
            None
        '''
        if isinstance(ppr_bookmark, tuple):
            _ppr_bookmark = ppr_bookmark[1] 
        elif ( 
            isinstance(ppr_bookmark, Bookmark.__bases__) 
            or isinstance(ppr_bookmark, BookmarkGroup.__bases__) 
            ):
            _ppr_bookmark = ppr_bookmark.bookmark_dict
        else:
            _ppr_bookmark = None

        config_str = self.layout_pbi_dict.get('config', {}) 
        config_dict = json.loads(config_str)

        report_books_list = config_dict.setdefault('bookmarks',[])
        report_books_list.append(_ppr_bookmark)

        self.layout_pbi_dict.update(
            {
                'config':json.dumps(config_dict)
            }
        )

        self.__list_bookmarks()

        return None

    '''
    Consolidation methods.

    These methods saves modifications in layout dict and create a new report
    file in the folder.
    '''
    def save_changes(self):
        '''Consolidate all changes made through classes methods in layout dict.
            
        This should run before save_report() to report reflect changes.
                    
        '''

        # Refresh the visual list
        self.__list_visuals()
        # Dump all dicts
        for visual in self.visuals:
            visual.dump_dicts()
        
        # Dump layout dict
        self.layout_pbi_str = json.dumps(self.layout_pbi_dict, 
                                         ensure_ascii=False)
        
        # Refresh the visual list again, to keep visuais as Visual type, 
        # instead of string
        self.__list_visuals()

        return 'All modification are in report.'

    def save_report(self, replace_original:bool=False, suffix:str='ppr_out', 
        file_name:str|None=None, open_file=False):
        '''Consolidate the report layout_dict input in a new PBIX file
        
        Args:
            replace_original (bool, optional): If is true, the original report
                will be replaced for a report with modification. The original 
                file should be closed. Defaults to False.
            suffix (str, optional): You might want a suffix to reports create 
                by module. Defaults to 'ppr_out'.
            file_name (str | None, optional): Desired report file name. 
                Defaults to None.
            open_file (bool, optional): Not implemented. Defaults to False.
        '''

        # Guarantee that all changes are in layout dict
        self.save_changes()

        # Saving report
        super().save_report(layout_dict = self.layout_pbi_str, 
                                   replace_original=replace_original, 
                                   suffix=suffix,
                                   file_name=file_name,
                                   open_file=open_file)