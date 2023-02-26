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
    

    def table_map(self):
        get_all_tables = f"""SELECT table_name FROM information_schema.tables
                WHERE table_schema = '{self.schema}'"""

        with self.connection.cursor() as cursor:
            cursor.execute(get_all_tables)
            t_names = cursor.fetchall()

        my_map = dict()
        for name in t_names:
            qry = f"SELECT column_name, data_type,is_nullable FROM information_schema.columns WHERE table_name = '{name[0]}'"
            with self.connection.cursor() as cursor:
                cursor.execute(qry)
                columns = cursor.fetchall()
            my_map[name[0]] = columns

        return my_map