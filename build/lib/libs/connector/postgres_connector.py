import psycopg2
import psycopg2.extras
from psycopg2.extras import (
   DictConnection,
   NamedTupleConnection,
   RealDictCursor,
   NamedTupleCursor
)
import os
import uuid
import json


from psycopg2.extras import register_hstore


# from libs.exceptions.connector.db_exceptions import (
#    PostgresConnectionError,
#    PostgresExecutionError,
#    PostgresInsertError,
#    PostgresUpdateError,
#    DatabaseError,
# )


from libs.connector.base_connector import BaseConnector


from typing import Union, List, Dict, Tuple, Any




class PostgresConnector(BaseConnector):
  
   def __init__(self, keep_alive: bool=False, host: str=None, port: str=None, user: str=None, password: str=None, database: str=None):
       self._connection = None
       self._cursor = None
       self._keep_alive = keep_alive
       self._connection_params = self._process_connection_params(host, port, user, password, database)




   def __del__(self):
       self.disconnect()




   def connect(self, cursor_factory: Union[RealDictCursor, NamedTupleCursor]=RealDictCursor):
       '''
       Creates a connection to the Postgres database and sets the cursor to the connection.
       '''
       try:
           self._connection: DictConnection = psycopg2.connect(**self._connection_params)
           # register_hstore(self.connection)
           self._cursor = self.connection.cursor(cursor_factory=cursor_factory)
       except psycopg2.OperationalError as e:
        #    raise PostgresConnectionError(e)
        pass




   @property
   def connection(self) -> Union[DictConnection, NamedTupleConnection]:
       '''
       Gets a connection to the database. If the connection is not open, it will open a new connection. To return a tuple cursor, use the connect
       property with the NamedTupleCursor class as the named cursor_factory argument.
       '''
       if not self._connection:
           self.connect()
      
       return self._connection




   @property
   def cursor(self) -> Union[RealDictCursor, NamedTupleCursor]:
       '''
       Gets a cursor to the database. If the cursor is not open, it will open a new cursor. To return a tuple cursor, use the connect method with the NamedTupleCursor class as
       the named cursor_factory argument.
       '''
       if not self._cursor:
           self.connect()
          
       return self._cursor
  


   def disconnect(self):
       '''
       Disconnects from the database. If the connection is open, it will close the connection and the cursor.
       '''
       if self.connection is not None:
               try:
                   self._connection.close()
                   self._connection = None
                   self._cursor = None


               except Exception as e:
                   return False
       return True




   def execute(self, query: str, args: List[Any]=False):
       '''
       Executes a query on the database. If the query has a RETURNING clause, it will return the records. Else, it will return None. If there are returning records, as in a select statement,
       it will return the records. If there is an error, it will raise a PostgresExecutionError. This method will try to commit the transaction if there are no results to fetch.
       Disconnect should be called after this method to close the connection.
       '''
       # Handle single argument
       if args and not isinstance(args, (list, tuple)):
           args = (args,)


       # Convert UUIDs to strings and adapt dictionaries
       if args and len(args) > 0:
           args = [self.adapt_python_value_to_postgres(arg) for arg in args]


       self.cursor.execute(query, args)


       try:
           self.connection.commit()
       except psycopg2.Error as e:
           pass # Pass silently. We just want to try to commit if there are no results to fetch.


       try:
           results = self.cursor.fetchall()
           self.disconnect()
           return results
       except:
           pass
          
      
       self.disconnect()




   def execute_many(self, query: str, data: Union[List[List[Any]], List[Tuple[Any]], Tuple[List[Any]], Tuple[Tuple[Any]]]):
       '''
       Executes a query on the database in batch. This method is useful for batch inserts. This method does not try to commit the transaction.
       '''
       formatted_data: list = []
       for row in data:
           formatted_data.append([self.adapt_python_value_to_postgres(value) for value in row])
       try:
           psycopg2.extras.execute_values(self.cursor, query, formatted_data)
           self.connection.commit()
       except psycopg2.Error as e:
           self.connection.rollback()
           self.disconnect()
        #    raise PostgresExecutionError(e)


       self.disconnect()




   def insert(self, query: str, args: Union[list[Any], Tuple[Any]]):
       """
       Inserts data into Postgres database and handles the RETURNING clause. If RETURNING is present, returns the records. Else, returns an empty list.
       """
       # Convert UUIDs to strings and adapt dictionaries
       args = [self.adapt_python_value_to_postgres(arg) for arg in args]


  
       inserted_rows = []
      
       try:
           self.cursor.execute(query, args)
           self.connection.commit()
       except Exception as e:
           # print (e)
           # print(self.cursor.mogrify(query, args))  # This will print the SQL query that will be executed
           self.connection.rollback()
           self.disconnect()
        #    raise PostgresInsertError(e.args)
          
       # Check if the query has a RETURNING clause by checking if the cursor has a description attribute. If it does, we will fetch the inserted rows and return them.
       if self.cursor.description is not None:
           inserted_rows = self.cursor.fetchall()
           self.disconnect()
           return inserted_rows
      
       self.disconnect()
       return None
      


   def insert_many(self, query: str, data: Union[List[List[Any]], List[Tuple[Any]], Tuple[List[Any]], Tuple[Tuple[Any]]]):
       """
       Inserts data into Postgres database and handles the RETURNING clause. If RETURNING is present, returns the records. Else, returns an empty list.
       """
       formatted_data: list = []
       for row in data:
           formatted_data.append([self.adapt_python_value_to_postgres(value) for value in row])
       try:
           psycopg2.extras.execute_values(self.cursor, query, formatted_data)
       except psycopg2.Error as e:
           self.connection.rollback()
           self.disconnect()
        #    raise PostgresInsertError(e.args)
      
       self.connection.commit()


       # Check if there is a RETURNING clause in the query. If there is, we will fetch the inserted rows and return them.
       if self.cursor.description is not None:
           inserted_rows = self.cursor.fetchall()
           self.disconnect()
           return inserted_rows


       self.disconnect()
       return None       
      




   def update(self, query: str, data: list):
       '''
       Not implemented. Use execute() to update a record in the database.
       '''
       raise NotImplementedError('This method is not yet implemented.')




   def fetch_one(self, query: str, args: Union[List[Any], Tuple[Any]]=None):
       '''
       Fetches one record from the database. If there is an error, it will raise a PostgresExecutionError.
       '''
       if args and len(args) > 0: 
           args = [self.adapt_python_value_to_postgres(arg) for arg in args]




       try:
           self.cursor.execute(query, args)
           results = self.cursor.fetchone()
           self.disconnect()
           return results
      
       except psycopg2.Error as e:
           self.disconnect()
        #    raise PostgresExecutionError(e)




   def fetch_all(self, query: str, args: Union[List[Any], Tuple[Any]]=None):
       '''
       Fetches all records from the database. If there is an error, it will raise a PostgresExecutionError.
       '''
       if args and len(args) > 0:
           args = [self.adapt_python_value_to_postgres(arg) for arg in args]


       try:
           self.cursor.execute(query, args)
           results = self.cursor.fetchall()
           self.disconnect()
           return results
       except psycopg2.Error as e:
           self.disconnect()
        #    raise PostgresExecutionError(e)




   @staticmethod
   def to_hstore(d):
       '''
       Used to convert a dictionary to an hstore string.
       '''
       return ', '.join([f'"{k}" => "{v}"' for k, v in d.items()])




   def adapt_python_value_to_postgres(self, value):
       '''
       Converts a Python value to a Postgres value. Handles UUIDs and dictionaries to hstore.
       '''
       if isinstance(value, dict):
       #     if len(value) == 0:
       #         return '{}'
       #     else:
             return json.dumps(value)


           # return self.to_hstore(value)
           # return psycopg2.extras.Json(value)
                  
       if isinstance(value, uuid.UUID):
           return str(value)
      
       return value






   # Initialize the connection parameters ////////////////////////////////////////////////////////////////////////////////////////////////
   def _process_connection_params(self, host: str, port: str, user: str, password: str, database: str): 
       '''
       Get connection parameters from environment variables by processing each envionment variable.
       '''
      
       if any(var is None for var in (host, port, user, password, database)):
           for key, value in os.environ.items(): # Scan for direct matches on POSTGRES. We want these to override everything.
               match key:
                   case 'POSTGRES_HOST':
                       host = value if not host else host
                   case 'POSTGRES_PORT':
                       port = value if not port else port
                   case 'POSTGRES_USERNAME':
                       user = value if not user else user
                   case 'POSTGRES_PASSWORD':
                       password = value if not password else password
                   case 'POSTGRES_DATABASE':
                       database = value if not database else database
      
       if any(var is None for var in (host, port, user, password, database)):
           for key, value in os.environ.items(): # Scan for direct matches on DATABASE. We want these to override next.
               match key:
                   case 'DB_HOST':
                       host = value if not host else host
                   case 'DB_PORT':
                       port = value if not port else port
                   case 'DB_USERNAME':
                       user = value if not user else user
                   case 'DB_PASSWORD':
                       password = value if not password else password
                   case 'DB_DATABASE':
                       database = value if not database else database
      
       if any(var is None for var in (host, port, user, password, database)):
           # Finally, we will look for a generic host and port, and a database name.
           for key, value in os.environ.items():
               if not host and 'host' in key.lower():
                   host = value if not host else host
               if not port and 'port' in key.lower():
                   port = value if not port else port
               if not user and 'username' in key.lower():
                   user = value if not user else user
               if not password and 'password' in key.lower():
                   password = value if not password else password
               if not database and 'database' in key.lower():
                   database = value if not database else database




       for key, value in os.environ.items():
          
           if key == 'POSTGRES_HOST':
               host = value if not host else host
           elif key == 'POSTGRES_PORT':
               port = value if not port else port
           elif key == 'DATABASE_USERNAME':
               user = value if not user else user
           elif key == 'DATABASE_PASSWORD':
               password = value if not password else password
           elif key == 'AUTH_POSTGRES_DATABASE':
               database = value if not database else database
      
    #    if any(var is None for var in (host, port, user, password, database)):
    #        raise PostgresConnectionError('Could not find all required environment variables for connection.')
  
       return {
           'host': host,
           'port': port,
           'user': user,
           'password': password,
           'database': database
       }



# '''
# Postgres connectors are used to either connect to a Postgres database or write to a Postgres database.
# '''

# import pandas as pd
# import json

# from libs.connector.generic_connector import GenericConnecter

# from libs.log_handler.log_handler import LogHandler
# from libs.handler.postgres_handler import PostgresHandler
# from libs.handler.json_handler import JsonHandler
# from libs.handler.excel_handler import ExcelHandler


# from libs.uuid import random_uuid

# from libs.dataframes.to_types import to_list_of_dicts

# class BasePostgresConnector(GenericConnecter):
#     def __init__(
#             self, 
#             input_handler: PostgresHandler, 
#             output_handler: PostgresHandler, 
#             log_handler: LogHandler,
#             write_logs: bool=True
#         ):
#         super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)        
        
#         if self.input_handler.query:
#             self.read()

#     def read(self):
#         data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
#         self.df = data_df


# class PostgresToPostgresConnector(BasePostgresConnector):
    
#     def __init__(
#             self, 
#             input_handler: PostgresHandler, 
#             output_handler: PostgresHandler, 
#             log_handler: LogHandler,
#             write_logs: bool=True
#         ):
#         super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)        
        

#     def write(self):
#         affected = self.output_handler.execute(self.output_handler.query)
#         return affected

    
# class PostgresToJsonConnector(BasePostgresConnector):
#     '''
#     The write method returns a list of dictionaries that can then be serialized into JSON.
#     '''
#     def __init__(
#             self,
#             input_handler: PostgresHandler,
#             output_handler: JsonHandler,
#             log_handler: LogHandler,
#             write_logs: bool=True,
#         ):
#         super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)


#     def write(self):
#         '''
#         The JsonHandler implements a null "execute" method because it does not handle any actual write operations. Instead, the write method returns the json data.
#         '''
#         return to_list_of_dicts(self.df)

    
# class PostgresToDataFrameConnector(BasePostgresConnector):
#     '''
#     The Connector handles an input postgres connection and outputs a copy of its DataFrame. This is especially useful in chaining operations using a DataFrameTo_________Connector.
#     '''
#     def __init__(
#             self,
#             input_handler: PostgresHandler,
#             output_handler: JsonHandler,
#             log_handler: LogHandler,
#             write_logs: bool=True,
#         ):
#         super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)
#         if self.input_handler.query:
#             self.read()


#     def read(self):
#         data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
#         self.df = data_df

    
#     def write(self):
#         '''
#         The DataFrameHandler implements a null "execute" method because it does not handle any actual write operations. Instead, the write method returns a deep copy of the Connector instance dataframe.        
#         '''
#         return self.df.copy(deep=True)



# class PostgresToExcelConnector(GenericConnecter):
#     '''
#     The Connector handles an input postgres connection and outputs an excel filestream object.
#     '''
#     def __init__(
#             self,
#             input_handler: PostgresHandler,
#             output_handler: ExcelHandler,
#             log_handler: LogHandler,
#             write_logs: bool=True,
#         ):
#         super().__init__(input_handler=input_handler, output_handler=output_handler, log_handler=log_handler, write_logs=write_logs)
#         if self.input_handler.query:
#             self.read()


#     def read(self):
#         data_df = pd.DataFrame.from_records(self.input_handler.execute(self.input_handler.query))
#         self.df = data_df

    
#     def write(self, job_id: str=None):
#         '''
#         Returns a filestream object of an excel file
#         '''
#         return self.output_handler.execute(self.df)

