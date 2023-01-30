'''
Postgres converter.
Accepts Postgres Source connections.

Transform function takes any number of functions to transform the data and then
logs the transformations and writes the final, transformed records.

'''
import pandas as pd

from libs.connector.base_connector import BaseConnector
from libs.handler.base_handler import BaseHandler

from libs.uuid import random_uuid
from libs.dataframes.to_types import to_list_of_dicts


class GenericConnecter(BaseConnector):
    
    def __init__(
            self, 
            input_handler: BaseHandler, 
            output_handler: BaseHandler, 
            log_handler: BaseHandler,
            write_logs: bool
        ):

        self.__input_handler = input_handler
        self.__log_handler = log_handler
        self.__output_handler = output_handler
        self.__write_logs = write_logs        

    @property
    def input_handler(self) -> object:
        return self.__input_handler


    @property
    def log_handler(self) -> object:
        return self.__log_handler


    @property
    def output_handler(self) -> object:
        return self.__output_handler


    @property
    def write_logs(self) -> bool:
        return self.__write_logs


    @write_logs.setter
    def write_logs(self, value: bool):
        self.__write_logs = value


    @property
    def df(self) -> pd.DataFrame:
        return self.__df


    @df.setter
    def df(self, value: pd.DataFrame):
        self.__df = value


    @staticmethod
    def parse_steps(steps: dict):
        all_funcs = list()
        for func_name, path in steps.items():
            exec(f'from {path} import {func_name}')
            all_funcs.append(eval(func_name))
        return all_funcs


    def transform(self, *funcs):
        job_id = str(random_uuid())
        
        # Unpack lists that may by passed either directly or by parse_steps
        all_funcs = list()
        for func in funcs:
            if isinstance(func, list):
                all_funcs.append(*func)
            else:
                all_funcs.append(func)

        for func in all_funcs:
            if self.write_logs and self.log_handler:
                new_df = self.df.copy()
                results, changes, *additional_args = func(new_df)            
                self.log_handler.log(results, changes, *additional_args, job_id=job_id, step_name=func.__name__)

            else:
                func(self.df)

            self.df = new_df

            
            return to_list_of_dicts(new_df)

