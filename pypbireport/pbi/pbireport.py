'''
PBI Report

Python 3.11.3
Developed by: Ismael Miranda
     E-mail : ismaelmiranda11@hotmail.com
'''
# import os
# import sys
# sys.path.append(os.path.dirname(os.getcwd()))

import json
import pandas as pd
import copy

from ..functions.functions import hex_code, get_str_dict, export_dict_as_file
from ..constants.structures import *
from ..constants import bookmarks
from ..constants import charts
from ..constants import shapes

from .pbifile import PBIXFile

class PBIReport(PBIXFile):
    '''
    Class to work with PBI report objects        
    '''
    def __init__(self, pbix_path:str) -> None:

        super().__init__(pbix_path=pbix_path)
        self.layout_pbi_dict = (
            json.loads
                (
                    self.extract_layout_and_encoding()
                )
        )
    
        self.save_changes()
        self.__list_pages()

        self.number_report_pages = len(self.pages_list)
        self.report_visuals = self.resume_report_visuals(page_name='')
        self.number_report_visuals = self.report_visuals.shape[0]

    def __repr__(self):
        _ = f"""
        {self.report_name}: {self.number_report_pages} pages,
        {self.number_report_visuals} visuals
        """
        return ' '.join(_.split())
    
        
    '''
    General functions of class
    '''
    def __list_pages(self):
        '''
        Input:
            None 
        Output:
            None

        Description:
            Create a list of all dict pages in report
        '''
        self.pages_list = self.layout_pbi_dict.get('sections')
        return None

    def __filter_page(self, page_name:str):
        '''
        Input:
            page_name (str): Page name which want to retrive. Default '' value
            retrive all pages.
        Output:
            page_filter_list (list): List of page filtered

        Description:
            Return a list of unique value with dict page from report.
        '''
        if page_name:
            page_filter_list = [page for page in self.pages_list if page.get('displayName')==page_name]
            if len(page_filter_list) == 0:
                raise ValueError(f'{page_name} was not found in report')
            else:
                return page_filter_list
        else:
            return self.pages_list
    
    def __get_report_of_visual(self, visual_id:str) -> str:
        '''
        Input:
            visual_id (str): The visual report id to get the page location.
        Output:
            page_id (str):

        Description:
            Return the page hexadecimal code of report which visual is in.         
        '''
        report_visuals_df = self.resume_report_visuals()

        page_id = (
            report_visuals_df
            .loc
            [   
                report_visuals_df
                .visualid == visual_id
            ]
            .pageid
            .iloc[0]
        )

        return page_id

    def __create_a_bookmark_dict(self, bookmark_name:str, books_dict:list):
        '''
        Input:
            bookmark_name (str):
            books_dict (list): 

        Output:
            name (type):

        Description:
            This function use a default json layout for bookmark and put values 
        from input
        '''
       
        # Get values from tag_dict
        report_section = list(books_dict.keys())[0]
        visual_list = books_dict.get(report_section)
        visual_id_list = [visual.get('visual') for visual in visual_list]
        
        book_default_dict = copy.deepcopy(BOOKMARK_DICT)

        # Update the infos in dict
        # Name and ID
        book_default_dict.update(
            {
                'displayName':bookmark_name,
                'name': hex_code('Bookmark')
            }
        )
        # Active report section
        (
            book_default_dict
            .get('explorationState')
            .update(
                {
                    'activeSection': report_section
                }
            )
        )

        # Create a dict for each visual with defined state
        for visual_dict in visual_list:
            visual_book_dict = {}

            visual_id = visual_dict.get('visual')
            book_ = visual_dict.get('displaymode')

            (
                visual_book_dict
                .update(
                    {
                        visual_id:{'singleVisual': {'display': {'mode': book_}}}
                    }
                )
            )
            # print(visual_book_dict)
            
            # Update the exemplo key in defalut dict
            (
                book_default_dict
                .get('explorationState')
                .get('sections')
                .get('exemplo')          
                .get('visualContainers')
                .update(visual_book_dict)      
            )
        
        # Change exemplo key to report section
        exemple_dict = (
            book_default_dict
            .get('explorationState')
            .get('sections').pop('exemplo')            
        )
        (
            book_default_dict
            .get('explorationState')
            .get('sections')
            .update({report_section:exemple_dict})
        )

        # Put new target names in targetVisualNames
        (
            book_default_dict
            .get('options')
            .get('targetVisualNames')
            .extend(list(set(visual_id_list)))
        )
                
        return book_default_dict

    '''
    Resume methods.

    These methods don't modify report content, just give information on report
    pages, visuals and bookmarks.
    '''
    def resume_report_pages(self):
        '''
        WIP
        Extract information from pages.
        Indicates the postion (ordinal) and name (displayName) in report.
        '''
        '''
        Input:
            var1 (type):
            var2 (type): 

        Output:
            name (type):

        Description:
            
        '''
        self.__list_pages()
        info_dict = {}

        for page_dict in self.pages_list:
            positon = page_dict.get('ordinal')
            display_name = page_dict.get('displayName')
            name = page_dict.get('name')
            
            info_dict.update({positon: [display_name,name]})

        # TODO: Put this in a dataframe
        
        return info_dict

    def resume_report_visuals(self, page_name : str ='', as_pd_dataframe : bool = True):
        '''
        WIP 
        Arguments
        Input:
            page_name (optional): name of page which wants visuals
        Output:
            info_dict: a python dict with page names and visual informations
        Description: 
            WIP
        '''
        '''
        Input:
            var1 (type):
            var2 (type): 

        Output:
            name (type):

        Description:
            
        '''
        self.__list_pages()

        # Colhendo a lista de visuais de cada página
        info_dict = {} # page is the key, list of visuals are the values
        for page in self.__filter_page(page_name):
            pagename_ = page.get('displayName')
            pageid_ = page.get('name')
            
            visual_info_list = [] # list of visual info dicts
            visual_group_dict = {} # group id is the key, group name is the value
            visual_list = page.get('visualContainers')

            # 1. Get groups in page
            for visual_dict in visual_list:
                visual_config_dict = get_str_dict(visual_dict, 'config')
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
                                 
                visual_config_dict = json.loads(visual_dict.get('config'))
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

                # if name_ == '65e4b299da705d515c2a':
                visual_info_dict = {
                        'py_tag':''
                        ,'visualid':visual_id_
                        ,'type':type_
                        ,'displaymode':displaymode_
                        ,'position':position_
                        ,'size':size_
                        ,'tile':title_
                        ,'subtitle':subtitle_
                        ,'fields':fields_                  
                        ,'groupname':group_name_
                        ,'groupid':group_id_
                        ,'pagename':pagename_
                        ,'pageid':pageid_
                    } 
            
                visual_info_list.extend([visual_info_dict])
                                
            (
                info_dict.update(
                    {
                        pagename_:visual_info_list
                    }
                )
            )    

        if as_pd_dataframe:
            _df = (
                (
                    pd.json_normalize
                    (
                        pd.DataFrame
                        ([info_dict])    
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
        else:
            return info_dict
    
    def resume_report_bookmarks(self):
        '''
        Bookmarks são uma lista
        A lista pode conter grupos de bookmarks ou bookmarks individuais,
        o campo children determina se é grupo ou é individual.
        explorationState sections ID_PAGINA visualContainers DA PAGINA
        As keys desse caminho entregam quais visuais o bookmark interage.
        Isso somente dentro dos bookmarks individuais.
        '''
        '''
        Input:
            var1 (type):
            var2 (type): 

        Output:
            name (type):

        Description:
            
        '''
        info_dict = {}

        # Transform the config string object into dict object
        config_str = self.layout_pbi_dict.get('config') # é um string
        config_dict = json.loads(config_str)
        # Get the list of bookmarks
        books_list = config_dict.get('bookmarks')

        # Some of bookmarks in the list are actually groups of bookmarks
        grouped_books_list = []
        individual_books_list = []
        for book_dict in books_list:
            if 'children' in book_dict:
                grouped_books_list.append(book_dict)
            else:
                individual_books_list.append(book_dict)

        # For each group, get the bookmarks
        grupos = []
        for group_dict in grouped_books_list:
            # Each group of bookmarks has childrens
            group_name = group_dict.get('displayName')
            group_id = group_dict.get('name')
            children_list = group_dict.get('children')

            children_books_info_dict = {}
            for child_dict in children_list:
                child_name = child_dict.get('displayName')
                
                child_pages_dict = child_dict.get('explorationState').get('sections')

                children_pages_visuals_info_dict = {}
                for page in child_pages_dict:
                    # page will be the keys of child_pages_dict
                    # Each page has a dict named 'visualContainers', which keys
                    # are visuals ids TODO: CHECAR ISSO AQUI!
                    visuals_list = ( 
                        list ( 
                            child_pages_dict
                            .get(page)
                            .get('visualContainers')
                            .keys()
                        )
                    )
                    children_pages_visuals_info_dict.update(
                        {
                           page:visuals_list
                        }
                    )

                children_books_info_dict.update(
                    {
                        child_name:children_pages_visuals_info_dict
                    }
                )  

            info_dict.update(
                {
                    f'{group_name}, {group_id}' : children_books_info_dict
                }
                )

        # Para os individuais, vai ser eles mesmos
        for individual in individual_books_list:
            book_name = individual.get('displayName')
            book_pages_dict = individual.get('explorationState').get('sections')

            book_pages_visuals_info_dict = {}
            for page in book_pages_dict:
                visuals_list = ( 
                        list ( 
                            book_pages_dict
                            .get(page)
                            .get('visualContainers')
                            .keys()
                        )
                    )
                book_pages_visuals_info_dict.update(
                    {
                        page:visuals_list
                    }
                )

            info_dict.update(
                {
                    book_name : book_pages_visuals_info_dict
                }
                )
        
        return info_dict

    '''
    Get methods.
    
    These methods allow to capture parts of layout dict as dict. 
    So, all modification done in returned varibles will be reflected in report
    after run dumps_changes().
    '''
    def get_report_visuals(self, visual_id: str | list)-> list:
        '''
        WIP
        Input: 
            visual_id: The visual id in report. 
                       Use resume_report_visuals() to see available options.
        Description
            Returns the visual dict in layout json.
            This allows modify visual in page.
            All modification in returned dict will be reflected in report
            after dump made. 
        
        '''
        '''
        Input:
            var1 (type):
            var2 (type): 

        Output:
            name (type):

        Description:
            
        '''
        if isinstance(visual_id, str):
            _visual_list = [visual_id]
        if isinstance(visual_id, list):
            _visual_list = visual_id
        
        visuals_list = []
        for page in self.pages_list:
            for visual_dict in page.get('visualContainers'):
                config_visual = get_str_dict(visual_dict, 'config')
                if config_visual.get('name') in _visual_list:
                    visuals_list.append(visual_dict)
        
        return visuals_list 

    '''
    Creation methods of class.

    These methods create report objects in dict forms. 
    The default returns of these methods are id and dict, witch should be
    insert into report through intertion methods.
    '''
    def create_group_of_bookmarks(self, 
        group_name:str,
        book_group_config_dict:dict
        ):
        '''
        WIP
        Input:
            group_name (str): Name of bookmark group

            book_group_config_dict: a dict with pattern 
                {   
                    'bookmar_name_1': {
                            ppr.bookmark.SHOW: [list of visual ids to show],
                            ppr.bookmark.HIDE: [list of visual ids to hide],
                        },
                    ...
                    'bookmar_name_n': {
                            ppr.bookmark.SHOW: [list of visual ids to show],
                            ppr.bookmark.HIDE: [list of visual ids to hide],
                        }
                }
        Output:
            bookmark_group_dict
        
        Description:
            Each key of bookmark_names_and_visual dict will be the name of 
            bookmark inside report.
            Each bookmark will be configured to show the visuals in list as value
            in bookmark_names_and_visual and hide the visuals from others lists
            in bookmark_names_and_visual
            For example:
                bookmark_names_and_visual = {
                    'Show column graph':['columngraphid', 'columngraphidtitleid'],
                    'Show bar graph':['bargraphid', 'bargraphidtitleid']
                }
                It will create two bookmarks in report:
                    1. Show column graph: this will show 'columngraphid', 
                       'columngraphidtitleid' and hide 'bargraphid', 
                       'bargraphidtitleid'
                    2. Show bar graph: this will show 'bargraphid', 
                       'bargraphidtitleid' and hide 'columngraphid', 
                       'columngraphidtitleid'
        '''
        '''
        Input:
            var1 (type):
            var2 (type): 

        Output:
            name (type):

        Description:
            
        '''
        
        # Transform the config string object into dict object
        # Get the list of bookmarks. At final, this list needed to be appended
        # with new group
                    
        # With tag_dict, create the dict of bookmark to append in books_list
        # As this a group will be created, first, create individualy each
        # bookmark to, so, create a bookmark group.
        
        # Transform bookmark_names_and_visual in a dict with visual, bookmar 
        # keys
        bookmark_list = []
        books_dict = {}
        for bookmark_name in book_group_config_dict:
            display_mode_dict = book_group_config_dict.get(bookmark_name)
            # 1. Show
            for visual_id in display_mode_dict.get(bookmarks.SHOW):
                report_id = self.__get_report_of_visual(visual_id)
                (
                    books_dict
                    .setdefault(report_id, [])
                    .append(
                        {
                        'displaymode':bookmarks.SHOW,
                        'visual':visual_id
                        }
                    )
                )
            # 2. Hide
            for visual_id in display_mode_dict.get(bookmarks.HIDE):
                pass 
                report_id = self.__get_report_of_visual(visual_id)
                (
                    books_dict
                    .setdefault(report_id, [])
                    .append(
                        {
                        'displaymode':bookmarks.HIDE,
                        'visual':visual_id
                        }
                    )
                )
                
            bookmark_list.append ( 
                self.__create_a_bookmark_dict (
                    bookmark_name=bookmark_name, 
                    books_dict=books_dict
                    )
            )
        
        # Now both books should be in children of group bookmark
        book_id = hex_code('Bookmark')
        group_dict = {        
                "displayName": group_name,
                "name": book_id,
                "children": bookmark_list
            }
        
        _id_, _dict_ =  book_id, group_dict
        
        return _id_, _dict_

    def create_bookmark_slicer(self, ppr_bookmark_or_group:tuple):
        '''
        WIP
        '''
        '''
        Input:
            var1 (type):
            var2 (type): 

        Output:
            name (type):

        Description:
            
        '''
        bookmark_slicer_dict = BOOKMARK_SLICER_DICT
        
        # 1. Assemble the condig dict
        _visual_id = hex_code()

        bookmark_slice_config_dict = BOOKMARK_SLICER_CONFIG_DICT
        (
            bookmark_slice_config_dict
            .get('layouts',[{}])
            [0]
            .get('position',{})
            .update(
                {
                    "x": bookmark_slicer_dict.get('x'),
                    "y": bookmark_slicer_dict.get('y'),
                    "z": bookmark_slicer_dict.get('z'),
                    "width":  bookmark_slicer_dict.get('width'),
                    "height": bookmark_slicer_dict.get('height'),
                    "tabOrder":  bookmark_slicer_dict.get('tabOrder')
                }
            )
        )
        
        (
            bookmark_slice_config_dict
            .get('singleVisual',{})
            .get('objects',{})
            .get('bookmarks',[])
            [0]
            .get('properties',{})
            .get('bookmarkGroup',{})
            .get('expr', {})
            .get('Literal', {})
            .update(
                {
                    "Value": f"\'{ppr_bookmark_or_group[0]}\'"
                }
            )
        )

        bookmark_slicer_dict.update(
            {'config':json.dumps(bookmark_slice_config_dict, ensure_ascii=False)}
        )

        _id_, _dict_ = _visual_id, bookmark_slicer_dict

        return _id_, _dict_
    
    def create_duplicate_page(self, page_name='Capa') -> None:
        '''
        TODO: change all ids in visual containers!
        WIP
        Input:
            displayName: Name in report to create a copy
        Output_
        Description:
            Sections contém uma list de dicts que representam as páginas.
            Para duplicar uma nova página no report, basta fazer um append de
            um dict que já existe dentro da lista de section.
            Esse processo é feito no próprio JSON de layout carregado.
        '''
        '''
        Input:
            var1 (type):
            var2 (type): 

        Output:
            name (type):

        Description:
            
        '''
                
        # Dentro de de páginas, retornar o dict que se deseja copiar
        page_to_duplicate_dict = self.__filter_page(page_name)[0]
        
        # Criar a página ao lado da original. Para isso, é necessário atualizar
        # os ordinals
        for page_dict in self.pages_list :
            ordinal_to_copy = page_to_duplicate_dict.get('ordinal')
            if page_dict.get('ordinal') > ordinal_to_copy:
                page_dict.update(
                    {
                        'ordinal': page_dict.get('ordinal') + 1
                    })

        # Agora, é necessário atualizar alguns valores.
        # name, displayName, ordinal precisam ser atualizados

        copy_of_page_dict = page_to_duplicate_dict.copy()
        copy_name = hex_code('ReportSection')
        copy_displayname = copy_of_page_dict.get('displayName') + ' py copy'
        copy_ordinal = copy_of_page_dict.get('ordinal') + 1
        # Update values in copy
        copy_of_page_dict.update(
            {
             'name':copy_name, 
             'displayName':copy_displayname,
             'ordinal':copy_ordinal
             }
        )

        # Append new page in page list
        self.pages_list.append(copy_of_page_dict)

        # Refresh number of pages
        self.number_report_pages += 1
        
        return None   
    
    '''
    Insertion methods.

    All visual or bookmarks created in class should be insert into layout dict.
    Just the objetcs inserted through theses methos will reflected in report
    after save_changes runs.
    '''
    def insert_visual_in_page(self, page_name:str, ppr_visual:tuple):
        '''
        Input:
            page_name (type):
            visual (type): 

        Output:
            name (type):

        Description:
            
        '''
        page_dict = self.__filter_page(page_name=page_name)[0]

        (
            page_dict
            .get('visualContainers')
            .append(ppr_visual[1])
        )  

        return None
    
    def insert_bookmark_in_page(self, bookmark:tuple):
        '''
        Input:
            bookmark (tuple): a tuple with (id, dict) of a bookmark create 
            in classe.
        Output:
            None

        Description:
            Insert a created bookmark.
        '''

        config_str = self.layout_pbi_dict.get('config') # é um string
        config_dict = json.loads(config_str)
        report_books_list = config_dict.get('bookmarks')

        report_books_list.append(bookmark[1])

        # Voltar para o string do config
        self.layout_pbi_dict.update(
            {
                'config':json.dumps(config_dict)
            }
        )

        return None

    '''
    Consolidation methods.

    These methods saves modifications in layout dict and create a new report
    file in the folder.
    '''
    def save_changes(self):
        '''
        Input:
            None 
        Output:
            None
        Description:
            Consolidate all changes made through classes methods in layout dict.
            This should run before sabe report to report reflect changes.
        '''
        self.layout_pbi_str = json.dumps(self.layout_pbi_dict)
        
        return 'All modification are in report.'

    def save_report(self, replace_original:bool=False, suffix:str='ppr_out'):
        '''
        Input:
            replace_original (bool): If is true, the original report will be 
            replaced for a report with modification. Important: the original 
            file should be closed.
            suffix (str): You might want a suffix to reports create by module. 
            The default is ppr_out.
        Output:
            None

        Description:
            Consolidate the report layout_dict input in a new PBIX file.
        '''

        # Garantee that all changes are in layout dict
        self.save_changes()

        return super().save_report(layout_dict = self.layout_pbi_str, 
                                   replace_original=replace_original, 
                                   suffix=suffix) 