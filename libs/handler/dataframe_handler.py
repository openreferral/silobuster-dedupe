'''
Dataframe handlers return the dataframe of the connector
'''

import pandas as pd

from libs.handler.base_handler import BaseHandler


class DataFrameHandler(BaseHandler):
    def __init__(self, df: pd.DataFrame=pd.DataFrame()):
        self.__df = df.copy(deep=True)


    def execute(self, data: pd.DataFrame) -> dict:
        pass


    @property
    def df(self) -> pd.DataFrame:
        return self.__df
    
    
    @df.setter
    def df(self, value: pd.DataFrame):
        self.__df = value


    def columns(self):
        return self.df.columns