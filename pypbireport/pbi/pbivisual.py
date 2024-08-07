
'''Module for class to work with visuals of Power BI
'''

import json
import copy
from jsonpath_ng import parse
from typing import Literal, Any

from ..functions.functions import (export_dict_as_file, 
    set_attrs_name_visual, hex_code)
from ..constants import structures
from ..constants import charts

from .pbimodel import Measure

from ..visuals.preset_attrs import pre_set, pre_set_fields

from ..visuals.visuals_attrs import attributes_visual_dict

class VisualAttributes():
    '''Class of all atributes of a Visual.

    This object gather all visual JSON path, as its values.
    For this, parse of jsonpath_ng libary is used to find all internal path,
    desconsidering `dict` and `list` objects.
    The full path is tranformed in a valid attribute name and along with value
    and original full path they are record inside a dictionary.

    Args:
        visual_dict (dict): A Power BI visual dictionary.

    Attributes:
        attributes_dict (dict): A dictionary with all visual path and its value.
    '''

    def __init__(self, visual_dict:dict) -> None:
        
        contexts = parse('$..*').find(visual_dict) # find all path of JSON

        valid_contexts = [context for context in contexts
            if not isinstance(context.value, (dict, list)) ] # no dict or list
        self.contexts:list = valid_contexts 

        attrs_names = [ set_attrs_name_visual(str(context.full_path))
            for context in valid_contexts ] 

        attrs_values = [ context.value for context in valid_contexts ] 
        
        full_paths = [ str(context.full_path) for context in valid_contexts ]

        
        self.attributes_dict:dict = {}
        for (name, value, path) in zip(attrs_names,attrs_values,full_paths):
            # Put information into the dict
            self.attributes_dict.update(
                { name: {'attr_value': value, 'full_path': path} } )
            # Set attribute for the object
            object.__setattr__(self, name, value)

class Visual():
    '''Class to represent a visual of Power BI.

    A Power BI visual is represented by a JSON or a dictionary in python. They
    are hold in `visualContainers` key of each page in report layout JSON.
    From visual dictionary, it is possible to set a bunch of proprities, such 
    as vertical and horizontal positions, as well the measure field.
    The visual dictionary structure is based in some other dictionary represent 
    by keys like `config`, `query` and `dataTranforms`. After serialization
    of visual dictionary, these came as strings and they should be processed 
    before extract or modify any content.
    
    Note:
        As a disclaimer, all the work done here is just a reverse engineering 
        of what Power BI design results. It is totally normal erros occurs
        and some features being implemented by another way.

    Args:
        visual_dict (dict): The dictionary that represent a Power BI visual
        page_name (str | None, optional): The page where the visual is placed. 
            It can be None, for new visuals. Defaults to ''.
        page_id (str | None, optional): The heximadecimal id page value. 
            Defaults to ''.

    Attributes:
        original_visual (dict): The original JSON format before any 
            tranformation of the visual.
        visual (dict): The dictionary that represent the visual.
        page_name (str): The page name where the visual is placed.
        page_id (str): The hexadecimal page value where the visual is placed.
        config (dict): Dictonary that represents config of the visual. Hold a 
            great part of visual display configurations, such as position.
        query (dict): Dictonary that represents query that are done of visual 
            display data. 
        dataTransforms (dict): Dictonary with configuration of data 
            tranformation of the visual.
        filters (dict): Dictonary with filters applied to the visual.
        id (str): Hexadecimal value that represent the visual. It should be
            unique in a report.
        horizontal (float): The x position of the visual in a page.
        vertical (float): The y position of the visual in a page.
        height (float): The height of the visual.
        width (float): The width of the visual.
        visual_type (str): The Power BI type of the visual.
        tab_order (str):  The layer order of the visual in a page.

    '''

    def __init__(self, 
        visual_dict: dict, 
        page_name: str | None ='',
        page_id: str | None = ''
    ) -> None:
        # If input is a dict, it must be a visual dict from report layout dict
        if not isinstance(visual_dict, dict):
            raise ValueError("It must be a dict as input")

        # Deepcopy
        self.original_visual = copy.deepcopy(visual_dict)
        # Get visual dict
        self.visual = visual_dict
            
        # Page name
        self.page_name = page_name
        self.page_id = page_id

        # Convert to dict object in __setattrs__
        self.config = self.visual.get('config', "{}")
        self.query = self.visual.get('query', "{}")
        self.dataTransforms = self.visual.get('dataTransforms', "{}")
        self.filters = self.visual.get('filters', "{}")

        # These are preset attributes of any Visual
        self.id:str
        self.horizontal:float
        self.vertical:float
        self.height:float
        self.width:float
        self.visual_type:str
        self.tab_order:int

        
        # Parse all paths inside the visual dict with a proper class.
        ### Deprecated due perfomance issues 
        # self.all_attributes:VisualAttributes
        # object.__setattr__(self, 'all_attributes', 
        #     VisualAttributes(self.visual))

        # List of json path context
        contexts = parse('$..*').find(visual_dict) # find all path of JSON
        valid_contexts = [context for context in contexts
            if not isinstance(context.value, (dict, list)) ] # no dict or list
        self.__contexts:list = valid_contexts 
        
        # Set of attributes. Note:
        # There are two type of attributes, 'normal' and field attributes.
        # Fields attributes are special because great part of its update
        # depends of modifing a bunch of JSON path inside visual dictionary.
        # Because of this, the two types of attributes are setted with 
        # different kind of functions.
        
        # Preset of attributes should be collected by JSON path
        for attr_name, attr_dict in pre_set.items():
            full_path = attr_dict.get('full_path', [])
            # For setting, only the `0`
            object.__setattr__(self, attr_name, self._get_value(full_path[0])) 

        # Preset of fields attributes should be collected by JSON path
        for attr_name, attr_dict in pre_set_fields.items():
            full_path = attr_dict.get('full_path', [])
            object.__setattr__(self, attr_name, self._get_value(full_path[0]))
        
    
    def _set_dict_attrs(self, __name:str, __value:Any) -> None:
        '''Setter method for dict attributes for visual

        The attributes `config`, `query`, `dataTranforms` and `filters` came 
        as string represention of JSON. This method parse these strings to
        dict objects and update the visual dictionary with its.

        Args:
            __name (str): The name of attribute
            __value (Any): The value for the attribute

        '''
        if isinstance(__value, str):
            dict_value = json.loads(__value) #convert to dict
        else:
            dict_value = __value 
        # Set attribute of the object
        object.__setattr__(self, __name, dict_value )
        # Update the visual dict
        object.__getattribute__(self,'visual').update({ __name: dict_value } )

        return None

    def _set_pre_set_attrs(self,__name:str, __value:Any) -> None:
        '''Setter method for normal attributes for the visual

        The normal attributes are those that have a list of paths to update its
        values. That means that one attribute is present in differents places
        inside visual dictionary.
        This method set the attribute value for the attribute name and for all
        dictionary keys inside paths list.

        Args:
            __name (str): The name of attribute
            __value (Any): The value for the attribute
        '''

        attr_dict = pre_set.get(__name, {}) #dictionary of that attribute
        paths = attr_dict.get('full_path',[]) #list of paths
        
        # Update the paths
        for path in paths:
            self._update_value(path=path, new_value=__value)
        
        # Set the attribute of the object, beside for the paths
        object.__setattr__(self, __name, __value)


    def _set_pre_set_attrs_fields(self,__name:str, __value:Any) -> None:
        '''Setter method for fields attributes for the visual

        The fields attributes have a special characteristc where their values 
        follow the format of `Table.NameField`. Within the visual dictionary, 
        different keys have this qualified name, while others have only `Table`
        , and yet others have only `NameField`.
        This method updates all paths for these three values using the 
        attribute dictionary, which contains each of the three paths.

        Args:
            __name (str): The name of attribute
            __value (Any): The value for the attribute

        '''

        # For those attributes, if input is a PBIModel.Measure type,
        # extract values from input and set values
        if not isinstance(__value, Measure.__bases__):
            raise ValueError("The input should be a Measure")
        
        # Measure type delivery Table.NameField pattern
        qualified_name = __value
        field_name = qualified_name.split('.')[1]
        table_name = qualified_name.split('.')[0]
        
        # For those attributes, get the chain of dict path
        # and replace the template value for input value
        attr_dict = pre_set_fields.get(__name, {})
        paths = attr_dict.get('full_path',[]) #paths for that value
        field_paths = attr_dict.get('field',[]) #for NameField
        table_paths =attr_dict.get('table',[]) #for Table
        qualified_paths =attr_dict.get('qualified',[]) # for Table.NameField
        
        # Run for each list of paths
        for path in paths:
            self._update_value(path=path,new_value=__value)
        for path in field_paths:
            self._update_value(path=path,new_value=field_name)
        for path in table_paths:
            self._update_value(path=path,new_value=table_name)
        for path in qualified_paths:
            self._update_value(path=path,new_value=qualified_name)

        # Set the attribute of the object, beside for the paths
        object.__setattr__(self, __name, __value)

        return None


    def __setattr__(self, __name, __value):
        '''Modified to manipulate dictionary keys updating
        '''

        # For attributes of dictionary strings
        if __name in ['config', 'query', 'dataTransforms', 'filters']:
            self._set_dict_attrs(__name, __value)
            return None

        # For pre set attributes
        if __name in pre_set:
            self._set_pre_set_attrs(__name, __value)
            return None
        # For pre set fields attributes
        if __name in pre_set_fields:
            self._set_pre_set_attrs_fields(__name, __value)
            return None

        # For any other attribute, just set it
        object.__setattr__(self, __name, __value)

        
    def __repr__(self) -> str:
        round_x = int(self.horizontal)
        round_y = int(self.vertical)
        round_heigh = int(self.height)
        round_width = int(self.width)
        _ = f'''
        Visual(
        id: {self.id} |
        page: {self.page_name} |
        hor,ver: ({round_x},{round_y}) |
        h,w: ({round_heigh}, {round_width}) |
        type: {self.visual_type}
        )
        '''
        return ' '.join(_.split())
    
    def _get_value(self, path:str) -> Any | None:
        '''Method to retrieve the value of a key in dict using for a JSON path

        Args:
            path (str): A JSON path to desired value into obejct

        Returns:
            The value of JSON path can be a int, str, bool or anything else,
                even none.
        '''
        for context in self.__contexts:
            if str(context.full_path) == path:
                return context.value

        return None

    
    def _update_value(self, path:str, new_value) -> None:
        '''Method to update the value of a key in a dict using a JSON path

        Args:
            path (str): A JSON path to desired value into obejct
        '''
        context = parse(f'$.{path}').find(self.visual)
        if context: #may not exist
            parse(f'$.{path}').update(self.visual, new_value)

        return None
    
    def dump_dicts(self) -> None:
        '''Method to update values in the visual dict.

        The Power BI visual dictionary will be converted to a JSON object.
        Within the JSON, the bellow keys should be in string format. 
        This method is called within PBIReport.save_report() and performs this
        action before saving a new Power BI file.
        
        '''

        self.visual.update(
            {
                'config': json.dumps(self.config, ensure_ascii=False),
                'query':json.dumps(self.query, ensure_ascii=False),
                'dataTransforms': json.dumps(self.dataTransforms, 
                    ensure_ascii=False),
                'filters': json.dumps(self.filters, ensure_ascii=False)
            }
        )

        return None


    def export_visual_dicts(self, file_name:str | None = None): 
        '''Method to export dict of visual as a JSON file.

        This method is a convinent way to export and provide a view of visual 
        dictionary.
        This divide in 'original' and 'transformed' dictionaries. The 'origina'
        may contains the visual dictionary as this came from Power BI. It is
        not garanteed after some tranformations. The 'transformed' is the
        result of the parsing of string to dictionary object inside this class.

        Args:
            file_name (str | None, optional): The name of file. 
                Defaults to None.
        
        '''
        # If there is no file_name, it uses a default one.
        if not file_name:
            file_name = f'{self.visual_type}_{self.id}.json'

        # Create a dictionary to export, with original and transformed keys.
        dict_ = {'original': self.original_visual , 'transformed': self.visual}

        export_dict_as_file(dict_, file_name=file_name)

        return None

class BaseVisual(Visual):
    '''Class to represent the base of any specific visual type

    More than generic class Visual, some visuals have their specificity, namely
    the attributes. This class works to initiate this specific classes.
    
    Args:
        visual_dict (dict): The dictionary that represent a Power BI visual
        page_name (str | None, optional): The page where the visual is placed. 
            It can be None, for new visuals. Defaults to ''.
        page_id (str | None, optional): The heximadecimal id page value. 
            Defaults to ''.

    Attributes:
        _obj_name (str): The name of viusal type
        _attrs (dict): A dictonary with set of attributes for the visual type
        _field_attrs (dict): A dictonary with set of fields attributes for the 
            visual type
    '''

    def __init__(self, visual_dict: dict, page_name, page_id) -> None:
        '''_summary_

        _extended_summary_

        Args:
           
        '''
        
        super().__init__(visual_dict, page_name, page_id)

        self._obj_name:str
        self._attrs:dict
        self._field_attrs:dict

        # Set the exclusives attributes
        for attr_name, attr_dict in self._attrs.items():
            full_path = attr_dict.get('full_path', [])
            object.__setattr__(self, attr_name, self._get_value(full_path[0]))

        # Set the exclusives fields attributes
        for attr_name, attr_dict in self._field_attrs.items():
            full_path = attr_dict.get('full_path', [])
            object.__setattr__(self, attr_name, self._get_value(full_path[0]))

    def _set_attrs(self,__name:str, __value:Any) -> None:
        '''Setter method for normal attributes for the visual

        The normal attributes are those that have a list of paths to update its
        values. That means that one attribute is present in differents places
        inside visual dictionary.
        This method set the attribute value for the attribute name and for all
        dictionary keys inside paths list.

        Args:
            __name (str): The name of attribute
            __value (Any): The value for the attribute
        '''

        attr_dict = self._attrs.get(__name, {}) #dictionary of that attribute
        paths = attr_dict.get('full_path',[]) #list of paths
        
        for path in paths:
            super()._update_value(
                path=path,
                new_value=__value
            )

        # Set the attribute of the object, beside for the paths
        object.__setattr__(self, __name, __value)

        return None
    
    def _set_attrs_fields(self,__name, __value):
        '''Setter method for fields attributes for the visual

        The fields attributes have a special characteristc where their values 
        follow the format of `Table.NameField`. Within the visual dictionary, 
        different keys have this qualified name, while others have only `Table`
        , and yet others have only `NameField`.
        This method updates all paths for these three values using the 
        attribute dictionary, which contains each of the three paths.

        Args:
            __name (str): The name of attribute
            __value (Any): The value for the attribute

        '''

        # For those attributes, if input is a PBIModel.Measure type,
        # extract values from input and set values
        if not isinstance(__value, Measure.__bases__):
            raise ValueError("The input should be a Measure")
        
        # Measure type delivery Table.NameField pattern
        qualified_name = __value
        field_name = qualified_name.split('.')[1]
        table_name = qualified_name.split('.')[0]

        # For those attributes, get the chain of dict path
        # and replace the template value for input value
        attr_dict = self._field_attrs.get(__name, {})
        paths = attr_dict.get('full_path',[]) #paths for that value
        field_paths = attr_dict.get('field',[]) #for NameField
        table_paths =attr_dict.get('table',[]) #for Table
        qualified_paths =attr_dict.get('qualified',[]) # for Table.NameField
        
        # Run for each list of paths
        for path in paths:
            self._update_value(path=path,new_value=__value)
        for path in field_paths:
            self._update_value(path=path,new_value=field_name)
        for path in table_paths:
            self._update_value(path=path,new_value=table_name)
        for path in qualified_paths:
            self._update_value(path=path,new_value=qualified_name)

        # Set the attribute of the object, beside for the paths
        object.__setattr__(self, __name, __value)

    def __setattr__(self, __name, __value):
        '''Modified to manipulate dictionary keys updating
        
        '''
        # For visual attributes
        if __name in self._attrs:
            self._set_attrs(__name, __value)
        # For visual fields attributes
        if __name in self._field_attrs:
            self._set_attrs_fields(__name, __value)
        
        # For any other attribute, just set it
        super().__setattr__(__name, __value)

    def __repr__(self) -> str:
        return super().__repr__().replace('Visual',self._obj_name)

class Card(BaseVisual):
    '''Representation of Power BI Card visual

    Args:
        visual_dict (dict): The dictionary that represent a Power BI visual
        page_name (str | None, optional): The page where the visual is placed. 
            It can be None, for new visuals. Defaults to ''.
        page_id (str | None, optional): The heximadecimal id page value. 
            Defaults to ''.
    
    Attributes:
        __visual (str): Visual name key to use in main dictonary of attributes
        _obj_name (str): Viusal name to use in __repr__.
         _attrs (dict): A dictonary with set of attributes for the visual type
        _field_attrs (dict): A dictonary with set of fields attributes for the 
            visual type
    '''
    __visual = 'card'
    _obj_name = 'Card'

    _attrs = attributes_visual_dict.get(__visual,{}).get('attrs', {})
    _field_attrs = attributes_visual_dict.get(__visual,{}).get(
        'field_attrs', {})

    def __init__(self, visual_dict: dict, page_name, page_id) -> None:
        super().__init__(visual_dict, page_name, page_id)

class Column(BaseVisual):
    '''Representation of Power BI Column Chart visual

    Args:
        visual_dict (dict): The dictionary that represent a Power BI visual
        page_name (str | None, optional): The page where the visual is placed. 
            It can be None, for new visuals. Defaults to ''.
        page_id (str | None, optional): The heximadecimal id page value. 
            Defaults to ''.
    
    Attributes:
        __visual (str): Visual name key to use in main dictonary of attributes
        _obj_name (str): Viusal name to use in __repr__.
         _attrs (dict): A dictonary with set of attributes for the visual type
        _field_attrs (dict): A dictonary with set of fields attributes for the 
            visual type
    '''
    __visual = 'columnChart'
    _obj_name = 'Column'

    _attrs = attributes_visual_dict.get(__visual,{}).get('attrs', {})
    _field_attrs = attributes_visual_dict.get(__visual,{}).get(
        'field_attrs', {})

    def __init__(self, visual_dict: dict, page_name, page_id) -> None:
        super().__init__(visual_dict, page_name, page_id)
    

class Slicer(BaseVisual):
    '''Representation of Power BI Slicer visual

    Args:
        visual_dict (dict): The dictionary that represent a Power BI visual
        page_name (str | None, optional): The page where the visual is placed. 
            It can be None, for new visuals. Defaults to ''.
        page_id (str | None, optional): The heximadecimal id page value. 
            Defaults to ''.
    
    Attributes:
        __visual (str): Visual name key to use in main dictonary of attributes
        _obj_name (str): Viusal name to use in __repr__.
         _attrs (dict): A dictonary with set of attributes for the visual type
        _field_attrs (dict): A dictonary with set of fields attributes for the 
            visual type
    '''
    __visual = 'slicer'
    _obj_name = 'Slicer'

    _attrs = attributes_visual_dict.get(__visual,{}).get('attrs', {})
    _field_attrs = attributes_visual_dict.get(__visual,{}).get(
        'field_attrs', {})

    def __init__(self, visual_dict: dict, page_name, page_id) -> None:
        super().__init__(visual_dict, page_name, page_id)

class BookmarkSlicer(BaseVisual):
    '''Representation of Power BI Bookmark Navigator visual

    Args:
        visual_dict (dict): The dictionary that represent a Power BI visual
        page_name (str | None, optional): The page where the visual is placed. 
            It can be None, for new visuals. Defaults to ''.
        page_id (str | None, optional): The heximadecimal id page value. 
            Defaults to ''.
    
    Attributes:
        __visual (str): Visual name key to use in main dictonary of attributes
        _obj_name (str): Viusal name to use in __repr__.
         _attrs (dict): A dictonary with set of attributes for the visual type
        _field_attrs (dict): A dictonary with set of fields attributes for the 
            visual type
    '''
    __visual = 'bookmarkNavigator'
    _obj_name = 'BookmarkSlicer'

    _attrs = attributes_visual_dict.get(__visual,{}).get('attrs', {})
    _field_attrs = attributes_visual_dict.get(__visual,{}).get(
        'field_attrs', {})

    def __init__(self, visual_dict: dict, page_name, page_id) -> None:
        super().__init__(visual_dict, page_name, page_id)

class VisualInitializer():
    '''Class to initializer a Visual

    Receive a and evaluate its type. For certain types, this class returns
    a proper class of visual type.

    Args:
        visual (Visual):

    Returns:
        A class of visual.

    '''

    __initializer_dict:dict = {
        'card': Card,
        'columnChart': Column,
        'slicer': Slicer,
        'bookmarkNavigator': BookmarkSlicer
    } # type: ignore

    def __new__(cls, visual:Visual) -> Visual:
        if visual.visual_type in cls.__initializer_dict:
            return ( 
                cls.__initializer_dict.get(visual.visual_type)(
                    visual_dict = visual.visual,
                    page_name = visual.page_name,
                    page_id = visual.page_id
                )
                ) # type: ignore
        else:
            return visual
        

def create_new_visual(
    visual:Literal[
        'card', 
        'column', 
        'slicer_drop', 
        'slicer_list', 
        'bookmark_slicer'],
    page_name:str,
    page_id:str,
    custom_template: dict | None = None
    ) -> Visual:

    
    '''Function to create a new visual from a existing or custom template.

    Here some template are offered to be create for futher customization. 
    There are four options: card, column chart, slicer (dropdown or list) and 
    a bookmark navagitor.
    The return of this funtion is a Viusal object of chossen class that can be
    inserted inside a report.

    Args:
        visual ('str'): The desired visual.
        page_name (str): The page name where visual will be placed.
        page_id (str): The page hexadecimal value where visual will be placed.
        custom_template (dict | None, optional): A custom visual dictionary can
            be an input for the new visual. Defaults to None.

    Returns:
        Visual: A visual object choosen.
    '''

    if custom_template:
        visual_dict = custom_template
    else:
        visual_dict = charts.VISUAL_TEMPLATE_DICT.get(visual, {})
    
    visual_obj = VisualInitializer(
        Visual(
            visual_dict=visual_dict, 
            page_name=page_name,
            page_id=page_id
        )
    )

    # Change the hexadecimal code of the visual
    visual_obj.id = hex_code()

    return visual_obj

def copy_visual(visual:Visual) -> Visual:
    '''Function to copy an existing visual of report.
    
    Use this function when you want to get an existing visual in report and to
    copy it for futher modification.
    The return copied visual has no page allocated. Remember to insert it in a 
    page after copy.

    Args:
        visual (Visual): A visual object.

    Return:
        Visual: A copied visual.
    '''
    # Deepcopy the visual dictionary.
    visual_copy_dict = copy.deepcopy(visual.visual)
    
    # Create a copy with Visual and VisualInitializer
    visual_copy = VisualInitializer(Visual(visual_copy_dict))
    # Change the id of visual
    visual_copy.id = hex_code()

    return visual_copy