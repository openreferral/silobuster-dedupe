'''
Json handlers return/serialize the connectors dataframe.
'''

import io

import pandas as pd

from libs.handler.base_handler import BaseHandler


class ExcelHandler(BaseHandler):
    def __init__(self):
        pass


    def execute(self, data: object) -> dict:
        '''
        If data is of a DataFrame type, Returns a filestream of the excel document. If data is of a filestream type, returns a DataFrame.
        '''
        if isinstance(data, pd.DataFrame):
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')

            sheet_name = "Results"
            data.to_excel(writer, sheet_name=sheet_name)
            writer.save()
            output.seek(0)
            return output

    @property
    def columns(self):
        pass