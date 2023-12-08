'''Module for class to work with core file of PBI

The layout of a Power BI report comes from a JSON file name ``Layout`` inside 
the ``.pbix`` file.

The class ``PBIXFile`` means capture the file and delivery it for ``PBIReport``
class to work with.
'''

import json
import tempfile
import zipfile
import codecs
import os
import pathlib

from ..functions.functions import encode_content
from ..constants.structures import CONTENT_TYPE_XML

class PBIXFile():
    '''Class to work with PBIX File
    
    This class represent a Power BI report file (extesion of ``.pbix``).
    This class has two objectives:
        
        1. Extract the report layout JSON from a PBI report file.
        2. Save a new Power BI file with a report layout JSON.

    Note:
        This isn't prepare to work with PBIH files yet. The future plan is to
        manipulate report.json file directly.

    Args:
        pbix_path (str): Path of a PBIX file.

    Attributes:
        pbix_path (str): Path of a PBIX file.
        pbix (zipfile.ZipFile): Zip file with PBIX files.
            PBIX file are composed by a collection of compressed files. pbix
            variable is an instantiation of the zip file.
        report_name (str): The name of report. Simple fil name without .pbix
    '''

    def __init__(self, pbix_path:str) -> None:
        '''__init__ documentation'''
        self.pbix_path = os.path.abspath(pbix_path)

        self.report_name = (
            self.pbix_path
            .split("\\")
            [-1]
            .replace(".pbix", '')
        )

        # Call open PBIX file to initiate variable pbix
        self.__open_pbix_file()

    def __open_pbix_file(self) -> None:
        '''Method to open the zipped file of PBIX

        '''

        # Whenever it is necessary access PBIX files, it must defines a ZipFile
        self.pbix : zipfile.ZipFile = zipfile.ZipFile(file=self.pbix_path,
            compression = zipfile.ZIP_DEFLATED
        )

        return None

    def extract_layout_and_encoding(self) -> str:
        '''Method to return the report layout JSON as a string

        The `Layout` file is a JSON archive that contains all configuration of
        the Power BI report.
        This method reads the file and decodes it to a readable string for
        future serialization into a `dict` object.

        Returns:
            str: A string that represents the report layout JSON from Layout
                file.
        '''

        with self.pbix.open('Report/Layout', 'r') as f:
            content : bytes = f.read()
            layout_content : str = codecs.decode(content, 'utf-16-le')

        return layout_content


    def extract_layout(self) -> None:
        '''Method to extract the Layout file from pbix and save in folder.

        The `Layout` file is a JSON archive that contains all configuration of
        the Power BI report.
        This method simply extracts it from the PBIX zipped file and saves it
        in the working directory for consulting.

        Returns:
            None. Save a file with pattern layout_`report_name`.json in folder

        '''

        self.__open_pbix_file()
        # Extract the file
        with self.pbix as f:
            f.extract('Report/Layout')

        # Extracted file path
        current_path = pathlib.Path(self.pbix_path).parents[0]
        file_path = pathlib.Path(current_path, 'Report/Layout')

        # Read and save as a new file with indentation
        layout_file_json = pathlib.Path(file_path.parents[1],
            f'report_{self.report_name}.json')

        with open(layout_file_json, 'w') as f:
            with open(file_path, 'rb') as ff:
                d = json.load(ff)
                json.dump(d, fp=f, indent=4)

        # Remove extracted files from pbix
        file_path.unlink()
        file_path.parents[0].rmdir()

        return None

    def save_report(self, layout_dict:str, replace_original:bool=False,
        suffix:str='ppr_out', file_name:str|None=None, open_file:bool=False
        ) -> str:

        '''Method to save PBIX file hold as object of this class.

        This method works in the following steps:
            1. Create a temp file.
            2. Passes all files inside PBIX zipped file for temp file, expect
               ``Report/Layout``, ``SecurityBindings`` and
               ``Content_Types.xml``.
            3. Inserts ``Report/Layout`` with ``layout_dict`` written in proper
               encoding, as well as inserts ``Content_Types.xml`` file

        Note:
            SecurityBindings will be created after open PBIX file and save it.

        Args:
            layout_dict (str): Layout dict (json) of a PBI report.
            replace_original (bool, optional): If is true, the original report
                will be replaced for a report with modification. Important:
                the original file should be closed. Defaults to False.
            suffix (str, optional): You might want a suffix to report create by
                module. Defaults to 'ppr_out'.
            file_name (str | None, optional): Give desired name for new report.
                Defaults to None.
            open_file (bool, optional): Not implemented. Defaults to False.

        Returns:
            str: Confirmation that report was saved into folder
        '''

        # Garantee that file is open in memory
        self.__open_pbix_file()

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
        ]

        # Loop over files
        with self.pbix as pbix_file, zipfile.ZipFile(t_name, 'w') as temp_zip:
            temp_zip.comment = pbix_file.comment
            for file in pbix_file.infolist():
                if not file.filename in no_to_copy:
                    temp_zip.writestr(file, pbix_file.read(file.filename))

        # 3. Put the layout dict modified in
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
        if not file_name:
            if replace_original:
                if os.path.exists(self.pbix_path):
                    os.remove(self.pbix_path)
                file_name = self.report_name + '.pbix'
            else:
                file_name = f'{self.report_name} {suffix}.pbix'
                if os.path.exists(file_name): # if exists, delete
                    os.remove(file_name)

        try:
            os.rename(t_name, file_name)
        except:
            os.remove(t_name)

        # if open_file:
        #     os.system(file_name)

        return f'{file_name} created in folder'