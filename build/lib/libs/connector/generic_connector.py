'''
The generic connector inherits from the abstract BaseConnector class. This is the primary class to inherit connectors from, as it provides the methods for performing DataFrame operations.

All Connectors maintain an attribute "df", or DataFrame. Functions that mutate this dataframe are passed in the "transform" method. Once a transformation is complete, the "write" method then
handles the results by executing the output handler's execute action.
'''

import pandas as pd
import json

from libs.connector.base_connector import BaseConnector
from libs.handler.base_handler import BaseHandler
from libs.log_handler.log_handler import LogHandler


from libs.uuid import random_uuid
from libs.dataframes.to_types import to_list_of_dicts


HANDLER_METHODS = {
    1: 'original',
    2: 'enrich',
    3: 'join',
    10: 'transform',
}


class GenericConnecter(BaseConnector):
    
    def __init__(
            self, 
            input_handler: BaseHandler, 
            output_handler: BaseHandler, 
            log_handler: BaseHandler,
            write_logs: bool=True,
            jsonify: bool=True,
            STEPS: dict=dict(),
        ):
        self.__input_handlers = list()
        self.__input_handlers.append((input_handler, 1))
        self.__log_handler = log_handler
        self.__output_handler = output_handler
        self.__write_logs = write_logs        
        self.jsonify = jsonify


    @property
    def input_handler(self) -> BaseHandler:
        return self.__input_handlers[0][0]


    def get_input_handler(self, index: int) -> BaseHandler:
        return self.__input_handlers[index][0]


    @property
    def log_handler(self) -> LogHandler:
        return self.__log_handler


    @property
    def output_handler(self) -> BaseHandler:
        return self.__output_handler


    @property
    def input_columns(self) -> list:
        all_columns = list()
        for handler in self.__input_handlers:
            for column in handler[0].columns:
                all_columns.append(column)
        
        return all_columns


    @property
    def output_columns(self) -> list:
        return self.output_handler.columns


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


    def mutate(self, *funcs):
        '''
        Accepts a number of functions that mutate a dataframe and returns a dictionary. The return dictionary must have a 
        key of results and all keys in the dictionary must be arrays of records. Each function mutates the df attribute and the 
        logger logs each of the steps.
        '''
        
        if isinstance(funcs, dict):
            funcs = self.parse_steps(funcs)
        
        job_id = str(random_uuid())
        
        # Unpack lists that may by passed either directly or by parse_steps
        all_funcs = list()
        for func in funcs:
            if isinstance(func, list):
                all_funcs.extend(func)
            else:
                all_funcs.append(func)

        for func in all_funcs:
            if self.write_logs and self.log_handler:
                new_df = self.df.copy(deep=True)
                props = func(new_df)      
                
                self.log_handler.log(props, job_id=job_id, step_name=func.__name__)
                del new_df

            else:
                props = func(self.df)


            self.df = props.get('results')
        
        # Call this explicitly from other classes.
        # self.write()
        return job_id

    
    def transform(self, handler: BaseHandler, column_map: dict, func: object):
        '''
        Accepts a handler and a number of functions that mutate a dataframe using another dataframe and returns a dictionary. The return dictionary must have a 
        key of results and all keys in the dictionary must be arrays of records. Each function mutates the df attribute and the 
        logger logs each of the steps.

        Handlers of transform type do not take action on "refresh".
        '''
        #self.__input_handlers.append((handler, 10))
        #return super().transform(handler.df)
        pass

    def enrich(self, handler: BaseHandler, left_column: str, right_column: str):
        '''
        Accepts a handler, a left column (and existing column from the df attribute), and a right column (existing 
        column from the df argument). Extends the df attribute with the df argument using a left join.

        The handler is appended to the __input_handlers instance attribute. Whenever "refresh" is called, the handlers read their data source and recreate the DataFrame.
        '''
        self.__input_handlers.append((handler, 2))
        df = pd.DataFrame.from_records(handler.execute(handler.query))
        self.df = self.df = self.df.merge(self.df, df, how="left", left_on=left_column, right_on=right_column)



    def join(self, handler: BaseHandler, left_column: str, right_column: str, join_type: str="left"):
        '''
        Accepts a dataframe, a left column (and existing column from the df attribute), a right column (existing 
        column from the df argument), and a join type. Joins the df attribute with the new table.
        '''
        self.__input_handlers.append((handler, 3))        
        df = pd.DataFrame.from_records(handler.execute(handler.query))
        self.df = self.df.merge(df, how=join_type, left_on=left_column, right_on=right_column)
        

    def reduce(self):
        '''
        '''        
        pass


    def write(self):
        for index, row in self.df.iterrows():
            values = row.values
            formatted_values = list()
            if self.jsonify:
                for value in values:
                    if isinstance(value, dict) or isinstance(value, list):
                        formatted_values.append(json.dumps(value))
                    else:
                        formatted_values.append(value)

            try:
                self.output_handler.execute(self.output_handler.query, formatted_values)
            except Exception as e:
                print (e)

    
    def read(self):
        '''
        Calls the Handler's "execute" method and loads it into a dataframe.
        '''
        data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
        self.df = data_df
