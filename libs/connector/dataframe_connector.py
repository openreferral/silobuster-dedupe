'''
Connectors of type "Dataframe" either accept input or they output to a Pandas DataFrame. These connectors are used in chaining multiple connectors together to perform complex operations.
'''
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

    