import pandas as pd


class Transformer:

    def __init__(self, data: pd.DataFrame):
        self.__data = data
        

    @property
    def data(self) -> pd.DataFrame:
        return self.__data



    def url(self, target_column: str='url') -> pd.DataFrame:
        pass
