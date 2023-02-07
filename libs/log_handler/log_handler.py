'''
The Log Handler (Connector) is a singleton Handler/Connector that manages the log system. It accepts a handler as its input/output handlers. If connecting to a database, it requires a table of the following format:

log_message: json
id: str/UUID
job_id: str/UUID
iteration_id: str/UUID
step_name: str
contributor_name: str

Writing logs: All connectors that perform an action will use the log handler to persist the logs of each step.
Retrieving logs: The log handler retrieves the logs in various formats (i.e. dataframe, json)
'''

import pandas as pd 
import json
import xlsxwriter

from libs.handler.base_handler import BaseHandler, BaseDBHandler
from libs.handler.postgres_handler import PostgresHandler
from libs.silobuster_exceptions.type_exceptions import HandlerError
from libs.silobuster_exceptions.log_exceptions import LogTypeNotImplemented

from libs.dataframes.to_types import to_list_of_dicts
from libs.dataframes.encoders import NpEncoder
from libs.uuid import random_uuid

from libs.base_classes.singleton import SingletonMeta

from libs.silobuster_exceptions.log_exceptions import InvalidQueryParams, LogDoesNotExist


class LOG_DESTINATION:
    DB = 1
    JSON = 2


class LogHandler(metaclass=SingletonMeta):

    insert_query = ''
    def __init__(self, default_destination: LOG_DESTINATION='db', db_handler: BaseDBHandler=None, REGISTERED_STEPS: dict=dict()):
        self.__db_handler = db_handler

        
        if self.db_handler:
            self.db_handler.query = "INSERT INTO logs (log_message, id, job_id, iteration_id, step_name, contributor_name) VALUES (%s, %s, %s, %s, %s, %s)"
            self.retrieve_query = 'SELECT log_message, id, iteration_id, step_name, contributor_name FROM logs'
        
        self.default_destination = default_destination


    def __str__(self):
        msgs = list()
        msgs.append(f'Default Destination: {self.default_destination}')
        if self.db_handler:
            msgs.append(f'DB handler host: {self.db_handler.host}')
            msgs.append(f'DB handler db: {self.db_handler.db}')
            msgs.append(f'DB handler username: {self.db_handler.username}')
            if isinstance(self.db_handler, PostgresHandler):
                msgs.append(f'DB handler schema: {self.db_handler.schema}')

            msgs.append('Connection Alive? ' + 'Yes' if self.db_handler.is_alive else 'No')
            
        return "\n".join(msgs)


    @property
    def retrieve_query(self) -> str:
        return self.__retrieve_query


    @retrieve_query.setter
    def retrieve_query(self, value: str):
        self.__retrieve_query = value


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
    def db_handler(self) -> BaseDBHandler:
        return self.__db_handler


    @db_handler.setter
    def db_handler(self, value: BaseDBHandler):
        if isinstance(value, BaseDBHandler):
            self.__db_handler = value


    def create_log_message(self, props: dict, *args, **kwargs):

        # Create the additional log fields
        id = str(random_uuid())
        fields = id, kwargs.get('job_id'), kwargs.get('iteration_id'), kwargs.get('step_name'), kwargs.get('contributor_name')
        final_obj = dict()
        
        
        for key, val in props.items():
            if isinstance(val, pd.DataFrame):
                final_obj[key] = to_list_of_dicts(val)

        # Create the changes unless specified not to or they already exist
        changes_flag = False
        if kwargs.get('changes'):
            changes_flag = True
            changes = kwargs.get('changes')
            if isinstance(changes, pd.DataFrame):
                final_obj['changes'] = to_list_of_dicts(kwargs.get('changes'))

            elif isinstance(changes, list) or isinstance(changes, dict):
                final_obj['changes'] = to_list_of_dicts('changes')
            
        # Compare the before and the after and get changes.
        if kwargs.get('get_changes') and not changes_flag:
            final_obj['changes'] = 'todo. must get changes'


        return final_obj, *fields


    def _log_to_db(self, props: dict, *args) -> bool:
        
        '''
        This code serializes and writes to the db individual records as was previously.
        Changed to blob format for speed.
        '''
        # id, job_id, iteration_id, step_name, contributor_name, log_message
        # for row in log_message:
        #     print (json.dumps(row, cls=NpEncoder))
        #     self.db_handler.execute(self.db_handler.query, ('1', '2', '3', '4', '5', json.dumps(row, cls=NpEncoder)))
        # return True
        # return log_message
        self.db_handler.execute(self.db_handler.query, (json.dumps(props, cls=NpEncoder), *args))
    
    

    def log(self, props: dict, *args, **kwargs) -> bool:
        
        values = self.create_log_message(props, *args, **kwargs)
        if self.default_destination == LOG_DESTINATION.DB or kwargs.get('destination') == 'db':
            return self._log_to_db(*values)
        else:
            raise LogTypeNotImplemented([kwargs.get('destination'), self.default_destination])


    def get(self, **kwargs) -> dict:

        
        # Check kwargs
        valid_params = False
        results = dict()
        
        if kwargs.get('id'):
            valid_params = True
            if isinstance(kwargs['id'], list):
                id = kwargs['id'][0]
            else:
                id = kwargs['id']
            results = self.db_handler.execute(self.retrieve_query + f' WHERE id = %s', [id])
        elif kwargs.get('job_id') and kwargs.get('step_name'):
            valid_params = True
            if isinstance(kwargs.get('job_id'), list):
                job_id = kwargs['job_id'][0]
            else:
                job_id = kwargs['job_id']
            if isinstance(kwargs['step_name'], list):
                step_name = kwargs['step_name'][0]
            else:
                step_name = kwargs['step_name']

            results = self.db_handler.execute(self.retrieve_query + f' WHERE job_id = %s AND step_name = %s', [job_id, step_name])
        

        if not valid_params:
            raise InvalidQueryParams(**kwargs)

        if not results:
            raise LogDoesNotExist(**kwargs)

        return results[0]

    
    def get_dataframe(self, message_part: str="results", **kwargs) -> object:

        record = self.get(**kwargs)
        data = (record['log_message'][message_part])
        return pd.DataFrame.from_dict(data)


    def create_excel(self, **kwargs):

        record = self.get(**kwargs)
        
        writer = pd.ExcelWriter(f'log_report_{record["id"]}_{record["step_name"]}.xlsx', engine='xlsxwriter')
        for key in record['log_message'].keys():
            df = pd.DataFrame.from_dict(record['log_message'][key])
            
            df.to_excel(writer, sheet_name=f'{key}')
        
        writer.close()
        return True
        

