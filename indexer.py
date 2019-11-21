"""
Indexator
This module performs indexing of a text in a given file
"""
import tokenizator
from tokenizator import Tokenizator
from functools import total_ordering
import shelve
import os

class Position(object):
    """
    Class Position
    Cointains positions of each token
    """

    def __init__(self, start, end):
        """
        @param start: position on the 1st element of a token
        @param end: position on the last element of a token
        """ 
        self.start = start
        self.end = end
        
    def __eq__(self, position):
      
        return self.start == position.start and self.end == position.end

    def __repr__(self):

        return str(self.start) + ',' + str(self.end)

@total_ordering
class Position_Plus(Position):
    """
    Class Position
    Cointains positions of each token
    """

    def __init__(self, lnumber, start, end):
        """
        @param start: position on the 1st element of a token
        @param end: position on the last element of a token
        @param lnumber: number of a line in a given text
        """
        
        self.start = start
        self.end = end
        self.lnumber = lnumber
        
    def __eq__(self, position):

        return self.lnumber == position.lnumber and self.start == position.start and self.end == position.end 

    def __lt__(self, other_pos):
        '''
        This function compares two positions, i.e. their parameters
        and returns the result of this comparison
        @param other_pos: position that is to be compared with self
        @return: comparison_result, i.e. True or False if one position less than another
        '''
        '''comparison_result = False
        if self.lnumber < other_pos.lnumber:
            comparison_result = True
        if self.lnumber == other_pos.lnumber:
            if self.start < other_pos.start:
                comparison_result = True
        return comparison_result'''
        return((self.lnumber < other_pos.lnumber) or ((self.lnumber == other_pos.lnumber) and(self.start < other_pos.start)))

    def __repr__(self):

        return str(self.lnumber) + ','+ str(self.start) + ',' + str(self.end)
          
class Indexer(object):
    """
    class Indexer
    Contains database with indexed tokens 
    """

    def __init__(self, database):
        """
        Constructor for an database
        @param database: element of Indexer,
        contains a dictionary where token is a key,
        and a value is a dictionary where the key is filename,
        and the value is a list of positions
        """
        self.database = shelve.open(database,writeback=True)
        self.tokenizator = Tokenizator()


    def __del__(self):
        self.database.close()
        

    def get_index(self, filename):
        """
        This function performs indexing of a text in a given file
        """
        if  not isinstance(filename, str):
            raise TypeError('Input has an unappropriate type!')
        my_file = open(filename)
        for token in self.tokenizator.token_gen(my_file.read()):
            start = token.position
            end = start + len(token.s)
            pos = Position(start, end)
            self.database.setdefault(token.s, {}).setdefault(filename, []).append(pos)
        my_file.close()    
            
    def get_index_with_line(self, filename):
        """
        This function performs indexing of a text in a given file
        """
        if  not isinstance(filename, str):
            raise TypeError('Input has an unappropriate type!')
        my_file = open(filename)
        for lnumber,line in enumerate(my_file):
            if not line:
                lnumber+=1
            for token in self.tokenizator.token_gen(line):
                start = token.position
                end = start + len(token.s)
                pos = Position_Plus(lnumber, start, end)
                self.database.setdefault(token.s, {}).setdefault(filename, []).append(pos)
            lnumber+=1
        my_file.close() 
