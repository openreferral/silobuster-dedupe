
class LogError(Exception):
    def __init__(self):
        pass

class LogTypeNotImplemented(LogError):
    def __init__(self, log_type):
        self.log_type = log_type


class InvalidQueryParams(LogError):
    def __init__(self, **params):
        self.params = params


class LogDoesNotExist(LogError):
    def __init__(self, **params):
        self.params = params


class LogMessageIncorrectlyFormatted(LogError):
    def __init__(self, **params):
        self.params = params