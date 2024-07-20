'''Module to work with Power BI Model

'''

import os
import subprocess
import re
import json
from typing import Any, Literal, Optional, Union
import pandas as pd

from ..constants import dax_code
from ..functions.functions import (
    get_parent_dir_path, format_column_width, set_attrs_name )

'''
This module works with an interface with .net langage, using the runtime
environment of .net to acess Power BI Analysis Server when running.
The main libary to do this is pythonnet (https://github.com/pythonnet/pythonnet)
that provide a clr (common language runtime) to use DLL.
For everything to work fine, there must be imported dlls file to this module
'''
if os.name == 'nt': #only works for Windows
    import clr

    # Add dlls to runtime environment
    # clr.AddReference(fr'{get_parent_dir_path(__file__)}' # type: ignore
    #                  r'\ms_dll_scripts\Microsoft.AnalysisServices.Core.dll')
    clr.AddReference(fr'{get_parent_dir_path(__file__)}' # type: ignore
                    r'\ms_dll_scripts\Microsoft.AnalysisServices.Tabular.dll')

    # Import dlls as libaries
    # import Microsoft.AnalysisServices as AS # type: ignore
    import Microsoft.AnalysisServices.Tabular as Tabular # type: ignore

    # A mesure object of Tabular Model
    measure_obj = Tabular.Measure()

class PBIModel():
    '''Class to represent Power BI Analysis Services tabular model

    This class only works with opened model in memory. It is because the
    Power BI Analysis Services model is launched when the pbix file is opened.
    Data model inside zipped file is compressed.

    Args:
        pbix_path (str): Path of an opened Power BI file.

    Attributes:
        pbix_path (str): Path of the Power BI file.
        report_name (str): The name of Power BI report file.
        port_number (str): The number of Analysis Server port
        model (Tabular.Model): Tabular Analysis Server port model of the Power
            BI file.
        tables (list): A list of tables names inside the Power BI model.

    '''

    def __init__(self, pbix_path:str) -> None:
        self.pbix_path:str = os.path.abspath(pbix_path)

        self.report_name:str = (
            self.pbix_path
            .split("\\")
            [-1]
            .replace(".pbix", '')
        )

        # Get port number and the model
        self.port_number = self.__get_analysis_server_port()
        self.model = self.__get_model()
        # Collect tables names
        self.tables = self.__get_tables_model_name()

        # Assign model tables as attributes of the class
        self.__intellisense()

    def __get_analysis_server_port(self) -> str:
        '''Method to get the port number for Power BI file

        Read running processes in Windows system and get the port number of the
        report.
        This function use a `powershell` script to get this information.
        This is an example of PS script output:
        {
            'PBI': [
                {'Id': 5352, 'MainWindowTitle': 'Sample Report -
                    Power BI Desktop'},
                {'Id': 17568, 'MainWindowTitle': 'Sample Report with changes
                    - Power BI Desktop'}
            ],
            'AS': [
                {'ParentProcessId': 5352, 'CommandLine': '...'},
                {'ParentProcessId': 17568, 'CommandLine': '...'}
            ]
        }
        With PID number, other powershell script capture the CommandLine of
        process initialization, where is indicated the folder location of temp
        Analysis Server instance.
        The final part is read the file msmdsrv.port.txt with port number.

        Returns:
            str: The port number for the Power BI file.
        '''

        # PowerShell script to get running processes
        get_pbi_win_names = open(
            fr'{get_parent_dir_path(__file__)}\ms_dll_scripts'
            r'\get_open_reports.ps1'
            ).read()

        # Run PS script
        processes_infos = (
            subprocess
            .run(
                ["powershell", get_pbi_win_names],
                capture_output=True,
                encoding='utf8'
            )
            .stdout
        )

        # Verify if there is any pbi opened.
        if not processes_infos[:-1]:
            raise ValueError('Is there any PBI file opened?')

        # Load PS script output as a dictionary
        processes_dict = json.loads(processes_infos)

        # Search for report name to get PID of Power BI
        report_id = None #objective to find
        for pbi in processes_dict.get('PBI'):
            name = (
                pbi.get('MainWindowTitle')[::-1]
                .split('- Power BI Desktop', 1)
                [-1][::-1].strip()
            )
            if name == self.report_name:
                report_id = pbi.get('Id', None)
                break #get id and end seraching

        if not report_id:
            raise LookupError(f'"{self.report_name}" PBI file is opened? It '
                              'wasn\'t find in the processes')

        # Search for linked Analysis Server with report
        as_process = [
            as_
            for as_
            in processes_dict.get('AS')
            if as_.get('ParentProcessId') == report_id
        ][0]

        # Get the command line of AS process
        cl_as = as_process.get('CommandLine')

        # Extract the AnalysisServicesWorkspace path
        as_pattern = re.compile('-s \"(.*)\"')
        as_path = as_pattern.findall(cl_as)[0]

        # Get port number from path
        with open(f'{as_path}\\msmdsrv.port.txt', encoding='utf-16-Le') as f:
            port = f.read()

        return port

    def __get_model(self):
        '''Method to get the Tabular Model object of Power BI

        Connect to Analysis Service server throught clr and port number.
        This method use

        Returns:
            Tabular.Model: The data model of the Power BI file
        '''

        # Connect to server
        url_ = f'DataSource=localhost:{self.port_number}'
        server = Tabular.Server()
        server.Connect(url_)

        # For PBI, there is only one database
        db_name = str(server.Databases[0])

        # Get model from database
        return server.Databases.GetByName(db_name).Model

    def __get_tables_model_name(self) -> list:
        '''Method to create a simple list of tables name in model

        Returns:
            list: A list of model tables name.
        '''

        tables_name = []
        for table in self.model.Tables:
            tables_name.append(table.Name)

        return tables_name

    def __intellisense(self):
        '''Method to assign fields and measures as attributes of the class.

        This method use Table class. When initiated, the Table class will be
        assinged with fields and measures as attributes.

        '''

        # Iterate over all tables of model and get its name
        for table in self.model.Tables:
            tabela = Table(table)
            _name = tabela._attrs_name
            object.__setattr__(self, _name, tabela)

        return None

    def resume_tables_and_columns(self, export_to_excel:bool=False
        ) -> pd.DataFrame:
        '''Method to resume all tables and columns of the model

        Args:
            export_to_excel (bool): Export the dataframe as an excel file.

        Returns:
            pd.DataFrame: A dataframe with information of tables and columns of
                the Power BI data model.

        '''

        # Initiate a information dict with Database e a empty list of tables
        info_dict = {}
        info_dict.setdefault('Tables', [])

        # Get information
        for table in self.model.Tables:
            # Initiate a table dict
            table_dict = {}
            table_dict.update({'Table Name': table.Name})
            n_cols = table.Columns.Count
            table_dict.update({'Number of Columns': n_cols})
            table_dict.setdefault('Table Columns', [])
            for column in table.Columns:
                col_dict = {}
                # if str(column.Type) != 'RowNumber':
                col_dict.update({'Column Name': column.Name})
                col_info_dict = {
                        'Description': str(column.Description),
                        'Data type': str(column.DataType),
                        'Format string': str(column.FormatString),
                        'Sort by column': str(column.SortByColumn),
                        'Summarize by': str(column.SummarizeBy),
                        'Display folder': str(column.DisplayFolder),
                        'Display ordinal': str(column.DisplayOrdinal),
                        'Is unique': str(column.IsUnique),
                        'Is key': str(column.IsKey),
                        'Is hidden': str(column.IsHidden),
                        'Is nullable': str(column.IsNullable),
                        'Type': str(column.Type),
                        'Data category': str(column.DataCategory),
                        'Modified time': str(column.ModifiedTime),
                        'Qualified Table Name':
                            f'\'{str(column.Table.Name)}\'',
                        'Qualified Column Name':
                            f'\'{str(column.Table.Name)}\'[{str(column.Name)}]'
                    }
                col_dict.update({'Column Infos': col_info_dict})
                table_dict.get('Table Columns', []).append(col_dict)

            info_dict.get('Tables', []).append(table_dict)

        # Assemble the pandas dataframe
        df = (
            pd.DataFrame(info_dict)
            .pipe(lambda df: pd.json_normalize(df['Tables'], max_level=0))
            .explode('Table Columns')
            .pipe(
                lambda df:
                    df
                    .drop(columns='Table Columns')
                    .drop_duplicates()
                    .join(
                        pd.json_normalize(
                            df['Table Columns'], max_level=0
                        )
                        .set_index(df.index)
                    )
            )
            .reset_index(drop=True)
            .pipe(
                lambda df:
                    df
                    .drop(columns='Column Infos')
                    .drop_duplicates()
                    .join(
                        pd.json_normalize(
                            df['Column Infos'], max_level=0
                        )
                        .set_index(df.index)
                    )
            )
            .set_index(['Table Name', 'Number of Columns', 'Column Name'])
        )

        if export_to_excel:
            excel_name = f'{self.report_name} model tables.xlsx'
            with pd.ExcelWriter(excel_name) as excel:
                df.to_excel(excel, sheet_name='Model tables')
                format_column_width(df, excel, 'Model tables')

            print(f'Excel file {excel_name} saved in the folder')

        return df

    def resume_measures(self, export_to_excel:bool=False) -> pd.DataFrame:
        '''Method to resume the measures of the model

        Args:
            export_to_excel (bool): Export the dataframe as an excel file.

        Returns:
            pd.DataFrame: A dataframe with information of measure of the Power
                BI data model.
        '''

        # Initiate a information dict with Database e a empty list of tables
        info_dict = {}
        info_dict.setdefault('Tables', [])

        for table in self.model.Tables:
            # Initiate a table dict
            if table.Measures.Count == 0:
                continue
            table_dict = {}
            table_dict.update({'Table Name': table.Name})

            n_measures = table.Measures.Count
            table_dict.update({'Number of Measures': n_measures})

            table_dict.setdefault('Table Measures', [])
            for measure in table.Measures:
                mea_dict = {}
                mea_dict.update({'Measure Name': measure.Name})
                mea_info_dict = {
                    'Description': str(measure.Description),
                    'Data type': str(measure.DataType),
                    'Expression': str(measure.Expression),
                    'Format string': str(measure.FormatString),
                    'Display folder': str(measure.DisplayFolder),
                    'Modified time': str(measure.ModifiedTime),
                    'Qualified name':
                        f'\'{str(measure.Table.Name)}\'[{str(measure.Name)}]'
                }

                mea_dict.update({'Measure Infos': mea_info_dict})
                table_dict.get('Table Measures', []).append(mea_dict)

            info_dict.get('Tables', []).append(table_dict)

        # Assemble the pandas dataframe
        df = (
            pd.DataFrame(info_dict)
            .pipe(lambda df: pd.json_normalize(df['Tables'], max_level=0))
            .explode('Table Measures')
            .pipe(
                lambda df:
                    df
                    .drop(columns='Table Measures')
                    .drop_duplicates()
                    .join(
                        pd.json_normalize(
                            df['Table Measures'], max_level=0
                        )
                        .set_index(df.index)
                    )
            )
            .reset_index(drop=True)
            .pipe(
                lambda df:
                    df
                    .drop(columns='Measure Infos')
                    .drop_duplicates()
                    .join(
                        pd.json_normalize(
                            df['Measure Infos'], max_level=0
                        )
                        .set_index(df.index)
                    )
            )
            .set_index(['Table Name', 'Number of Measures', 'Measure Name'])
        )

        if export_to_excel:
            excel_name = f'{self.report_name} model measures.xlsx'
            with pd.ExcelWriter(excel_name) as excel:
                df.to_excel(excel, sheet_name='Model measures')
                format_column_width(df, excel, 'Model measures')

            print(f'Excel file {excel_name} saved in the folder')

        return df

    def export_excel_measure_creator(self,
        excel_file_name:str='ppr_measure_creator'
        ) -> None:
        '''Method to export an auxiliar excel file to create measures.

        The `ppr_measure_creator` file is intended to be used in conjunction
        with the `add_measure_in_model` method.
        The format of the excel table is perfectly suited to be read by pandas
        and used for adding measures.

        Args:
            excel_file_name (str, optional): The name of excel file.
                Defaults to 'ppr_measure_creator'.

        '''

        # Prepare three sheets

        # Fields (columns) of the model
        df_fields = (
            self.resume_tables_and_columns()
            .pipe(lambda df: df[df['Type'] != 'RowNumber'])
            .reset_index()
            .sort_values(['Table Name', 'Column Name'])
            [['Table Name', 'Column Name', 'Description', 'Data type',
              'Format string', 'Qualified Table Name', 'Qualified Column Name']
            ]
        )
        # Existing measures in the model
        df_measures = (
            self.resume_measures()
            .reset_index()
            .sort_values(['Table Name', 'Measure Name'])
            .rename(columns={'Measure Name': 'Name', 'Table Name': 'Table'})
            [[
                'Table',
                'Name',
                'Description',
                'Expression',
                'Display folder',
                'Format string',
                'Qualified name',
                'Data type'
            ]]
        )
        # Measure creator template
        df_measure_creator = (
            pd.DataFrame(
                {
                    'Table': ['Table must already exist, sorry!'],
                    'Name': ['Meaningful name, please'],
                    'Description': ['Be criative'],
                    'Expression': ['DAX Code'],
                    'Display Folder':[r'Format: folder\subfolder\otherfolder'],
                    'Format String':['Like 0.00% or 0.00. Empty is cool, too']
                }
            )
        )

        # Assemle the excel file
        with pd.ExcelWriter(f'{excel_file_name}.xlsx', engine='xlsxwriter') \
            as excel:
            df_fields.to_excel(excel, index=False, sheet_name='Fields')
            df_measures.to_excel(excel, index=False, sheet_name='Measures')
            df_measure_creator.to_excel(excel, index=False,
                sheet_name='Measure Creator')
            # Correct the column width of pandas export
            format_column_width(df_fields, excel, 'Fields')
            format_column_width(df_measures, excel, 'Measures')
            format_column_width(df_measure_creator, excel, 'Measure Creator')

        print(f'Excel file {excel_file_name}.xlsx saved in the folder')

    def import_excel_measure_creator(self, file_name:str='ppr_measure_creator.xlsx', 
                                     sheet_name:str='Measure Creator',
                                     if_exists:Literal['warn', 'delete']='warn'):
        '''Method to import measures from an excel file

        This function read the `sheet_name` sheet of the `file_name` excel file
        and use the main columns to add measures in the model.
        The necessary columns are:
            - Table: The name of the table where the measure will be placed
            - Name: The name of the measure
            - Description: A description for the measure
            - Expression: The DAX expression of the measure
            - Display Folder: The folder where the measure will be placed
            - Format String: The format string of the measure

        Args:
            file_name (str): 
            sheet_name (str, optional): _description_. Defaults to 'Measure Creator'.
        '''

        # Read the excel file
        df = pd.read_excel(file_name, sheet_name=sheet_name)
        # Fill NaN with empty string, to not raise error in SASS server
        df = df.fillna('')

        # Iterate over the rows of the dataframe
        for _, row in df.iterrows():
            self.add_measure_in_model(
                table_name=row['Table'],
                name=row['Name'],
                expression=row['Expression'],
                display_folder=row['Display Folder'],
                description=row['Description'],
                format_string=row['Format String'],
                if_exists=if_exists
            )
        
        return None

    def add_measure_in_model(self,
            table_name:str,
            name:str,
            expression:str,
            display_folder:str = "",
            description:str = 'Created with ppr',
            format_string:str = '0',
            if_exists: Literal['warn', 'delete'] = 'warn'
        ):
        '''Method to add a measure into Power BI model

        This method works with clr. This collects the MeasureCollection of
        Table object of Model and add a measure with necessary fields.

        Args:
            table_name (str): The name where measure will be placed
            name (str): The name of the measure
            expression (str): DAX expression of the measure
            dispaly_folder (str, optional): The table folder of the meausre.
                Defaults to "".
            description (str, optional): A descrption for the measure. Defaults
                to 'Created with ppr'.
            format_string (str, optional): The format string of the measure.
                Defaults to '0'.
            if_exists (['warn', 'delete'], optional): Action to do if the
                measure is already present in the model. Defaults to 'warn'.

        Raises:
            ValueError: If the table isn't found in the model.
            Warning: If the measure already exists in the model.

        '''

        # Initiate a Measure AS object
        tabular_measure = Tabular.Measure()

        # The table should exixts in the model
        try:
            tabular_table = self.model.Tables.Find(table_name)
            table_name = tabular_table.Name
        except:
            raise ValueError(f'{table_name} wasn\'t found in model')

        # Check if the measure exists
        exists =bool(self.model.Tables.Find(table_name).Measures.Find(name))

        if if_exists == 'warn':
            if exists:
                raise Warning(f"Measure {name} already in {table_name} in the "
                              "model. If disered replace, chage if_exists to "
                              "'delete'")

        # Measure must be delete before create again in the model
        if if_exists == 'delete':
            if exists:
                self.model.Tables.Find(table_name).Measures.Remove(name)
                self.model.SaveChanges()

        # Putting arguments into measure AS object
        tabular_measure.Name = name
        tabular_measure.Description = description
        tabular_measure.Expression = expression
        tabular_measure.DisplayFolder = display_folder
        tabular_measure.FormatString = format_string

        # Add into model table
        tabular_table.Measures.Add(tabular_measure)

        # Save changes in model
        self.model.SaveChanges()

        print(f'Measure {name} was added in table {table_name} in the model')

        return None

class Column():
    '''Represents a column in Power BI model

    Attributes:
        _name (str): The name of the column
        _attrs_name (str): The attribute name for the column
        table_name (str): The parent table name of the column
        field_name (str): Name suited to visuals insert (Table.FieldName).
        qualified_name (str): Name suited to measures ('Table'[FieldName])
    '''
    def __init__(self, table_name, column) -> None:
        self._name = column.Name
        self._attrs_name = set_attrs_name(column.Name, 'c')
        self.table_name = table_name

        self.field_name = f"{self.table_name}.{self._name}"
        self.qualified_name = f"'{self.table_name}'[{self._name}]"

    def __repr__(self) -> str:
        return f"'{self.table_name}'[{self._name}]"


class Measure():
    '''Represents a measure in Power BI model

    Attributes:
        _name (str): The name of the measure.
        _attrs_name (str): The attribute name for the measure.
        table_name (str): The parent table name of the measure.
        field_name (str): Name suited to visuals insert (Table.FieldName).
        qualified_name (str): Name suited to measures ('Table'[FieldName])
        dax (str): The DAX expression of the measure.
    '''
    def __init__(self, table_name, measure) -> None:
        self._name = measure.Name
        self._attrs_name = set_attrs_name(measure.Name, 'm')
        self.table_name = table_name

        self.visual_field_name = f"{self.table_name}.{self._name}"
        self.qualified_name = f"'{self.table_name}'[{self._name}]"

        self.dax = measure.Expression

    def __repr__(self) -> str:
        return f"'{self.table_name}'[{self._name}]"

class Table():
    '''Represents a table in Power BI model

    Dynamics attributes are setted for table, namely columns and measures
    objects of the table.

    Attributes:
        _name (str): The name of the table
        _attrs_name: (str): The attribute name of the table
        *columns (Column): The columns of the table. The names begins with
            `c_`.
        *measures (Measure): The measures of the table. The names begins with
            `m_`

    '''
    def __init__(self, table) -> None:
        self._name = table.Name
        self._attrs_name = set_attrs_name(table.Name, 't')

        # The columns
        for col in table.Columns:
            if str(col.Type) != 'RowNumber':
                column = Column(self._name, col)
                _name = column._attrs_name
                object.__setattr__(self, _name, column)
        # The measures
        for measure in table.Measures:
            column = Measure(self._name, measure)
            _name = column._attrs_name
            object.__setattr__(self, _name, column)

    def __repr__(self) -> str:
        return f"'{self._name}'"