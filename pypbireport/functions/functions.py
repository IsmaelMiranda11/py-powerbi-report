'''
General functions module to help in test or features
'''

import json
import secrets
import codecs

def export_dict_as_file(dict, file_name='Sample.json'):
    with open(file_name, 'w') as f:
        f.write(json.dumps(dict, indent=4))
    return None

def hex_code(prefix=''):
    return prefix + secrets.token_hex(nbytes=10)

def get_str_dict(dict={}, field_name=''):
    return json.loads(dict.get(field_name))

def encode_content(content, enconding='utf-8'):
    return codecs.encode(content, enconding)