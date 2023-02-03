'''
Postgres handlers connect to a postgres database and manage the connection. The class reads and writes to the database using the "execute" method.
'''

import os
import psycopg2
from psycopg2._psycopg import connection
from psycopg2 import extras


from libs.handler.base_handler import BaseDBHandler
from libs.silobuster_exceptions.connection_exceptions import PostgresConnectionFailed

from libs.silobuster_exceptions.query_exceptions import PostgresQueryError

from libs.globals.queries import ALLOWED_QUERIES



class PostgresHandler(BaseDBHandler):
    
    @classmethod
    def load_param(cls, param: str, env_name: str) -> str:
        '''
        Used to load settings, such as conenction configuration, from the ENVIRONMENT if none are passed.
        '''
        if param:
            return param

        val = os.environ.get(env_name)
        if not val:
            raise PostgresConnectionFailed('Could not initialize postgres connection. We tried to load from environment setting: ' + env_name, param)
        
        return val


    def __init__(self, db: str=None, username: str=None, password: str=None, host: str=None, port: int=None, query: str=None, schema: str='public', env_prefix: str="POSTGRES"):
        '''
        Accepts connection settings and an env_prefix. env_prefix defines the prefix in the ENVIRONMENT settings. For example, a prefix of POSTGRES will load the host name 
        from the POSTGRES_HOST ENVIRONMENT parameter.

        The query is unique what the handler is doing (i.e. input or output). It will either perform a read from the database or a write. This query is executed when the "read" or "write" methods 
        are called from the connector.
        '''

        # Set environment prefix to default if none
        if env_prefix is None:
            env_prefix = 'POSTGRES'
        self.__db = PostgresHandler.load_param(db, env_prefix + "_DB")
        self.__username = PostgresHandler.load_param(username, env_prefix + '_USERNAME')
        self.__password = PostgresHandler.load_param(password, env_prefix + '_PASSWORD')
        self.__host = PostgresHandler.load_param(host, env_prefix + '_HOST')
        self.__port = PostgresHandler.load_param(port, env_prefix + '_PORT')
        self.__schema = schema
        self.query = query

        
        self.__env_prefix = env_prefix

        self.__conn = psycopg2.connect(
            database=self.db,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
             options=f'-c search_path={schema}',
        )

    def __str__(self):
        msgs = list()
        msgs.append('Host: ' + self.host)
        msgs.append('Port: ' + str(self.port))
        msgs.append('Database: ' + self.db)
        msgs.append('Username: ' + self.username)
        msgs.append(f'Schema: {self.schema}')
        msgs.append('Connection Alive? ' + 'Yes' if self.is_alive else 'No')

        return '\n'.join(msgs)


    def __del__(self):
        '''
        Closes the connection automatically when the instance is deleted.
        '''
        try:
            self.__conn.close()
        except Exception as e:
            print (e)

    
    @property
    def env_prefix(self) -> str:
        return self.__env_prefix


    @property
    def schema(self) -> str:
        return self.__schema


    @property
    def host(self) -> str:
        return self.__host


    @property
    def port(self) -> int:
        '''
        Raises ValueError if the port is not an integer.
        '''
        try:
            return int(self.__port)
        except ValueError:
            raise ValueError('Port must be an integer')
        except Exception as e:
            raise e


    @property
    def query(self) -> str:
        return self.__query


    @query.setter
    def query(self, value: str):
        '''
        The query setter parses the querystring and removes newlines and double quotes from the beginning and the end of the string. This is helpful when passing a multiline string.
        '''
        if isinstance(value, str):
            formatted_query = value.strip().replace('\n', '')
            lst_query = list(formatted_query)
            
            while True:    
                break_flag = True
                if lst_query[0] == "'" or lst_query[0] == '"':
                    lst_query.pop(0)
                    lst_query.pop()
                    break_flag = False
                
                if break_flag:
                    break
            self.__query = ''.join(lst_query)
            
        else:
            self.__query = ''


    @property
    def db(self) -> str:
        return self.__db

    
    @property
    def username(self) -> str:
        return self.__username

    
    @property
    def password(self) -> str:
        return self.__password


    @property
    def connection(self) -> connection:
        return self.__conn


    @property
    def is_alive(self) -> bool:
        '''
        Returns whether the connection is "alive", or open.
        '''
        with self.connection.cursor() as cursor:
            cursor.execute("select version()")
            data = cursor.fetchone()
        
        if data is not None or data != '':
            return True

        return False


    def execute(self, query: str, args: list=None) -> object:
        '''
        Executes the query attribute. It checks whether the passed query is of an allowed querytype as defined in the ALLOWED_QUERIES found in the "globals" module. 
        Raises PostgresQueryError if the query is not allowed.
        '''        
        query_type = query.split(' ')[0].lower()

        if query_type == 'select':
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                try:
                    cursor.execute(query, args)
                except Exception as e:
                    raise PostgresQueryError(query, e)

                data = cursor.fetchall()

            return data
        
        elif query_type in ALLOWED_QUERIES:
            with self.connection.cursor() as cursor:
                try:
                    cursor.execute(query, args) 
                    self.connection.commit()           
                except Exception as e:
                    raise PostgresQueryError(query, '', e)

                affected = cursor.rowcount

            return affected

        raise PostgresQueryError(query, 'Query is not of allowed query type: ' + ", ".join(ALLOWED_QUERIES))


