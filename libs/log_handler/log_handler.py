import pandas as pd 
import json

from libs.handler.base_handler import BaseHandler, BaseDBHandler
from libs.silobuster_exceptions.type_exceptions import HandlerError

from libs.dataframes.to_types import to_list_of_dicts
from libs.dataframes.encoders import NpEncoder
from libs.uuid import random_uuid


class LOG_DESTINATION:
    DB = 1
    JSON = 2


class LogHandler:

    insert_query = ''
    def __init__(self, default_destination: LOG_DESTINATION='db', db_handler: BaseDBHandler=None):
        self.__db_handler = db_handler

        
        if self.db_handler:
            self.db_handler.query = "INSERT INTO logs (log_message, id, job_id, iteration_id, step_name, contributor_name) VALUES (%s, %s, %s, %s, %s, %s)"
            # self.db_handler.query = "INSERT INTO logs (id, log_message) VALUES ('1', %s)"

        self.default_destination = default_destination


    @property
    def default_destination(self) -> str:
        return self.__default_destination

    
    @default_destination.setter
    def default_destination(self, value: str):
        dest_type = getattr(LOG_DESTINATION, value.upper())
        
        if dest_type == LOG_DESTINATION.DB:
            if not self.db_handler:
                raise HandlerError('db_handler for log handler expects a type inherited from (BaseDBHandler).')

        self.__default_destination = dest_type


    @property
    def db_handler(self):
        return self.__db_handler


    def create_log_message(self, original_data: pd.DataFrame, results: pd.DataFrame, *args, **kwargs):

        id = str(random_uuid())
        fields = id, kwargs.get('job_id'), kwargs.get('iteration_id'), kwargs.get('step_name'), kwargs.get('contributor_name')

        print ('fields')
        print (fields)
        print (*fields)
        for arg in args:
            if arg == 'dedupe_results':
                return self.create_log_message_dedupe(results, *fields)

        final_obj = dict()

        final_obj['original'] = to_list_of_dicts(original_data)
        final_obj['results'] = to_list_of_dicts(results)

        changes_flag = False
        if kwargs.get('changes'):
            changes_flag = True
            changes = kwargs.get('changes')
            if isinstance(changes, pd.DataFrame):
                final_obj['changes'] = to_list_of_dicts(changes)

            elif isinstance(changes, list) or isinstance(changes, dict):
                final_obj['changes'] = changes
            
        
        if kwargs.get('get_changes') and not changes_flag:
            final_obj['changes'] = 'todo. must get changes'


        return final_obj, *fields


    def create_log_message_dedupe(self, results: pd.DataFrame, *args):
        print (*args)
        return to_list_of_dicts(results), *args
        

    def _log_to_db(self, log_message: str, *args) -> bool:
        
        '''
        This code serializes and writes to the db individual records as was previously.
        '''
        # id, job_id, iteration_id, step_name, contributor_name, log_message
        # for row in log_message:
        #     print (json.dumps(row, cls=NpEncoder))
        #     self.db_handler.execute(self.db_handler.query, ('1', '2', '3', '4', '5', json.dumps(row, cls=NpEncoder)))
        # return True
        # return log_message
        print (args)
        print (*args)
        self.db_handler.execute(self.db_handler.query, (json.dumps(log_message, cls=NpEncoder), *args))
    
    

    def log(self, original_data: pd.DataFrame, results: pd.DataFrame, *args, **kwargs) -> bool:
        
        values = self.create_log_message(original_data, results, *args, **kwargs)
        if self.default_destination == LOG_DESTINATION.DB:
            return self._log_to_db(*values)


    