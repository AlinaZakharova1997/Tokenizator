'''
SearchEngine
This module does searching for positions of tokens in database
'''
import os
import shelve
import indexer
from indexer import Indexer, Position_Plus

class SearchEngine(object):
    '''
    class SearchEngine
    @param database: datadase of tokens and thier positions
    '''
    
    def __init__(self,database):

        self.database = shelve.open(database,writeback=True)
            
    def get_dict (self,tok_str):
        '''
        This function performs searching for positions of a given token
        @param tok_str: str containing token
        @return: dictionary, where a key is a filename
        and a value is a list of positions
        ''' 
        
        if  not isinstance(tok_str,str):
            raise TypeError('Input has an unappropriate type!')

        if tok_str in self.database:
            return self.database[tok_str]
