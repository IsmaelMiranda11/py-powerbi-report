'''Module for class to work with model of PBI

'''

import subprocess
import re
import json
import clr
import os
import pandas as pd
from typing import Any, Literal, Optional, Union

from ..constants import dax_code
from ..functions.functions import ( 
    get_parent_dir_path, format_column_width, set_attrs_name )

# Adding the dll for connect to AS in windows
clr.AddReference(fr'{get_parent_dir_path(__file__)}'
                 r'\ms_dll_scripts\Microsoft.AnalysisServices.Core.dll'
                 ) # type: ignore
clr.AddReference(fr'{get_parent_dir_path(__file__)}'
                 r'\ms_dll_scripts\Microsoft.AnalysisServices.Tabular.dll'
                 ) # type: ignore

import Microsoft.AnalysisServices as AS # type: ignore
import Microsoft.AnalysisServices.Tabular as Tabular # type: ignore

measure_obj = Tabular.Measure()

class PBIModel():
    '''Class to read PBI Analysis Services model and write in it

    '''

    def __init__(self, pbix_path:str) -> None:
        '''
        
        Attrs:
            pbix_path: Path of an open Power BI file.

        '''
        self.pbix_path = os.path.abspath(pbix_path)

        self.report_name = (
            self.pbix_path
            .split("\\")
            [-1]
            .replace(".pbix", '')
        ) #: Doc return name of original pbix file
        '''str: '''

        self.port_number = self.__get_analysis_server_port()
        self.model = self.__get_model()
        self.tables = self.__get_tables_model_name()

        self.__intellisense()
        
    def __get_analysis_server_port(self):
        '''
        Input:
            report_name (string): name of an open report in system
        Output:
            None

        Description:
            Read running processes in Windows system and get the port number of 
            the report.
            This function use a powershell script to get this information.
            This is an example of script output:
            {
                'PBI': [
                    {'Id': 5352, 'MainWindowTitle': 'Sample Report - Power BI Desktop'},
                    {'Id': 17568, 'MainWindowTitle': 'Sample Report with changes - Power BI Desktop'}
                ],
                'AS': [
                    {'ParentProcessId': 5352, 'CommandLine': '...'},
                    {'ParentProcessId': 17568, 'CommandLine': '...'}
                ]
            }
        '''

        # PowerShell scripts
        get_pbi_win_names = f'{get_parent_dir_path(__file__)}\ms_dll_scripts\get_open_reports.ps1'
        get_pbi_win_names = open(get_pbi_win_names).read()
        
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

        # Needs opened PBI
        if not processes_infos[:-1]:
            error_text = 'Is there any PBI file opened?'
            raise LookupError(error_text)
        
        # Load output as dict
        processes_dict = json.loads(processes_infos)

        # Search for report name
        for pbi in processes_dict.get('PBI'):
            name = ( 
                pbi
                .get('MainWindowTitle')
                [::-1]
                .split('-', 1)
                [-1]
                [::-1]
                .strip()
            )
            report_name = self.report_name.split('.')[0]
            if name == report_name:
                report_id = pbi.get('Id', None)
                break
            else:
                report_id = None
        
        if not report_id:
            error_text = f'''
                {self.report_name} PBI file is opened? It wasn\'t find in the processes
                '''
            raise LookupError(' '.join(error_text.split()))
            
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
        '''
        Input:
            None
        Output:
            None

        Description:
            Connect to Analysis Service server throught port and get the model.
        '''

        # Connect to server
        
        url_ = f'DataSource=localhost:{self.port_number}'
        server = Tabular.Server()
        server.Connect(url_)

        # For PBI, there is only one database
        db_name = str(server.Databases[0])

        # Get model from database

        return server.Databases.GetByName(db_name).Model
    
    def __get_tables_model_name(self):
        '''
        Input:
            None
        Output:
            None

        Description:
            Create a simple list of tables name in model
        '''

        tables_name = []
        for table in self.model.Tables:
            tables_name.append(table.Name)
        
        return tables_name

    def __intellisense(self):
        '''
        Add all table name and measure as attributes in the object
        ''' 
        # Iterate over all tables of model and get its name
        
        for table in self.model.Tables:
            tabela = Table(table)
            _name = tabela._attrs_name
            object.__setattr__(self, _name, tabela)

        return None
    


    def resume_tables_and_columns(self, export_to_excel=False):
        '''
        Input:
            export_to_excel (bool): create a excel file in folder
        Outpu:
            None
        Description

        '''
        
        # Initiate a information dict with Database e a empty list of tables
        info_dict = {}
        info_dict.setdefault('Tables', [])

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
                        # 'Object type': str(column.ObjectType),
                        'Data category': str(column.DataCategory),
                        'Modified time': str(column.ModifiedTime),
                        'Qualified Table Name': f'\'{str(column.Table.Name)}\'',
                        'Qualified Column Name': f'\'{str(column.Table.Name)}\'[{str(column.Name)}]'
                    }
                col_dict.update({'Column Infos': col_info_dict})
                table_dict.get('Table Columns').append(col_dict)

            info_dict.get('Tables').append(table_dict)


        df = ( 
            pd.DataFrame(info_dict)
            .pipe(lambda df: pd.json_normalize(df['Tables'], max_level=0))#.set_index(df.index))
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
            with pd.ExcelWriter(f'{self.report_name} model tables.xlsx') as excel:
                df.to_excel(excel, sheet_name='Model tables')
                format_column_width(df, excel, 'Model tables')
            _ = f'''
            Excel file {self.report_name} model tables.xlsx saved in the folder
            '''
            return ' '.join(_.split())
        else:
            return df
    
    def resume_measures(self, export_to_excel=False):
        '''
        Input:
            export_to_excel (bool): create a excel file in folder
        Outpu:
            None
        Description

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
                # if str(column.Type) != 'RowNumber':
                mea_dict.update({'Measure Name': measure.Name})
                mea_info_dict = {
                    'Description': str(measure.Description),
                    'Data type': str(measure.DataType),
                    'Expression': str(measure.Expression),
                    'Format string': str(measure.FormatString),
                    'Display folder': str(measure.DisplayFolder),
                    'Modified time': str(measure.ModifiedTime),
                    'Qualified name': f'\'{str(measure.Table.Name)}\'[{str(measure.Name)}]'
                }
        
                mea_dict.update({'Measure Infos': mea_info_dict})
                table_dict.get('Table Measures').append(mea_dict)

            info_dict.get('Tables').append(table_dict)

        
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
            with pd.ExcelWriter(f'{self.report_name} model measures.xlsx') as excel:
                df.to_excel(excel, sheet_name='Model measures')
                format_column_width(df, excel, 'Model measures')
            _ = f'''
            Excel file {self.report_name} model measures.xlsx saved in the folder
            '''
            return ' '.join(_.split())
        else:
            return df

    def export_excel_measure_creator(self,
            excel_file_name='ppr_measure_creator'
        ):
        df_fields = ( 
            self.resume_tables_and_columns()
            .pipe(lambda df: df[df['Type'] != 'RowNumber'])
            .reset_index()
            .sort_values(['Table Name', 'Column Name'])
            [['Table Name', 'Column Name', 'Description', 'Data type', 
              'Format string', 'Qualified Table Name', 'Qualified Column Name']
            ]
        )
        df_measures = ( 
            self.resume_measures()
            .reset_index()
            .sort_values(['Table Name', 'Measure Name'])
            [['Table Name', 'Measure Name', 'Description', 'Data type', 
              'Expression', 'Format string', 'Display folder',  
              'Qualified name']
            ]
        )
        df_measure_creator = (
            pd.DataFrame(
                {
                    'Table': ['Table must already exist, sorry!'],
                    'Name': ['Meaningful name, please'],
                    'Description': ['Be criative'],
                    'Expression': ['You might want use fields in the other sheet'],
                    'Display Folder': ['Example: folder\subfolder\otherfolder'],
                    'Format String': ['Like 0.00% or 0.00. Empty is cool, too']
                }
            )
        )

        with pd.ExcelWriter(f'{excel_file_name}.xlsx') as excel:
            df_fields.to_excel(excel, index=False,
                sheet_name='Fields'
            )
            df_measures.to_excel(excel, index=False,
                sheet_name='Measures'
            )
            df_measure_creator.to_excel(excel, index=False,
                sheet_name='Measure Creator'
            )
            # Column width           
            format_column_width(df_fields, excel, 'Fields')
            format_column_width(df_measures, excel, 'Measures')
            format_column_width(df_measure_creator, excel, 'Measure Creator')
        
        _ = f'''
        Excel file {excel_file_name}.xlsx saved in the folder
        '''
        return ' '.join(_.split())
    
    def __get_ppr_args(self, input_:str):
        '''
        '''
        pattern = r'(\([^)]*\)|[^|]+)'
        matches = re.findall(pattern, input_)

        result = []
        composite_element = ""
        for match in matches:
            match = match.strip() 
            if "(" in match:
                composite_element = match
            elif composite_element:
                composite_element += " | " + match
                if ")" in match:
                    result.append(composite_element[1:-1])
                    composite_element = ""
            else:
                result.append(match)

        if composite_element:
            result.append(composite_element)

        return result

    def ___expression_eval(add_measure_fun):
        '''
        Decorator to check if expression has any ppr_template_function.
        If yes, replace the expression for template compiled
        '''
        def expression_eval(self,*args, **kwargs):
            # Get the expression input
            _expression = kwargs.get('expression')
            
            # If not found, error
            if not _expression:
                error_text = f'\'expression\' input wasn\'t find'
                raise KeyError(error_text)
            
            # Loop up for ppr_function templates
            for templates in dax_code.DAX_PPR_TEMPLATE:
                template_name = templates.get('name')
                # Check if any function was found
                in_expression = re.search(pattern=template_name,string=_expression)
                # If exists any, modify expression
                if in_expression:
                    _ppr_args = re.findall('\((.*)\)', _expression) # between ()
                    if not _ppr_args:
                        error_text = f'''
                        It was not found arguments to function {template_name}.
                        This is the expected syntax: {templates.get('syntax')}.
                        The input was {_expression}
                        '''
                        raise KeyError(' '.join(error_text.split()))
                    
                    _ppr_fun_args = _ppr_args[0]
                    _ppr_fun_args = self.__get_ppr_args(_ppr_fun_args)
                    sub_dict = ( 
                        dict(
                            zip(
                                templates.get('expected_args'),
                                _ppr_fun_args
                            )
                        )
                    )

                    _template_expression = templates.get('dax_template')
                    for sub in sub_dict:
                        re_template = re.compile(sub)
                        re_arg = sub_dict.get(sub)
                        _template_expression = ( 
                            re_template
                            .sub(
                                repl=re_arg, 
                                string=_template_expression
                            )
                        )
                    
                    kwargs.update({'expression':_template_expression})

                    pass              
            
            return add_measure_fun(self,*args, **kwargs)

        return expression_eval

    @___expression_eval
    def add_measure_in_model(self,
            table_name,       
            name:str,
            expression:str,
            dispaly_folder:str,
            description:Optional[str] = 'Created with ppr',
            format_string:Union[str, None] = '0',
            if_exists: Literal['warn', 'delete'] = 'warn'
    ):
        # Initiate a Measure AS object
        tabular_measure = Tabular.Measure()
        # The table should exixts in the model
        try:
            tabular_table = self.model.Tables.Find(table_name)
            table_name = tabular_table.Name
        except:
            raise LookupError(f'{table_name} wasn\'t found in model')
              
        # Measure must be delete before create again in the model
        if if_exists == 'delete':
            # Might be the first insertion, so, pass it
            try:
                self.model.Tables.Find(table_name).Measures.Remove(name)
                self.model.SaveChanges()
            except:
                pass
        elif if_exists == 'warn':
            warn_text = f'''
            Measure {name} already in {table_name} in the model.
            If disered replace, chage if_exists to 'delete'
            '''
            raise Warning(warn_text)

        # Putting arguments into measure object
        tabular_measure.Name = name
        tabular_measure.Description = description
        tabular_measure.Expression = expression
        tabular_measure.DisplayFolder = dispaly_folder
        tabular_measure.FormatString = format_string
        
        # Add into table
        tabular_table.Measures.Add(tabular_measure)
        # Save changes in model
        self.model.SaveChanges()
        
        print(f'Measure {name} was added in table {table_name} in the model')

        return None
    
class Column():
    def __init__(self, table_name, column) -> None:
        self._name = column.Name
        self._attrs_name = set_attrs_name(column.Name, 'c')
        self.table_name = table_name
        self.fc_name = self._name
        self.visual_field_name = f"{self.table_name}.{self._name}"        
        self.qualified_name = f"'{self.table_name}'[{self._name}]"
    
    def __repr__(self) -> str:
        return f"'{self.table_name}'[{self._name}]"

        
class Measure():
    def __init__(self, table_name, measure) -> None:
        self._name = measure.Name
        self._attrs_name = set_attrs_name(measure.Name, 'm')
        self.table_name = table_name
        self.dax = measure.Expression
        
        self.fc_name = self._name
        self.visual_field_name = f"{self.table_name}.{self._name}"        
        self.qualified_name = f"'{self.table_name}'[{self._name}]"
    
    def __repr__(self) -> str:
        return f"'{self.table_name}'[{self._name}]"
    
    def __getattribute__(self, __name: str) -> Any:
        if __name == 'dax':
            dax_ = object.__getattribute__(self, __name)
            return dax_
        else:
            return object.__getattribute__(self, __name)
    

class Table():
    def __init__(self, table) -> None:
        self._name = table.Name
        self._attrs_name = set_attrs_name(table.Name, 't')
        # All columns
        for col in table.Columns:
            if str(col.Type) != 'RowNumber':
                column = Column(self._name, col)
                _name = column._attrs_name
                object.__setattr__(self, _name, column)
        # All measures
        for measure in table.Measures:
            column = Measure(self._name, measure)
            _name = column._attrs_name
            object.__setattr__(self, _name, column)
    
    def __repr__(self) -> str:
        return f"'{self._name}'"
    
