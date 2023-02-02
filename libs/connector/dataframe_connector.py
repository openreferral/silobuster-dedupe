import pandas as pd

from libs.connector.generic_connector import GenericConnecter


class DataframeToDataframeConnector:

    def __init__(self, df: pd.DataFrame):

        self.read()
        self.__df = df


    def read(self):
        pass

    def write(self):
        return self.df.copy()

    