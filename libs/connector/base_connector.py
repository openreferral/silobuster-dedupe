'''
Abstract class for connectors. A connector is used to connect to an input data source, perform data operations on the data, and output the results to some output data source. All connectors operations 
are performed in Pandas and are passed to the "transform" method as functions that accept a DataFrame and return a dictionary with a key of "results". In this way, multiple operations can mutate the data
in a single job. Jobs are then logged and a trace of operations can be retrieved.

By inheriting this class, polymorphism is ensured amongst all connectors so that code bases can expect the same interface.
'''

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
    def parse_steps(self):
        pass

    @abstractmethod
    def transform(self):
        pass


    

class BaseDbConnector(BaseConnector):
    pass
    