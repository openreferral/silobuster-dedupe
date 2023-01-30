'''
Postgres converter.
Accepts Postgres Source connections.

Transform function takes any number of functions to transform the data and then
logs the transformations and writes the final, transformed records.

'''
import pandas as pd

from libs.connector.generic_connector import GenericConnecter

from libs.log_handler.log_handler import LogHandler
from libs.handler.postgres_handler import PostgresHandler

from libs.uuid import random_uuid


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

    
