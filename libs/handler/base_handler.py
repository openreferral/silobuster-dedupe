'''
All handlers implement the abstract BaseHandler class. It defines that each handler implement an "execute" method.

BaseDBHandler (Database handlers) must implement connection parameters.

Handlers are responsible for connecting to a source of data to either retrieve data or to write data. Connectors then implement these handlers to manage the input/output of data.
'''

from abc import ABC, abstractmethod


class BaseHandler(ABC):

    @abstractmethod
    def execute(self):
        pass


class BaseDBHandler(BaseHandler):

    @property
    @abstractmethod
    def db(self) -> str:
        pass


    @property
    @abstractmethod
    def username(self) -> str:
        pass


    @property
    @abstractmethod
    def password(self) -> str:
        pass


    @property
    @abstractmethod
    def host(self) -> str:
        pass


    @property
    @abstractmethod
    def port(self) -> str:
        pass


    @property
    @abstractmethod
    def query(self) -> str:
        pass


    @property
    @abstractmethod
    def columns(self) -> list:
        pass

