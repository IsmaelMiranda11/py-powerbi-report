'''This module is edited every time run a Visual object

The goal is to map all possible combination of path inside a visual dict
from Power BI.

'''

# Cards
card_attrs : dict[str, dict[str, str | list[str]]]= {
    'callout_font_size': {
        'path_name' : 'Value',
        'full_path' : ['config.singleVisual.objects.labels[0].properties.fontSize.expr.Literal.Value','dataTransforms.objects.labels[0].properties.fontSize.expr.Literal.Value']
    }
    ,
    'title_alignment': {
        'path_name' : 'Value',
        'full_path' : ['config.singleVisual.vcObjects.title[0].properties.alignment.expr.Literal.Value']
    }
    ,
    'title_text': {
        'path_name' : 'Value',
        'full_path' : ['config.singleVisual.vcObjects.title[0].properties.text.expr.Literal.Value']
    }
    ,
    'title_font_size': {
        'path_name' : 'Value',
        'full_path' : ['config.singleVisual.vcObjects.title[0].properties.fontSize.expr.Literal.Value']
    }
    ,
    'title_font_family': {
        'path_name' : 'Value',
        'full_path' : ['config.singleVisual.vcObjects.title[0].properties.fontFamily.expr.Literal.Value']
    }
}

card_attrs_fields : dict[str, dict[str, str | list[str]]] = {
    'callout_format_conditional_color':{
        'path_name' : 'Property',
        'full_path' : ['config.singleVisual.objects.labels[0].properties.color.solid.color.expr.Measure.Property'],
        'field' : ['config.singleVisual.objects.labels[0].properties.color.solid.color.expr.Measure.Property'],
        'table' : ['config.singleVisual.objects.labels[0].properties.color.solid.color.expr.Measure.Expression.SourceRef.Entity'],
        'qualified': []
    }
}


# Bookmark Slicer
bookmark_slicer_attrs : dict[str, dict[str, str | list[str]]]= {
    'bookmark_group': {
        'path_name' : 'Value',
        'full_path' : ['config.singleVisual.objects.bookmarks[0].properties.bookmarkGroup.expr.Literal.Value']
    }
}

bookmark_slicer_attrs_fields : dict[str, dict[str, str | list[str]]] = {
    }


# ----------------------------------------------------------------------------

column_attrs : dict[str, dict[str, str | list[str]]]= {
}

column_attrs_fields : dict[str, dict[str, str | list[str]]] = {
    'y':{
        'path_name' : 'Property',
        'full_path' : [
            'config.singleVisual.projections.Y[0].queryRef'
        ],
        'field' : [
            'config.singleVisual.objects.labels[0].properties.color.solid.color.expr.Measure.Property'
            'config.singleVisual.prototypeQuery.Select[1].Measure.Property',
            'config.singleVisual.prototypeQuery.Select[1].NativeReferenceName',
            'config.singleVisual.prototypeQuery.OrderBy[0].Expression.Measure.Property'
        ],
        'table' : ['config.singleVisual.objects.labels[0].properties.color.solid.color.expr.Measure.Expression.SourceRef.Entity'
                'query.Commands[0].SemanticQueryDataShapeCommand.Query.From[0].Entity'
                'dataTransforms.selects[1].expr.Measure.Expression.SourceRef.Entity'
        ],
        'qualified': [
            'config.singleVisual.projections.Y[0].queryRef',
            'config.singleVisual.prototypeQuery.Select[1].Name',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[1].Name',
            'dataTransforms.queryMetadata.Select[1].Name',
            'dataTransforms.selects[1].queryName'
        ]
    },
    'x': {
        'path_name' : 'queryRef',
        'full_path' : [
            'config.singleVisual.projections.Category[0].queryRef'
        ],
        'field' : [
            'config.singleVisual.prototypeQuery.Select[0].Column.Property', 
            'config.singleVisual.prototypeQuery.Select[0].NativeReferenceName', 
            'filters[0].expression.Column.Property',
            'filters[0].filter.Where[0].Condition.Not.Expression.In.Expressions[0].Column.Property',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[0].Column.Property',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[0].NativeReferenceName',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Where[0].Condition.Not.Expression.In.Expressions[0].Column.Property',
            'dataTransforms.queryMetadata.Select[0].Restatement',
            'dataTransforms.queryMetadata.Filters[0].expression.Column.Property',
            'dataTransforms.selects[0].displayName',
            'dataTransforms.selects[0].expr.Column.Property'
        ],
        'table' : [
            'config.singleVisual.objects.labels[0].properties.color.solid.color.expr.Measure.Expression.SourceRef.Entity'
            'filters[0].expression.Column.Expression.SourceRef.Entity',
            'filters[0].filter.From[0].Entity',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.From[1].Entity',
            'dataTransforms.queryMetadata.Filters[0].expression.Column.Expression.SourceRef.Entity',
            'dataTransforms.selects[0].expr.Column.Expression.SourceRef.Entity'
        ],
        'qualified': [
            'config.singleVisual.projections.Category[0].queryRef',
            'config.singleVisual.prototypeQuery.Select[0].Name',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[0].Name',
            'dataTransforms.projectionActiveItems.Category[0].queryRef',
            'dataTransforms.queryMetadata.Select[0].Name',
            'dataTransforms.selects[0].queryName'
        ]
    },
    'legend': {
        'path_name' : 'Property',
        'full_path' : [
            'config.singleVisual.projections.Series[0].queryRef'
        ],
        'field' : [
            'config.singleVisual.prototypeQuery.Select[2].Column.Property',
            'config.singleVisual.prototypeQuery.Select[2].NativeReferenceName',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[2].Column.Property',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[2].NativeReferenceName',
            'dataTransforms.queryMetadata.Select[2].Restatement',
            'dataTransforms.selects[2].displayName',
            'dataTransforms.selects[2].expr.Column.Property'
        ],
        'table' : [
            'config.singleVisual.objects.labels[0].properties.color.solid.color.expr.Measure.Expression.SourceRef.Entity',
            'dataTransforms.selects[2].expr.Column.Expression.SourceRef.Entity'
        ],
        'qualified': ['config.singleVisual.projections.Series[0].queryRef',
            'config.singleVisual.prototypeQuery.Select[2].Name',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[2].Name',
            'dataTransforms.queryMetadata.Select[2].Name',
            'dataTransforms.selects[2].queryName'
            ]
    }
}

slicer_attrs = {

}
slicer_attrs_fields = {
    'field':{
        'path_name' : '',
        'full_path' : [
            'config.singleVisual.projections.Values[0].queryRef'
        ],
        'field' : [
            'config.singleVisual.prototypeQuery.Select[0].Column.Property',
            'config.singleVisual.prototypeQuery.Select[0].NativeReferenceName',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[0].Column.Property',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[0].NativeReferenceName',
            'dataTransforms.queryMetadata.Select[0].Restatement',
            'dataTransforms.selects[0].displayName',
            'dataTransforms.selects[0].expr.Column.Property'
        ],
        'table' : [
            'config.singleVisual.prototypeQuery.From[0].Entity',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.From[0].Entity',
            'dataTransforms.selects[0].expr.Column.Expression.SourceRef.Entity'
        ],
        'qualified': [
            'config.singleVisual.projections.Values[0].queryRef',
            'config.singleVisual.prototypeQuery.Select[0].Name',
            'query.Commands[0].SemanticQueryDataShapeCommand.Query.Select[0].Name',
            'dataTransforms.projectionActiveItems.Values[0].queryRef',
            'dataTransforms.queryMetadata.Select[0].Name',
            'dataTransforms.selects[0].queryName'
        ]
    }
}

attributes_visual_dict = {
    'card': 
        {
            'attrs':card_attrs, 
            'field_attrs': card_attrs_fields
        },
    'bookmarkNavigator': 
        {
            'attrs':bookmark_slicer_attrs, 
            'field_attrs': bookmark_slicer_attrs_fields
        },
    'columnChart': 
        {
            'attrs':column_attrs, 
            'field_attrs': column_attrs_fields
        },
    'slicer': 
        {
            'attrs':slicer_attrs, 
            'field_attrs': slicer_attrs_fields
        }
}