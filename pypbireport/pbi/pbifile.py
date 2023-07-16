'''
PBI File

Python 3.11.3
Developed by: Ismael Miranda
     E-mail : ismaelmiranda11@hotmail.com
'''

import tempfile
import zipfile
import codecs
import os

from ..functions.functions import encode_content
from ..constants.structures import *

class PBIXFile():
    '''
    Class to work with PBIX File
    '''
    def __init__(self, pbix_path):
        
        self.pbix_path = os.path.abspath(pbix_path)

        self.report_name = (
            self.pbix_path
            .split("\\")
            [-1]
            .replace(".pbix", '')
        ) # return name of original pbix file
        
        # Open the pbix file as a compressed file
        self.pbix = zipfile.ZipFile(
            file= pbix_path, 
            compression = zipfile.ZIP_DEFLATED 
            )
        
    
    def extract_layout_and_encoding(self):
        '''
        Input:
            None
        Output:
            None

        Description:
            Extract the Layout json file from report file.
        '''
        with self.pbix.open('Report/Layout', 'r') as f:
            content = f.read()
            layout_content = codecs.decode(content, 'utf-16-le')
        return layout_content

    def save_report(self, 
        layout_dict:str, 
        replace_original:bool=False, 
        suffix:str='ppr_out'
        ):
        '''
        Input:
            layout_dict (str): Layout dict (json) of a PBI report.
            replace_original (bool): If is true, the original report will be 
            replaced for a report with modification. Important: the original 
            file should be closed.
            suffix (str): You might want a suffix to reports create by module. 
            The default is ppr_out.
        Output:
            None

        Description:
            Consolidate the report layout_dict input in a new PBIX file.
        '''

        # 1. Create a temporary file in folder then closes it.
        t_file, t_name = (
            tempfile
            .mkstemp(
                dir = os.path.dirname(self.pbix_path)
            )
        )
        os.close(t_file)
        
        # 2. Run over all files in PBIX file and move them to temporary file 
    
        # List of unwanted files from original PBIX file
        no_to_copy = [
            'Report/Layout', # it will be replaced by modified dict in class 
            'SecurityBindings', # this file refers to original file and layout
            '[Content_Types].xml' # it refers to ignored SecurityBindings 
        ] # NOTE: SecurityBindings will be created after open PBIX file and save it.  
        
        # Loop over files
        with self.pbix as pbix_file, zipfile.ZipFile(t_name, 'w') as temp_zip:
            temp_zip.comment = pbix_file.comment
            for file in pbix_file.infolist():
                if not file.filename in no_to_copy:
                    temp_zip.writestr(file, pbix_file.read(file.filename))

        # 3. Put the layout dict modified in.
        with zipfile.ZipFile(file=t_name, 
            mode='a', 
            compression=zipfile.ZIP_DEFLATED
            ) as new_report:
            # Layout dict
            new_report.writestr(
                zinfo_or_arcname='Report/Layout', 
                data=encode_content(layout_dict, 'utf-16-le')
            )
            # Content xml
            new_report.writestr(
                zinfo_or_arcname='[Content_Types].xml', 
                data=encode_content(CONTENT_TYPE_XML)
            )

        # 4. Rename temporary file

        if replace_original:
            if os.path.exists(self.pbix_path):
                os.remove(self.pbix_path)
            file_name = self.report_name
        else:
            file_name = f'{self.report_name} {suffix}.pbix'    
            if os.path.exists(file_name): # if exists, delete
                os.remove(file_name)
        
        os.rename(t_name, file_name)

        return f'{file_name} created in folder'
    