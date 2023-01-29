from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @property
    @abstractmethod
    def df(self):
        pass

    @property
    @abstractmethod
    def input_handler(self):
        pass

    @property
    @abstractmethod
    def output_handler(self):
        pass

    @property
    @abstractmethod
    def log_handler(self):
        pass

    @property
    @abstractmethod
    def write_logs(self):
        pass

    @property
    @abstractmethod
    def input_fields(self):
        pass

    @property
    @abstractmethod
    def output_fields(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def transform(self):
        pass


    

class BaseDbConnector(BaseConnector):
    pass
    