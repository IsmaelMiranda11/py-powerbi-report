'''
Structure for report fields
'''
CONTENT_TYPE_XML = '''<?xml version="1.0" encoding="utf-8"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
        <Default Extension="json" ContentType="" />
        <Default Extension="png" ContentType="" />
        <Default Extension="jpeg" ContentType="" />
        <Override PartName="/Version" ContentType="" />
        <Override PartName="/DiagramLayout" ContentType="" />
        <Override PartName="/Report/Layout" ContentType="" />
        <Override PartName="/Settings" ContentType="application/json" />
        <Override PartName="/Metadata" ContentType="application/json" />
        <Override PartName="/DataModel" ContentType="" />
    </Types>
    '''

BOOKMARK_DICT = {
            'displayName': '',
            'name': '',
            'explorationState': 
                    {
                        'version': '1.3',
                        'activeSection': 'exemplo',
                        'sections': 
                            {
                            'exemplo': 
                                {
                                'visualContainers': {}
                                }
                            }
                    },
            'options': 
            {
                'targetVisualNames': [],
                'suppressData': True,
                'suppressActiveSection': True,
                'applyOnlyToTargetVisuals': True
            }
        }

BOOKMARK_SLICER_DICT = {
            'x': 0,
            'y': 0,
            'z': 3000,
            'width': 100,
            'height': 50,
            'config': '',
            'filters': '[]',
            'tabOrder': 11000
        }

BOOKMARK_SLICER_CONFIG_DICT = {
            "name": '',
            "layouts": [
                {
                    "id": 0,
                    "position": {
                        "x": '',
                        "y": '',
                        "z": '',
                        "width":  '',
                        "height": '',
                        "tabOrder":  ''
                    }
                }
            ],
            "singleVisual": {
                "visualType": "bookmarkNavigator",
                "drillFilterOtherVisuals": False,
                "objects": {
                    "bookmarks": [
                        {
                            "properties": {
                                "bookmarkGroup": {
                                    "expr": {
                                        "Literal": {
                                            "Value": ''
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }