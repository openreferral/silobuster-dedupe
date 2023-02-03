'''
Postgres connectors are used to either connect to a Postgres database or write to a Postgres database.
'''

import pandas as pd
import json

from libs.connector.generic_connector import GenericConnecter

from libs.log_handler.log_handler import LogHandler
from libs.handler.postgres_handler import PostgresHandler
from libs.handler.json_handler import JsonHandler

from libs.uuid import random_uuid

from libs.dataframes.to_types import to_list_of_dicts


class PostgresToPostgresConnector(GenericConnecter):
    
    def __init__(
            self, 
            input_handler: PostgresHandler, 
            output_handler: PostgresHandler, 
            log_handler: LogHandler,
            write_logs: bool=True
        ):
        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)        
        self.read()


    @property
    def input_fields(self) -> list:
        return list(self.df.columns)


    @property
    def output_fields(self) -> list:
        s = self.output_handler.query
        fields = s[s.find("(")+1:s.find(")")]
        return [s.strip() for s in fields.split(',')]


    def read(self):
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.df = data_df


    def write(self):
        affected = self.output_handler.execute(self.output_handler.query)
        return affected

    
class PostgresToJsonConnector(GenericConnecter):
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
        self.read()


    @property
    def input_fields(self):
        '''
        Returns the columns (fields) of the Input Handler's query columns
        '''
        return list(self.df.columns)


    @property
    def output_fields(self):
        '''
        Returns the columns (fields) of the Out Handler's query columns
        '''
        return list(self.df.columns)

    
    def read(self):
        '''
        Calls the Handler's "execute" method and loads it into a dataframe.
        '''
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.df = data_df

    
    def write(self):
        '''
        The JsonHandler implements a null "execute" method because it does not handle any actual write operations. Instead, the write method returns the json data.
        '''
        return json.dumps(to_list_of_dicts(self.df))


    def transform(self, *funcs):
        job_id = super().transform(*funcs)
        return job_id

    
class PostgresToDataFrameConnector(GenericConnecter):
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
        self.read()


    @property
    def input_fields(self):
        return list(self.df.columns)


    @property
    def output_fields(self):
        return list(self.df.columns)

    
    def read(self):
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.df = data_df

    
    def write(self):
        '''
        The DataFrameHandler implements a null "execute" method because it does not handle any actual write operations. Instead, the write method returns a deep copy of the Connector instance dataframe.        
        '''
        return self.df.copy(deep=True)

