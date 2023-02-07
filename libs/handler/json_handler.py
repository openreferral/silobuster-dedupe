'''
Json handlers return/serialize the connectors dataframe.
'''

import json

from libs.handler.base_handler import BaseHandler


class JsonHandler(BaseHandler):
    def __init__(self):
        pass


    def execute(self, data: dict) -> dict:
        '''
        The JsonHandler does not take any action on execute.
        '''
        pass

    @property
    def columns(self):
        pass