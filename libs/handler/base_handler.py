from abc import ABC, abstractmethod


class BaseHandler(ABC):

    @abstractmethod
    def execute(self):
        pass


class BaseDBHandler(BaseHandler):

    @property
    @abstractmethod
    def db(self):
        pass


    @property
    @abstractmethod
    def username(self):
        pass


    @property
    @abstractmethod
    def password(self):
        pass


    @property
    @abstractmethod
    def host(self):
        pass


    @property
    @abstractmethod
    def port(self):
        pass


    @property
    @abstractmethod
    def query(self):
        pass

