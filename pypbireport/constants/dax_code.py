DAX_SUM:str = '''

    SUM ( field )
'''

DAX_AVG:str = '''

    AVERAGE ( field )
'''

DAX_CATEGORY:str = '''

VAR _cat_tab = FILTER ( cat_table, cat_field in {list_cat_values} )
VAR _value = CALCULATE ( measure, _cat_tab )

RETURN
    _value
'''

DAX_DIVIDER:str = '''

VAR _numerator = CALCULATE ( measure_numerator )
VAR _denominator = CALCULATE ( measure_denominator )
VAR _value = DIVIDE ( _numerator, _denominator, 0 )

RETURN 
    _value
'''

DAX_DIVIDER_CATEGORY:str = ''' 

VAR _cat_tab_num = FILTER ( cat_table_numerator, cat_field_numerator in {list_cat_values_numerator} )
VAR _numerator = CALCULATE ( measure_numerator, _cat_tab_num )

VAR _cat_tab_den = FILTER ( cat_table_denominator, cat_field_denominator in {list_cat_values_denominator} )
VAR _denominator = CALCULATE ( measure_denominator, _cat_tab_den )

VAR _value = DIVIDE ( _numerator, _denominator, 0 )

RETURN 
    _value
'''

DAX_PPR_TEMPLATE = [
    {
        'name':'ppr_sum', 
        'syntax': 'ppr_sum(field)',
        'dax_template': DAX_SUM,
        'expected_args': ['field']
    },
    {
        'name':'ppr_avg', 
        'syntax': 'ppr_avg(field)',
        'dax_template': DAX_AVG,
        'expected_args': ['field']
    },
    {
        'name':'ppr_category', 
        'syntax': 'ppr_category(measure | cat_table | cat_field | list_cat_values)',
        'dax_template': DAX_CATEGORY,
        'expected_args': ['measure', 'cat_table', 'cat_field', 'list_cat_values']
    },
    {
        'name':'ppr_divider', 
        'syntax': 'ppr_divider(measure_numerator | measure_denominator)',
        'dax_template': DAX_DIVIDER
        ,'expected_args': ['measure_numerator', 'measure_denominator']
    },
    {
        'name':'ppr_divider_category', 
        'syntax': 'ppr_divider_category(measure_numerator | cat_table_numerator | cat_field_numerator | list_cat_values_numerator | measure_denominator | cat_table_denominator | cat_field_denominator | list_cat_values_denominator)',
        'dax_template': DAX_DIVIDER_CATEGORY,
        'expected_args': ['measure_numerator','cat_table_numerator','cat_field_numerator','list_cat_values_numerator','measure_denominator','cat_table_denominator','cat_field_denominator','list_cat_values_denominator']
    }
]
