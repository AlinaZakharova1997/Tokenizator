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
            # sort positions
            output_dict[filename].sort()
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
       # тут окна объединяются
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
                # если функция только модифицирует и ничего не возвращает
                # вызывай ее вот так и не путай! здесь я расширяю окно до границ предложения
                window.extend_window()
                # print(window,'extended')
               
        
        # print('I want to reunite')
        for key, win_array in dictionary.items():
            # print("I am in for")
            i = 0
            while i < len(win_array)-1:
                # print('I am in while')
                if win_array[i].is_crossed(win_array[i+1]):
                    print(win_array[i].is_crossed(win_array[i+1]),'is crossed')
                    win_array[i].get_united_window(win_array[i+1])
                    print('get_united')
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
        print(dictionary,'dictionary')
        for key, value in dictionary.items():
            # print(value,'value')
            for window in value:
                string = window.highlight_window()
                # here it can highlight two words
                # print(string,'string')
                output_dict.setdefault(key, []).append(string)
        print(output_dict,'dict')        
        return output_dict  

    def qulim_search(self, query, limit, offset, doc_limof, win_size):
        '''
        This function performs searching a query in database and returs
        a dictionary filemname:query in string format
        @param query: query to search
        @param win_size: a size of a context window
        @param limit: max number of documents to show
        @param offset: document number to start with
        @param doc_limof: list of pairs that show limit and offset of each concrete document,
        no more quotes can be shown than this doclimit
        @return: dictionary {filename: [query(str)]}
        '''
        if not isinstance(query, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
        
        # dictionary for results
        output_dict = dict()
        # number of document
        qunum = 0
        dictionary = self.unite_extended(query, win_size)
        print(dictionary, 'dictionary')
        print(doc_limof,'doc_limof')
        for number, filename in enumerate(sorted(dictionary)):
            if number == limit + offset:
                break;
            if number >= offset and number < limit + offset:
                # тут я создаю список для каждого файла
                output_dict.setdefault(filename, [])
                # get all the qoutes in file
                all_quotes  = dictionary[filename]
                # limit for document
                qulim = doc_limof[qunum][0]
                # offset for document
                quset = doc_limof[qunum][1]
                for num, quote in enumerate (all_quotes):
                    if num == qulim + quset:
                        break;
                    if num >= quset and num < qulim + quset:
                         print(quset,'quset')
                         print(qulim + quset,'qulim + quset')
                         output_dict[filename].append(quote.highlight_window())
                         print("I got a quote!") 
                         print(quote,'quote!!!')
                qunum += 1         
        print(output_dict, 'output_dict')        
        return output_dict 
        
   
       









