
class QueryError(Exception):

    def __init__(self, query: str, msg: str=None):
        self.msg = msg
        self.query = query


class PostgresQueryError(QueryError):

    def __init__(self, query: str, msg: str=None, e: Exception=None):
        self.msg = msg
        self.query = query
        