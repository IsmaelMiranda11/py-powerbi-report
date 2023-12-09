'''
Chart constants
'''

'''
Names
'''
CHART_BAR = 'barChart'
CHART_CLUSTERED_BAR = 'clusteredBarChart'

CHART_COLUMN = 'columnChart'
CHART_CLUSTERED_COLUMN = 'clusteredColumnChart'

CHART_LINE = 'lineChart'
CHART_COMBO_LINE_STACKED_COLUMN = 'lineStackedColumnComboChart'
CHART_COMBO_LINE_CLUSTERED_COLUMN = 'lineClusteredColumnComboChart'

CHART_SCATTER = 'scatterChart'
CHART_AREA = 'areaChart'
CHART_PIE = 'pieChart'
CHART_DONUT = 'donutChart'
CHART_TREE_MAP = 'treemap'
CHART_MAP = 'map'
CHART_GAUGE = 'gauge'
CHART_MULTI_ROW = 'multiRowCard'

CARD = 'card'
TABLE_PLAIN = 'tableEx'
TABLE_PIVOT = 'pivotTable'

SLICER = 'slicer'

'''
Templates
'''
CARD = {
"x": 164.06706327744726,
"y": 233.98593834505138,
"z": 0,
"width": 172.37425635478635,
"height": 68.53434288804759,
"config": "{\"name\":\"9fd11a99fdd4d2e146d5\",\"layouts\":[{\"id\":0,\"position\":{\"x\":164.06706327744726,\"y\":233.98593834505138,\"z\":0,\"width\":172.37425635478635,\"height\":68.53434288804759,\"tabOrder\":0}}],\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Métricas.Categorica\"}]},\"prototypeQuery\":{\"Version\":2,\"From\":[{\"Name\":\"m\",\"Entity\":\"Métricas\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"Categorica\"},\"Name\":\"Métricas.Categorica\",\"NativeReferenceName\":\"Categorica\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"Categorica\"}}}]},\"drillFilterOtherVisuals\":true,\"hasDefaultSort\":true,\"objects\":{\"labels\":[{\"properties\":{\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"30D\"}}},\"labelDisplayUnits\":{\"expr\":{\"Literal\":{\"Value\":\"1D\"}}},\"labelPrecision\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}},\"color\":{\"solid\":{\"color\":{\"expr\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Reporting Layout\"}},\"Property\":\"Formatação Condicional\"}}}}}}}],\"categoryLabels\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"text\":{\"expr\":{\"Literal\":{\"Value\":\"'ppr_card_title'\"}}},\"alignment\":{\"expr\":{\"Literal\":{\"Value\":\"'center'\"}}},\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"10D\"}}}}}]}}}",
"filters": "[]",
"query": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"m\",\"Entity\":\"Métricas\",\"Type\":0},{\"Name\":\"r\",\"Entity\":\"Reporting Layout\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"Categorica\"},\"Name\":\"Métricas.Categorica\",\"NativeReferenceName\":\"Categorica\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"r\"}},\"Property\":\"Formatação Condicional\"},\"Name\":\"Reporting Layout.Formatação Condicional\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"Projections\":[1],\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
"dataTransforms": "{\"objects\":{\"labels\":[{\"properties\":{\"fontSize\":{\"expr\":{\"Literal\":{\"Value\":\"30D\"}}},\"labelDisplayUnits\":{\"expr\":{\"Literal\":{\"Value\":\"1D\"}}},\"labelPrecision\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}},\"color\":{\"solid\":{\"color\":{\"expr\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Reporting Layout\"}},\"Property\":\"Formatação Condicional\"}}}}}}}],\"categoryLabels\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]},\"projectionOrdering\":{\"Values\":[0]},\"queryMetadata\":{\"Select\":[{\"Restatement\":\"Categorica\",\"Name\":\"Métricas.Categorica\",\"Type\":1}]},\"visualElements\":[{\"DataRoles\":[{\"Name\":\"Values\",\"Projection\":0,\"isActive\":false}]}],\"selects\":[{\"displayName\":\"Categorica\",\"queryName\":\"Métricas.Categorica\",\"roles\":{\"Values\":true},\"type\":{\"category\":null,\"underlyingType\":259},\"expr\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Métricas\"}},\"Property\":\"Categorica\"}}},{\"displayName\":\"Formatação Condicional\",\"queryName\":\"Reporting Layout.Formatação Condicional\",\"roles\":{},\"type\":{\"category\":null,\"underlyingType\":1},\"expr\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Reporting Layout\"}},\"Property\":\"Formatação Condicional\"}},\"relatedObjects\":{\"labels\":{\"color\":[null]}}}]}"
}

SLICER_LIST = {
"x": 440.4123711340206,
"y": 150.9278350515464,
"z": 1,
"width": 215.8762886597938,
"height": 126.80412371134021,
"config": "{\"name\":\"0e27638a82c2796f899a\",\"layouts\":[{\"id\":0,\"position\":{\"x\":440.4123711340206,\"y\":150.9278350515464,\"z\":1,\"width\":215.8762886597938,\"height\":126.80412371134021}}],\"singleVisual\":{\"visualType\":\"slicer\",\"projections\":{\"Values\":[{\"queryRef\":\"Campanhas.Tipo de Campanha\",\"active\":true}]},\"prototypeQuery\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"Campanhas\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Tipo de Campanha\"},\"Name\":\"Campanhas.Tipo de Campanha\",\"NativeReferenceName\":\"Tipo de Campanha\"}]},\"drillFilterOtherVisuals\":true,\"objects\":{\"data\":[{\"properties\":{\"mode\":{\"expr\":{\"Literal\":{\"Value\":\"'Basic'\"}}}}}],\"header\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"text\":{\"expr\":{\"Literal\":{\"Value\":\"'ppr_slicer_box_title'\"}}}}}],\"background\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"padding\":[{\"properties\":{\"top\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}},\"bottom\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}},\"right\":{\"expr\":{\"Literal\":{\"Value\":\"5D\"}}},\"left\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}}}}],\"visualHeader\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"general\":[{\"properties\":{\"keepLayerOrder\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}}}}]}}}",
"filters": "[]",
"query": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"Campanhas\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Tipo de Campanha\"},\"Name\":\"Campanhas.Tipo de Campanha\",\"NativeReferenceName\":\"Tipo de Campanha\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{}}},\"IncludeEmptyGroups\":true,\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
"dataTransforms": "{\"objects\":{\"data\":[{\"properties\":{\"mode\":{\"expr\":{\"Literal\":{\"Value\":\"'Basic'\"}}}}}],\"header\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]},\"projectionOrdering\":{\"Values\":[0]},\"projectionActiveItems\":{\"Values\":[{\"queryRef\":\"Campanhas.Tipo de Campanha\",\"suppressConcat\":false}]},\"queryMetadata\":{\"Select\":[{\"Restatement\":\"Tipo de Campanha\",\"Name\":\"Campanhas.Tipo de Campanha\",\"Type\":2048}]},\"visualElements\":[{\"DataRoles\":[{\"Name\":\"Values\",\"Projection\":0,\"isActive\":true}]}],\"selects\":[{\"displayName\":\"Tipo de Campanha\",\"queryName\":\"Campanhas.Tipo de Campanha\",\"roles\":{\"Values\":true},\"type\":{\"category\":null,\"underlyingType\":1},\"expr\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Campanhas\"}},\"Property\":\"Tipo de Campanha\"}}}]}"
}

SLICER_DROPDOWN = {
"x": 440.4123711340206,
"y": 306.8041237113402,
"z": 2,
"width": 215.8762886597938,
"height": 96.49484536082474,
"config": "{\"name\":\"4c77a1dc73ceb56b2c01\",\"layouts\":[{\"id\":0,\"position\":{\"x\":440.4123711340206,\"y\":306.8041237113402,\"z\":2,\"width\":215.8762886597938,\"height\":96.49484536082474}}],\"singleVisual\":{\"visualType\":\"slicer\",\"projections\":{\"Values\":[{\"queryRef\":\"Campanhas.Tipo de Campanha\",\"active\":true}]},\"prototypeQuery\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"Campanhas\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Tipo de Campanha\"},\"Name\":\"Campanhas.Tipo de Campanha\",\"NativeReferenceName\":\"Tipo de Campanha\"}]},\"drillFilterOtherVisuals\":true,\"objects\":{\"data\":[{\"properties\":{\"mode\":{\"expr\":{\"Literal\":{\"Value\":\"'Dropdown'\"}}}}}],\"header\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]},\"items\":[{\"properties\":{\"textSize\":{\"expr\":{\"Literal\":{\"Value\":\"8D\"}}}}}],\"vcObjects\":{\"title\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}},\"text\":{\"expr\":{\"Literal\":{\"Value\":\"'ppr_slicer_dropdown_title'\"}}}}}], \"background\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"padding\":[{\"properties\":{\"top\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}},\"bottom\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}},\"right\":{\"expr\":{\"Literal\":{\"Value\":\"5D\"}}},\"left\":{\"expr\":{\"Literal\":{\"Value\":\"0D\"}}}}}],\"visualHeader\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"general\":[{\"properties\":{\"keepLayerOrder\":{\"expr\":{\"Literal\":{\"Value\":\"true\"}}}}}]}}}",
"filters": "[]",
"query": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"Campanhas\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Tipo de Campanha\"},\"Name\":\"Campanhas.Tipo de Campanha\",\"NativeReferenceName\":\"Tipo de Campanha\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{}}},\"IncludeEmptyGroups\":true,\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
"dataTransforms": "{\"objects\":{\"data\":[{\"properties\":{\"mode\":{\"expr\":{\"Literal\":{\"Value\":\"'Dropdown'\"}}}}}],\"header\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]},\"items\":[{\"properties\":{\"textSize\":{\"expr\":{\"Literal\":{\"Value\":\"8D\"}}}}}],\"projectionOrdering\":{\"Values\":[0]},\"projectionActiveItems\":{\"Values\":[{\"queryRef\":\"Campanhas.Tipo de Campanha\",\"suppressConcat\":false}]},\"queryMetadata\":null,\"visualElements\":null,\"selects\":[{\"displayName\":\"Tipo de Campanha\",\"queryName\":\"Campanhas.Tipo de Campanha\",\"roles\":{\"Values\":true},\"type\":{\"category\":null,\"underlyingType\":1},\"expr\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Campanhas\"}},\"Property\":\"Tipo de Campanha\"}}}]}"
}

COLUMN = {
"x": 697.7319587628866,
"y": 145.36082474226805,
"z": 3,
"width": 531.340206185567,
"height": 288.24742268041234,
"config": "{\"name\":\"733f05ad4b953004ae44\",\"layouts\":[{\"id\":0,\"position\":{\"x\":697.7319587628866,\"y\":145.36082474226805,\"z\":3,\"width\":531.340206185567,\"height\":288.24742268041234}}],\"singleVisual\":{\"visualType\":\"clusteredColumnChart\",\"projections\":{\"Category\":[{\"queryRef\":\"Calendário.Ano Ciclo\",\"active\":true},{\"queryRef\":\"Calendário.Data\"}],\"Y\":[{\"queryRef\":\"Métricas.Categorica\"}]},\"prototypeQuery\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"Calendário\",\"Type\":0},{\"Name\":\"m\",\"Entity\":\"Métricas\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Ano Ciclo\"},\"Name\":\"Calendário.Ano Ciclo\",\"NativeReferenceName\":\"Ano Ciclo\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Data\"},\"Name\":\"Calendário.Data\",\"NativeReferenceName\":\"Data\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"Categorica\"},\"Name\":\"Métricas.Categorica\",\"NativeReferenceName\":\"Categorica\"}]},\"drillFilterOtherVisuals\":true,\"objects\":{\"valueAxis\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}},\"showAxisTitle\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"categoryAxis\":[{\"properties\":{\"titleFontSize\":{\"expr\":{\"Literal\":{\"Value\":\"8D\"}}}}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"text\":{\"expr\":{\"Literal\":{\"Value\":\"'ppr_column_title'\"}}}}}]}}}",
"filters": "[]",
"query": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"Calendário\",\"Type\":0},{\"Name\":\"m\",\"Entity\":\"Métricas\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Ano Ciclo\"},\"Name\":\"Calendário.Ano Ciclo\",\"NativeReferenceName\":\"Ano Ciclo\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Data\"},\"Name\":\"Calendário.Data\",\"NativeReferenceName\":\"Data\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"m\"}},\"Property\":\"Categorica\"},\"Name\":\"Métricas.Categorica\",\"NativeReferenceName\":\"Categorica\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Ano Ciclo\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":1000}}},\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
"dataTransforms": "{\"objects\":{\"valueAxis\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}},\"showAxisTitle\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"categoryAxis\":[{\"properties\":{\"titleFontSize\":{\"expr\":{\"Literal\":{\"Value\":\"8D\"}}}}}]},\"projectionOrdering\":{\"Category\":[0,1],\"Y\":[2]},\"projectionActiveItems\":{\"Category\":[{\"queryRef\":\"Calendário.Ano Ciclo\",\"suppressConcat\":false}]},\"queryMetadata\":{\"Select\":[{\"Restatement\":\"Ano Ciclo\",\"Name\":\"Calendário.Ano Ciclo\",\"Type\":2048},{\"Restatement\":\"Data\",\"Name\":\"Calendário.Data\",\"Type\":4,\"Format\":\"G\"},{\"Restatement\":\"Categorica\",\"Name\":\"Métricas.Categorica\",\"Type\":1}]},\"visualElements\":[{\"DataRoles\":[{\"Name\":\"Category\",\"Projection\":0,\"isActive\":true},{\"Name\":\"Category\",\"Projection\":1,\"isActive\":false},{\"Name\":\"Y\",\"Projection\":2,\"isActive\":false}]}],\"selects\":[{\"displayName\":\"Ano Ciclo\",\"queryName\":\"Calendário.Ano Ciclo\",\"roles\":{\"Category\":true},\"sort\":1,\"sortOrder\":0,\"type\":{\"category\":null,\"underlyingType\":1},\"expr\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Calendário\"}},\"Property\":\"Ano Ciclo\"}}},{\"displayName\":\"Data\",\"format\":\"G\",\"queryName\":\"Calendário.Data\",\"roles\":{\"Category\":true},\"type\":{\"category\":null,\"underlyingType\":519},\"expr\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Calendário\"}},\"Property\":\"Data\"}}},{\"displayName\":\"Categorica\",\"queryName\":\"Métricas.Categorica\",\"roles\":{\"Y\":true},\"type\":{\"category\":null,\"underlyingType\":259},\"expr\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Entity\":\"Métricas\"}},\"Property\":\"Categorica\"}}}]}"
}

BOOKMARK_SLICER = {
    "x": 493.6082474226804,
    "y": 118.14432989690721,
    "z": 3,
    "width": 259.7938144329897,
    "height": 49.48453608247423,
    "config": "{\"name\":\"07788b861426e801f4c7\",\"layouts\":[{\"id\":0,\"position\":{\"x\":493.6082474226804,\"y\":118.14432989690721,\"z\":3,\"width\":259.7938144329897,\"height\":49.48453608247423}}],\"singleVisual\":{\"visualType\":\"bookmarkNavigator\",\"drillFilterOtherVisuals\":true,\"objects\":{\"bookmarks\":[{\"properties\":{\"bookmarkGroup\":{\"expr\":{\"Literal\":{\"Value\":\"'Bookmark3a33e033c4557e665f3b'\"}}},\"selectedBookmark\":{\"expr\":{\"Literal\":{\"Value\":\"'Bookmark0ed6bff31aa9b8bd1871'\"}}}}}]}}}",
    "filters": "[]"
}

VISUAL_TEMPLATE_DICT = {
    'card': CARD,
    'slicer_drop': SLICER_DROPDOWN,
    'slicer_list': SLICER_LIST,
    'column':COLUMN,
    'bookmark_slicer': BOOKMARK_SLICER
}