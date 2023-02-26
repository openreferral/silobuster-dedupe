from libs.base_classes.base_iterator import BaseIterator

class Nodes(BaseIterator):

    def __init__(self):
        super().__init__(group_list=None, attr_key="id")
        self.__relations = list()
        
