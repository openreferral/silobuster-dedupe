
class NodeException(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args 
        self.kwargs = kwargs

class RelationDoesNotExist(NodeException):
    def __init__(self, relation: str):
        self.relation = relation
        