'''
Postgres converter.
Accepts Postgres Source connections.

Transform function takes any number of functions to transform the data and then
logs the transformations and writes the final, transformed records.

'''
import pandas as pd

from libs.connector.base_connector import BaseConnector
from libs.log_handler.log_handler import LogHandler
from libs.handler.postgres_handler import PostgresHandler

from libs.uuid import random_uuid


class PostgresToPostgresConnector(BaseConnector):
    
    def __init__(
            self, 
            input_handler: PostgresHandler, 
            output_handler: PostgresHandler, 
            log_handler: LogHandler,
            write_logs: bool=True
        ):

        self.__input_handler = input_handler
        self.__log_handler = log_handler
        self.__output_handler = output_handler
        self.__write_logs = write_logs
        
        self.read()


    @property
    def write_logs(self) -> bool:
        return self.__write_logs


    @property
    def input_handler(self) -> PostgresHandler:
        return self.__input_handler


    @property
    def log_handler(self) -> LogHandler:
        return self.__log_handler


    @property
    def output_handler(self) -> PostgresHandler:
        return self.__output_handler


    @property
    def input_fields(self) -> list:
        return list(self.df.columns)


    @property
    def output_fields(self) -> list:
        s = self.output_handler.query
        fields = s[s.find("(")+1:s.find(")")]
        return [s.strip() for s in fields.split(',')]


    @property
    def df(self) -> pd.DataFrame:
        return self.__df


    # def log(self, results: object, changes: object, *args):
    #     formatted_changes = logger.format(results, changes, *args)
        


    def read(self):
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.__df = data_df


    def write(self):
        affected = self.output_handler.execute(self.output_handler.query)


    def transform(self, *funcs):
        job_id = str(random_uuid())

        for func in funcs:
            
            if self.write_logs and self.log_handler:
                new_df = self.__df.copy()
                results, changes, *additional_args = func(new_df)            
                self.log_handler.log(results, changes, *additional_args, job_id=job_id, step_name=func.__name__)

            else:
                func(self.__df)

            self.__df = new_df
            
            return changes

