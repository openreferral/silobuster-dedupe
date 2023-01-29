

class ConnectionFailed(Exception):

    def __init__(self, msg: str=None, offending_paramater: str=None):
        self.msg = msg
        self.offending_parameter = offending_paramater


class PostgresConnectionFailed(ConnectionFailed):

    def __init__(self, msg: str=None, offending_paramater: str=None):
        self.msg = msg
        self.offending_parameter = offending_paramater
