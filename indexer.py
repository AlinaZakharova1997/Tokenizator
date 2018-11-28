"""
Indexator
This module performs indexing of a text in a given file
"""
import tokenizator
from tokenizator import Tokenizator
import shelve
import os

class Position(object):
    """
    Class Position
    Cointains positions of each token
    @param start: position on the 1st element of a token
    @param end: position on the last element of a token
    """

    def __init__(self, start, end):
        
        self.start = start
        self.end = end

          
class Indexer(object):

    def __init__(self, database):
        """
        Constructor for a database
        @param database: element of Indexer,
        contains a dictionary where token is a key,
        and a value is a dictionary where the key is filename,
        and the value is a list of positions
        """
        self.database = shelve.open(database)

    def __del__(self):
        self.database.close()
        
    def get_index(self,filename):
        """
        This function performs indexing of a text in a given file
        """
        if  not isinstance(filename,str):
            raise TypeError('Input has an unappropriate type!')
        my_file=open(filename,encoding='utf-8')
        for token in self.tokenizator.token_gen(my_file.read()):
            start = token.position
            end = start + len(token.s)
            pos = Position(start,end)
            self.database.setdefault(token.s,{}).setdefault(filename,[]).append(pos)
        my_file.close()    
            

            
            


