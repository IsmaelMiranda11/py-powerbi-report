'''This module is edited every time run a Visual object

The goal is to map all possible combination of path inside a visual dict
from Power BI.

'''

pre_set : dict[str, dict[str, str | list[str]]]= {
    'id': {
        'path_name' : 'name',
        'full_path' : ['config.name']
    },
    'horizontal': {
        'path_name' : 'x',
        'full_path' : ['config.layouts.[0].position.x', 'x']
    },
    'vertical': {
        'path_name' : 'y',
        'full_path' : ['config.layouts.[0].position.y', 'y']
    },
    'height': {
        'path_name' : 'height',
        'full_path' : ['config.layouts.[0].position.height', 'height']
    },
    'width': {
        'path_name' : 'width',
        'full_path' : ['config.layouts.[0].position.width', 'width']
    },
    'visual_type': {
        'path_name' : 'visualType',
        'full_path' : ['config.singleVisual.visualType']
    },
    'tab_order': {
        'path_name' : 'tabOrder',
        'full_path' : ['tabOrder']
    }
}

pre_set_fields = {

}