
'''Module for class to work with visuals of Power BI
'''
import json
import copy
import re
from jsonpath_ng.ext import parse

from typing import Literal

from ..functions.functions import hex_code
from ..constants.structures import *
from ..constants import charts
from ..functions.pprlist import PPRList

from .pbimodel import Measure


class Visual(object):
    '''Class to represent a visual in PBI.

    Two types of input are accepted: dict or string.
    If dict, it must be a visual dict from report layout dict.
    If string, it must be a visual type from VISUAL_TEMPLATE_DICT.

    '''
    # Propeties of visual and its path inside dict
    dict_attrs_path = {
        'id': ['config', 'name'],
        'x': ['config', 'layouts','position','x'],
        'y': ['config', 'layouts','position','y'],
        'height': ['config','layouts','position','height'],
        'width': ['config','layouts','position','width'],
        'type_': ['config','singleVisual','visualType'],
        'title': ['config','singleVisual', 'vcObjects', "title", "properties", "text", "expr","Literal", "Value"],
        'title_align': ['config','singleVisual', 'vcObjects', "title", "properties", "alignment",  "expr", "Literal", "Value"],
        'title_fontsize': ['config','singleVisual', 'vcObjects', "title", "properties", "fontSize", "expr", "Literal", "Value"],
        'font_size': ["config", "singleVisual", "objects", "labels", "properties", "fontSize", "expr", "Literal", "Value"],
        'format_conditional': ['config','singleVisual', 'objects', "labels", "properties",'color', 'solid', 'color', 'expr', 'Measure', 'Property'],
        'measure': ['config','singleVisual', 'projections', "Values", "queryRef"],
        'fc_card': ['config', 'singleVisual', 'objects', "labels", "properties",'color', 'solid','color', 'expr', 'Measure', 'Property'],
        'field_card': ['config','singleVisual','projections','Values','queryRef'],
        'field_y_column': ['config', 'singleVisual', 'projections', 'Y', 'queryRef'],
        'field_category_column_n1': ['config', 'singleVisual', 'projections', 'Category', 'queryRef'],
        'field_category_column_n2': [''],
        'field_slicer': ['config','singleVisual','projections','Values','queryRef'],
        'bookmark_group': ['config', 'singleVisual','objects','bookmarks','properties','bookmarkGroup','expr','Literal','Value']
    }
 
    dict_mod_path = {
        'x': [['x']],
        'y': [['y']],
        'height': [['height']],
        'width': [['width']],
        'font_size': [['dataTransforms', 'objects', 'labels', 'properties', 'fontSize', 'expr', 'Literal', 'Value']]
    }

    dict_fields = {
        'field_card': {'table': 'Métricas', 'field': 'Categorica'}, 
        'fc_card': {'table': 'Reporting Layout', 'field': 'Formatação Condicional'},
        'field_y_column': {'table': 'Métricas', 'field': 'Categorica'},
        'field_category_column_n1': {'table': 'Calendário', 'field': 'Ano Ciclo'},
        'field_category_column_n2': {'table': 'Calendário', 'field': 'Data'},
        'field_slicer': {'table': 'Campanhas', 'field': 'Tipo de Campanha'},
    }

    def __init__(self, 
        visual_dict: dict | Literal['card', 'column', 'slicer_drop', 
            'slicer_list', 'bookmark_slicer'], 
        page_name: str | None ='',
        page_id: str | None = '',
        custom_template_visual_dict: dict | None = None 
    ) -> None:
        '''__init__ doc'''
        # self.id = ''
        # self.x = 0
        # self.y = 0
        # self.height = 0
        # self.width = 0
        # self.type_ = None

        # If input is a string, it must be a visual type from VISUAL_TEMPLATE_DICT
        if visual_dict in ['card', 'column', 'slicer_drop', 'slicer_list', 'bookmark_slicer']:
            if custom_template_visual_dict:
                _visual_dict = copy.deepcopy(custom_template_visual_dict)
            else:
                _visual_dict = copy.deepcopy(
                    charts.VISUAL_TEMPLATE_DICT.get(visual_dict, {})
                )
            
            # Assign a new hex code
            ( 
                _visual_dict
                .update(
                    {
                        'config':json.loads(_visual_dict['config'])
                    }
                )
            )
            (
                _visual_dict
                .get('config', {})
                .update(
                    {
                        'name':hex_code()
                    }
                )
            )
            
        elif isinstance(visual_dict, dict):
            # If input is a dict, it must be a visual dict from report layout dict
            _visual_dict = visual_dict
        else:
            raise ValueError("It must be a dict as input")

        # Deepcopy just in case, for existing visuals
        self.original_visual = copy.deepcopy(_visual_dict)
        # Get visual dict
        self.visual = _visual_dict
            
        # Page name
        self.page_name = page_name
        self.page_id = page_id

        # Convert to dict object in __setattrs__
        self.config = self.visual.get('config', "{}")
        self.query = self.visual.get('query', "{}")
        self.dataTransforms = self.visual.get('dataTransforms', "{}")
        
        # Setting all properties as attributes
        # Here, all of attributes are setted as indicated in dict_attrs_path
        for attrs in self.dict_attrs_path:
            (
                object
                .__setattr__(
                    self, 
                    attrs, 
                    self.__get_dict_path_value(self.dict_attrs_path[attrs])
                )
            )
        
        
            
    def __setattr__(self, __name, __value):
        '''
        Using object to manipulate some behavoir of visual atributes
        '''
        # Loads strings in layout dict as a dict
        # When save_report is used, the method dump_dicts is called to dump
        # as string again

        # For these three attributes, convert to dict, since it is a string in
        # original dict. 
        # This only matters when a new visual is created!
        if __name in ['config', 'query', 'dataTransforms']:
            # 1. Convert to dict
            if isinstance(__value, str):
                dict_value = json.loads(__value)
            else:
                dict_value = __value                
            # 2. Set attribute
            (
                object
                .__setattr__(
                    self, 
                    __name, 
                    dict_value
                )
            )
            # 3. Update the visual dict
            (
                object
                .__getattribute__(
                    self, 
                    'visual'
                )
                .update(
                    {
                        __name: dict_value
                    }
                )
            )

            return None

        # For specific attributes, operate chain set (more than on field matters)
        # This is important only when a metric is inputed in a visual.
        if __name in self.dict_fields:
            # For those attributes, if input is a PBIModel.Measure type,
            # extract values from input and set values
            if isinstance(__value, Measure.__bases__):
                # Measure type delivery Table.Measure pattern
                table_field_name = __value
                table_name = __value.split('.')[0]
                field_name = __value.split('.')[1]                
                # For those attributes, get the chain of dict path
                # and replace the template value for input value
                
                # Values to replace in template
                table_to_replace = self.dict_fields[__name]['table']
                field_to_replace = self.dict_fields[__name]['field']
                # Loop through all context (paths) in dict
                for context in parse('$..*').find(self.visual):
                    # Most part are dict or list, skip it
                    if not isinstance(context.value, (dict,list)):
                        # Convert to string
                        context_str_value = str(context.value)
                        # Serch for template fields
                        if re.search(table_to_replace, context_str_value): 
                            # Replace for input field there
                            self.__set_value_dict_path_jsonpath_replace(
                                json_path=context.full_path,
                                find=table_to_replace,
                                replace=table_name
                            )
                        if re.search(field_to_replace, context_str_value):
                            # Replace for input field there
                            self.__set_value_dict_path_jsonpath_replace(
                                json_path=context.full_path,
                                find=field_to_replace,
                                replace=field_name
                            )
                return None

        # For value inside the dict_attrs_path, update value after an assignement.
        # This is important when a visual is created and its values are updated.
        if __name in self.dict_attrs_path:
            # 1. Update the path with the value.
            self.__set_value_dict_path(
                path=self.dict_attrs_path[__name], 
                value=__value
            )
            # 2. Set the attribute
            object.__setattr__(self, __name, __value)
            # 3. Some atributtes impact one more field in dict, so, update it
            if __name in self.dict_mod_path:
                for path_ in self.dict_mod_path[__name]:
                    self.__set_value_dict_path(
                        path=path_, 
                        value=__value
                    )
            return

        # For any other attribute, just set it
        object.__setattr__(self, __name, __value)

        
    def __repr__(self) -> str:
        round_x = int(self.x)
        round_y = int(self.y)
        round_heigh = int(self.height)
        round_width = int(self.width)
        _ = f'''
        Visual(
        id: {self.id} |
        page: {self.page_name} |
        x,y: ({round_x},{round_y}) |
        h,w: ({round_heigh}, {round_width}) |
        type: {self.type_}
        )
        '''
        return ' '.join(_.split())

    def __get_dict_path_value(self, path:list[str]):
        looping = self.visual
        # Initiate loop
        for key in path:
            # Value could be a list, dict or a unique value
            value = looping.get(key, {})
            # If value is a list, get the first element
            if isinstance(value, list):
                looping = value[0]
            # Else, if value is a dict, get the dict
            elif isinstance(value, dict):
                looping = value
            # else:
            #     value = {}
            # Continue looping util end to get path last element value.
        
        return value # type: ignore
    
    def __set_value_dict_path(self, path:list, value):
        looping = self.visual
        last_ = path[-1]
        for key in path:
            if key == last_:
                break
            _ = looping.get(key)
            if isinstance(_, list):
                looping = _[0]
            elif isinstance(_, dict):
                looping = _        
        looping.update({last_:value})

        return None

    def __set_value_dict_path_jsonpath_replace(self, json_path, find, replace):
        '''
        '''
        # Actual value
        _value = parse(f'$.{json_path}').find(self.visual)[0].value
        # New value
        _value = re.sub(find, replace, _value)        
        
        # Name of field to set value
        to_update = str(json_path).split('.')[-1]

        # Find from where the field comes. It must be a dict.
        json_path_parent = '$.' + str(json_path) + '.`parent`'

        # Get the dict to update
        parent_dict = parse(json_path_parent).find(self.visual)[0].value
        parent_dict.update({to_update:_value})
    

    def dump_dicts(self) -> None:
        '''Method to update values in main dict.
        
        '''
        (
            self.visual
            .update(
                {
                    'config': json.dumps(self.config, ensure_ascii=False),
                    'query':json.dumps(self.query, ensure_ascii=False),            
                    'dataTransforms': json.dumps(self.dataTransforms, 
                                                 ensure_ascii=False)
                }
            )
        )  
