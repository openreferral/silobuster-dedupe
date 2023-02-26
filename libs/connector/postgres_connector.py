
'''
Postgres connectors are used to either connect to a Postgres database or write to a Postgres database.
'''

import pandas as pd
import json

from libs.connector.generic_connector import GenericConnecter

from libs.log_handler.log_handler import LogHandler
from libs.handler.postgres_handler import PostgresHandler
from libs.handler.json_handler import JsonHandler
from libs.handler.excel_handler import ExcelHandler


from libs.uuid import random_uuid

from libs.dataframes.to_types import to_list_of_dicts

class BasePostgresConnector(GenericConnecter):
    def __init__(
            self, 
            input_handler: PostgresHandler, 
            output_handler: PostgresHandler, 
            log_handler: LogHandler,
            write_logs: bool=True
        ):
        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)        
        
        if self.input_handler.query:
            self.read()

    def read(self):
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.df = data_df


class PostgresToPostgresConnector(BasePostgresConnector):
    
    def __init__(
            self, 
            input_handler: PostgresHandler, 
            output_handler: PostgresHandler, 
            log_handler: LogHandler,
            write_logs: bool=True
        ):
        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)        
        

    def write(self):
        affected = self.output_handler.execute(self.output_handler.query)
        return affected

    
class PostgresToJsonConnector(BasePostgresConnector):
    '''
    The write method returns a list of dictionaries that can then be serialized into JSON.
    '''
    def __init__(
            self,
            input_handler: PostgresHandler,
            output_handler: JsonHandler,
            log_handler: LogHandler,
            write_logs: bool=True,
        ):
        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)


    def write(self):
        '''
        The JsonHandler implements a null "execute" method because it does not handle any actual write operations. Instead, the write method returns the json data.
        '''
        return to_list_of_dicts(self.df)

    
class PostgresToDataFrameConnector(BasePostgresConnector):
    '''
    The Connector handles an input postgres connection and outputs a copy of its DataFrame. This is especially useful in chaining operations using a DataFrameTo_________Connector.
    '''
    def __init__(
            self,
            input_handler: PostgresHandler,
            output_handler: JsonHandler,
            log_handler: LogHandler,
            write_logs: bool=True,
        ):
        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)
        if self.input_handler.query:
            self.read()


    def read(self):
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.df = data_df

    
    def write(self):
        '''
        The DataFrameHandler implements a null "execute" method because it does not handle any actual write operations. Instead, the write method returns a deep copy of the Connector instance dataframe.        
        '''
        return self.df.copy(deep=True)



class PostgresToExcelConnector(GenericConnecter):
    '''
    The Connector handles an input postgres connection and outputs an excel filestream object.
    '''
    def __init__(
            self,
            input_handler: PostgresHandler,
            output_handler: ExcelHandler,
            log_handler: LogHandler,
            write_logs: bool=True,
        ):
        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)
        if self.input_handler.query:
            self.read()


    def read(self):
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.df = data_df

    
    def write(self, job_id: str=None):
        '''
        Returns a filestream object of an excel file
        '''
        return self.output_handler.execute(self.df)

