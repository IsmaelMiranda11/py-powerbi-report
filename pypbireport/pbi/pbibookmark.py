
from ..constants import bookmarks
import copy

from ..functions.functions import hex_code
from ..functions.pprlist import PPRList

from ..constants.structures import BOOKMARK_DICT
from ..constants import bookmarks

from .pbivisual import Visual

class Bookmark(object):
    """Class to represent a bookmark in PBI report

    """
    '''
        1. Criar um corpo de bookmark para ser adicionado no config da página
        2. Cada bookmark tem que ser criado individualmente. 
        3. Bookmarks podem ser agrupados para criar os slicers. Mas por ordem, 
           primeiro cria-se bookmark e depois adiciona-se no grupo. (Isso que
           estava programado no create_a_bookmark_group)
        
        Criar um corpo de bookmark
            1. Informações essenciais:
                ReportSection;
                TargetVisuals
                1.1 ReportSection.
                    a. explorationState, activeSection. Determina qual a página 
                       que o bookmark afeta
                    b. explorationState, activeSection, sections, ReportSection.
                       Aqui ela recebe um dict de visual e o modo que ele aparecerá.
                1.2 TargetVisuals.
                    a. explorationState, activeSection, sections, ReportSection,
                       TargetVisual. Cada visual tem que ser colocado nesse dict
                       com a configuração 
                       visual_id:{'singleVisual': {'display': {'mode': ''}}}.
                       O modo de display será escolhido para como o bookmark vai afetar
                       cada visual.
                    b. options, targetVisualNames. Simples lista dos visuais que
                       o bookmark afeta.
    '''

    def __init__(self, bookmark_name:str, 
        show_visuals:list[Visual],
        hide_visuals:list[Visual],
        target_visuals:list[Visual]=[],
        id: str | None=None,
        group_name: str | None = None,
        group_id: str | None = None,
        ):
        
        # Just initiate a bookmark with a name
        self.name = bookmark_name

        # A list of tareget visuals. Should be a Visual class object.
        self.show_visuals = show_visuals
        self.hide_visuals = hide_visuals
        # Target visuals is really optional. If it is not input, then populate
        if not target_visuals:
            self.target_visuals = show_visuals + hide_visuals

        # Get ReportSection from visuals
        report_section = []; report_section_name = []
        for visual in self.target_visuals:
            # print(visual)
            report_section.append(
                visual.page_id
            )
            report_section_name.append(
                visual.page_name
            )
        self.report_section = ''
        self.report_section_name = ''
        if report_section:
            self.report_section = list(set(report_section))[0]
        if report_section_name:
            self.report_section_name = list(set(report_section_name))[0]
        
        self.bookmark_dict = copy.deepcopy(BOOKMARK_DICT)
        
        # Visual containers dict will hold all dict of display mode of visual
        # This should be added in sections in the end.
        self.visual_containers = {}

        self.__update_report_section()    
        self.__create_visuals_dict()
        self.__update_target_visuals()
        self.__update_sections()

        if id:
            self.id = id
            self.bookmark_dict.update(
                {
                    'name': id
                }
            )
        else:
            self.id = self.bookmark_dict.get('name')
        

            
    def add_target_visual(self, visual:Visual, display_mode=bookmarks.SHOW):
        pass
    
    def __update_report_section(self):
        self.bookmark_dict.update(
            {
                'displayName':self.name,
                'name': hex_code('Bookmark')
            }
        )
        # Active report section
        (
            self.bookmark_dict
            .get('explorationState', {})
            .update(
                {
                    'activeSection': self.report_section
                }
            )
        )
        # Erase the exemplo key, if exists
        try:
            (
                self.bookmark_dict
                .get('explorationState', {})
                .get('sections').pop('exemplo')
            )
        except:
            pass
        pass 
    
    def __create_visuals_dict(self):
        # For each visual in list, get the id and set display to show

        for visual in self.show_visuals:
            self.visual_containers.setdefault(visual.id, {})
            self.visual_containers.update(
                {
                    visual.id:{'singleVisual': {'display': {'mode': bookmarks.SHOW}}}
                }
            )
        for visual in self.hide_visuals:
            self.visual_containers.setdefault(visual.id, {})
            self.visual_containers.update(
                {
                    visual.id:{'singleVisual': {'display': {'mode': bookmarks.HIDE}}}
                }
            )
        pass

    def __update_target_visuals(self):
        for visual in self.target_visuals:
            (
                self.bookmark_dict
                .get('options', {})
                .get('targetVisualNames', [])
                .append(visual.id)
            )
        pass 

    def __update_sections(self):
        report_section_dict = {
            self.report_section:
                {
                    'visualContainers':self.visual_containers
                }
        }

        (
            self.bookmark_dict
            .get('explorationState', {})
            .get('sections')
            .update(report_section_dict)
        )

        pass

    def __repr__(self) -> str:
        _ = f'''
        Bookmark(
        id: '{self.id}' |
        name: {self.name} |
        page: {self.report_section_name} |
        show: {[v.id for v in self.show_visuals]} |
        hide: {[v.id for v in self.hide_visuals]}
        )
        '''
        return ' '.join(_.split())

class BookmarkGroup():
    ''''''

    def __init__(self, bookmark_group_name:str,
        children_list:list[Bookmark],
        id:str|None = None
        ) -> None:

        self.bookmark_group_name = bookmark_group_name        
        self.children_list = children_list
        
        self._create_book_group_dict()

        if id:
            self.id = id
        else:
            self.id = self.bookmark_dict.get('name')

        self.target_visuals = self.__get_targets_visuals()
        
        report_section_name = []
        for bookmark in self.children_list:
            report_section_name.append(
                bookmark.report_section_name
            )
        self.report_section_name = list(set(report_section_name))[0]
    
    def _create_book_group_dict(self):
        ''''''
        # A group of bookmarks is a simple dict with three fields.    
        
        self.bookmark_dict = {        
                "displayName": self.bookmark_group_name,
                "name": hex_code('Bookmark'),
                "children": [b.bookmark_dict for b in self.children_list]
            }    
           
        return None

    def __get_targets_visuals(self):
        target_visual_list = PPRList()
        for bookmark in self.children_list:
            target_visual_list.extend(bookmark.target_visuals)
        
        return target_visual_list

    def __repr__(self) -> str:
        _ = f'''
        Bookmark(
        id: \'{self.id}\' |
        name: {self.bookmark_group_name} |
        page: {self.report_section_name} |
        bookmarks_id: {[v.id for v in self.children_list]} |
        bookmarks_name: {[v.name for v in self.children_list]} |
        visuals: {[v.id for v in self.target_visuals]}
        )
        '''
        return ' '.join(_.split())
