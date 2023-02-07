'''
Abstract class for connectors. A connector is used to connect to an input data source, perform data operations on the data, and output the results to some output data source. All connectors operations 
are performed in Pandas and are passed to the "transform" method as functions that accept a DataFrame and return a dictionary with a key of "results". In this way, multiple operations can mutate the data
in a single job. Jobs are then logged and a trace of operations can be retrieved.

By inheriting this class, polymorphism is ensured amongst all connectors so that code bases can expect the same interface.
'''

from abc import ABC, abstractmethod

from libs.handler.base_handler import BaseHandler
from libs.log_handler.log_handler import LogHandler

import pandas as pd


class BaseConnector(ABC):

    @property
    @abstractmethod
    def df(self):
        pass

    @property
    @abstractmethod
    def input_handler(self) -> BaseHandler:
        pass

    @abstractmethod
    def get_input_handler(self, index: int) -> BaseHandler:
        pass
    
    @property
    @abstractmethod
    def output_handler(self) -> BaseHandler:
        pass

    @property
    @abstractmethod
    def log_handler(self) -> LogHandler:
        pass

    @property
    @abstractmethod
    def input_columns(self) -> list:
        pass

    @property
    @abstractmethod
    def output_columns(self) -> list:
        pass

    @property
    @abstractmethod
    def write_logs(self) -> bool:
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def parse_steps(self):
        pass

    @abstractmethod
    def transform(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def enrich(self, df: pd.DataFrame, left_column: str, right_column: str):
        pass

    @abstractmethod
    def join(self, df: pd.DataFrame, left_column: str, right_column: str, join: str="left"):
        pass

    @abstractmethod
    def reduce(self):
        pass

    @abstractmethod
    def mutate(self, *funcs):
        pass
    

class BaseDbConnector(BaseConnector):
    pass
    