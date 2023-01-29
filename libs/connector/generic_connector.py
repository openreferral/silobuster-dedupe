'''
Postgres converter.
Accepts Postgres Source connections.

Transform function takes any number of functions to transform the data and then
logs the transformations and writes the final, transformed records.

'''
import pandas as pd

from libs.connector.base_connector import BaseConnector
from libs.handler.postgres_handler import PostgresHandler



class GenericConnecter(BaseConnector):
    
    def __init__(
            self, 
            input_source: object, 
            output_source: object, 
            log_source: object,
            input_fields: list, 
            output_fields: list
        ):

        self.__input_source = input_source
        self.__log_source = log_source
        self.__output_source = output_source
        self.__input_fields = input_fields
        self.__output_fields = output_fields


    @property
    def input_source(self) -> object:
        return self.__input_source


    @property
    def log_source(self) -> object:
        return self.__log_source


    @property
    def output_source(self) -> object:
        return self.__output_source


    @property
    def input_fields(self) -> list:
        return self.__input_fields


    @property
    def output_fields(self) -> list:
        return self.__output_fields


    @property
    def df(self) -> pd.DataFrame:
        return self.__df


    def transform(self, write_logs: bool=True, *funcs):

        for func in funcs:
            new_df = self.__df.copy()
            func(new_df)

