"""
SearchEngine
This module does searching for positions of tokens in database
"""
import os
import shelve
import indexer
from indexer import Indexer, Position_Plus
import tokenizator
from tokenizator import Tokenizator


class SearchEngine(object):
    """
    class SearchEngine
    @param database: datadase of tokens and thier positions
    """
    
    def __init__(self,database):

        self.database = shelve.open(database,writeback=True)
        self.tokenizator = Tokenizator()

    def __del__(self):
        self.database.close()    
            
    def get_dict (self,tok_str):
        """
        This function performs searching for positions of a given token
        @param tok_str: str containing token
        @return: dictionary, where a key is a filename
        and a value is a list of positions
        """
        
        if  not isinstance(tok_str,str):
            raise TypeError('Input has an unappropriate type!')

        if tok_str in self.database:
            return self.database[tok_str]
        else:
            return {}

    def get_dict_many_tokens(self,tok_str):
        """
        This function performs searching for positions of given tokens
        @param tok_str: str containing tokens
        @return: dictionary, where a key is a filename
        and a value is a list of positions of all tokens     
        """

        if not isinstance(tok_str, str):
            raise TypeError('Input has an unappropriate type!')
       
        big_dict_files = []
        values = []
        
        for token in self.tokenizator.token_gen(tok_str):
            big_dict_files.append(self.get_dict(token.s))
            values.append((self.get_dict(token.s)).values())
        print(values)    
        files = set(big_dict_files[0])    
        for file_dict in big_dict_files[1:]:
            files = files.intersection(set(file_dict)) #пересечение файлов
            
        allpos = [values[0]]
        for filepos in values[1:]:
            allpos = allpos + values[1:]
            
        allpos_new = []
        for pos in allpos:
            if pos not in allpos_new:
                allpos_new.append(pos)              
            
        output_dict = {}    
        for filename in files:
            for pos in set(allpos_new):
                output_dict.setdefault(filename,[]).extend(pos)
        return output_dict
        
        
            

            
          
