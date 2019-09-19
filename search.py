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
import windows
from windows import Context_Window
import re



class SearchEngine(object):
    """
    class SearchEngine
    """
    
    def __init__(self,database):
        """
        @param database: datadase of tokens and thier positions
        """

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
        if not tok_str:
            return {}
        big_dict_files = []
        for token in self.tokenizator.token_gen(tok_str):
            big_dict_files.append(self.get_dict(token.s))#выделяем токены и зап-ем в список
            
        files = set(big_dict_files[0])    
        for file_dict in big_dict_files[1:]:
            files = files.intersection(set(file_dict)) #пересечение названия файлов

        output_dict = {} 
        for filename in files:
            for token in self.tokenizator.token_gen(tok_str):
               output_dict.setdefault(filename,[]).extend(self.database[token.s][filename])
        return output_dict
            
    def unite_all(self,dictionary,win_size):
       '''
       This function unites context windows
       @param dictionary: input dictionary filename:Positions
       @param win_size: a size of a context window
       @return: a dictionary filename:Context Windows
       '''
       if not isinstance(dictionary, dict) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
      
       output_dict = {}
       
       # value is an array of positions
       for key,value in dictionary.items():
           # создаем список каждый раз, чтобы у каждого окна был свой список позиций  
           win_array = output_dict.setdefault(key, [])
           pos_array = value
           # for each position in values get window()
           for pos in pos_array:
               window = Context_Window.get_window(key, pos, win_size)
               win_array.append(window) 
       i = 0
       for key, win_array in output_dict.items():
           while i < len(win_array)-1:
               if win_array[i].is_crossed(win_array[i+1]):
                   win_array[i].get_united_window(win_array[i+1])
                   win_array.remove(win_array[i+1])
               else:
                   i+=1

       return output_dict
    
    def unite_extended(self, query, win_size):
        '''
        This function unites extended windows in a dictionary
        It takes query and win_size, makes a dictionary from query,
        than makes a new one but with windows as values,
        extends these windows and finally unites them once again
        @param query: string query
        @param win_size: size of a window
        @return: dictionary with extended and reunated windows
        '''
        
        if not isinstance(query, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
        
        to_dict = self.get_dict_many_tokens(query)
        dictionary = self.unite_all(to_dict, win_size)
        for value in dictionary.values():
            for window in value:
                window = Context_Window.extend_window(window)       
        i = 0
        for key, win_array in dictionary.items():
            while i < len(win_array)-1:
                if win_array[i].is_crossed(win_array[i+1]):
                    win_array[i].get_united_window(win_array[i+1])
                    win_array.remove(win_array[i+1])
                else:
                    i+=1
         
        return dictionary 
    
    def query_search(self, query, win_size):
        '''
        This function performs searching a query in database and returs
        a dictionary filemname:query in string format
        @param query: query to search
        @param win_size: a size of a context window
        @return: dictionary {filename: [query(str)]}
        '''
        if not isinstance(query, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
        
        output_dict = {} 
        dictionary = self.unite_extended(query, win_size)
        for key, value in dictionary.items():
            for window in value:
                string = window.highlight_window()
                output_dict.setdefault(key, []).append(string)
        return output_dict  

