
class HandlerError(TypeError):
    def __init__(self, msg):
        self.msg = 'Expecting a type of handler: ' + msg
