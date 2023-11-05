'''
General functions module to help in test or features
'''

import json
import secrets
import codecs
import os
import re
from unidecode import unidecode


def export_dict_as_file(dict, file_name='Sample.json'):
    with open(file_name, 'w', encoding='utf8') as f:
        f.write(json.dumps(dict, indent=4, ensure_ascii=False))
    return None

def hex_code(prefix=''):
    return prefix + secrets.token_hex(nbytes=10)

def get_str_dict(dict={}, field_name=''):
    return json.loads(dict.get(field_name))

def update_str_dict(dict={}, field_name=''):
    return dict.update({field_name: json.dumps(dict.get(field_name))})

def encode_content(content, enconding='utf-8'):
    return codecs.encode(content, enconding)

def get_parent_dir_path(file):
    return os.path.dirname(os.path.dirname(file))

def format_column_width(df, excel, sheet_name):
    '''
    Format width column of exported Excel through pandas
    '''
    wb = excel.book
    formt = wb.add_format({'text_wrap' : True})
    formt.set_align('top')
    formt.set_align('left')
    
    sheet = excel.sheets[sheet_name]
    if df.index.names[0] != None:
        df = df.reset_index() 

    for idx, column in enumerate(df):
        series = df[column]
        ideal_width = (
            max (
                series.astype(str).map(len).max(),  
                len(str(series.name))
            ) + 1
        )
        ideal_width = 100 if ideal_width > 200 else ideal_width
        
        sheet.set_column(idx,idx, ideal_width, formt)
        
    return None

def set_attrs_name(_str_, preffix): 
    no_accents = unidecode(_str_).lower()
    no_pro_cara = re.sub(
        pattern='[^a-zA-Z0-9_ ]',
        string=no_accents,
        repl=''
    )
    no_spaces = ( 
        '_'
        .join(
            no_pro_cara
            .split(' ')
        ) 
    )
    
    return  preffix + '_' + no_spaces