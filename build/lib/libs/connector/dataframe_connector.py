'''
Connectors of type "Dataframe" either accept input or they output to a Pandas DataFrame. These connectors are used in chaining multiple connectors together to perform complex operations.
'''
import pandas as pd

from libs.connector.generic_connector import GenericConnecter
from libs.handler.dataframe_handler import DataFrameHandler
from libs.handler.postgres_handler import PostgresHandler
from libs.log_handler.log_handler import LogHandler

class DataFrameToDataFrameConnector(GenericConnecter):

    def __init__(self,
            input_handler: DataFrameHandler, 
            output_handler: PostgresHandler,
            log_handler: LogHandler,
            write_logs: bool=True
        ):

        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)        
        self.read()


    def read(self):
        pass


    def write(self):
        return self.df.copy()

    

class DataFrameToPostgresConnector(GenericConnecter):

    def __init__(self,
            input_handler: DataFrameHandler, 
            output_handler: PostgresHandler,
            log_handler: LogHandler,
            write_logs: bool=True
        ):

        super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)        
        self.read()

        
    def read(self):
        self.df = self.input_handler.df




    