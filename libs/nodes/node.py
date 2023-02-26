import pandas as pd

from libs.silobuster_exceptions.nodes_exceptions import NodeException, RelationDoesNotExist


class Node:
    '''
    Nodes are a representation of an object that relational databases typically model as a table. Attributes are considered concrete data that are absolute or are derived by a consensus of contributor
    data sources. 
    
    Nodes have these main properties, represented by columns:
    
    1. node group: Traditional name of a table
    2. relations: mapping to other nodes
    3. attributes: concrete data
    4. aliases: representations of the node from multiple data sources
    5. legecy_keys: temporary mappings of keys left over from ingestion of contributor data

    Nodes are stored in the same table. They operate on the principle of storing data more closely related to how data is accessed in programming. One-to-one relationships are simply extensions of the same 
    array and so do not exist. One-to-many relationships are simply nested arrays, and so forth. By simplifying how the data is stored, a more "canonical representation can be achieved.

    All ids are unique uuids. Defining relationships using ids ensures that the right element is node is reference.
    '''
    def __init__(self, node_group: str):
        self.__node_group = node_group
        self.__relations = dict()
        self.__legacy_keys = dict()
        self.__df = pd.DataFrame

    @property
    def node_group(self):
        return self.__node_group
    

    def get_relation(self, node_group: str):
        '''
        Relations are a hash of: "foreign node group (table) and a the value being an array of ids in that node group.
        '''
        ids = self.__relations.get(node_group)
        if not ids:
            raise RelationDoesNotExist(relation=node_group)
        
        return ids
    
    
    def set_relation(self, foreign_table: str, ids: list):
        self.__relations[foreign_table] = ids

    
    def get_legacy_key(self, node_group: str, attribute_name: str):
        key_group = self.__legacy_keys.get(node_group)
        if not key_group:
            raise RelationDoesNotExist(relation=key_group)
        
        ids = key_group.get(attribute_name)
        if not ids:
            raise RelationDoesNotExist(relation=attribute_name)
        return ids
    
    
    def set_legacy_key(self, node_group: str, attribute_name: str, ids: list):
        self.__legacy[node_group][attribute_name] = ids

    
    def get_aliases(self, **kwargs):
        self.__df['aliases'].filter()


    def df(self):
        return self.__df
    


