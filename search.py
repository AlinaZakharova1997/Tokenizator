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
    
    def get_dict_many_tokens_limit_offset(self,tok_str, limit=3, offset=0):
        """
        This function performs searching for positions of given tokens
        @param tok_str: str containing tokens
        @param limit: number of files to be returned
        @param offset: from which file to start
        @return: dictionary, where a key is a filename
        and a value is a list of positions of all tokens     
        """

        if not isinstance(tok_str, str):
            raise TypeError('Input has an unappropriate type!')
        
        if not isinstance(limit, int) or not isinstance (offset, int):
            raise TypeError('Input has an unappropriate type!')
        
        if not tok_str:
            return {}
        
        # в случае, если оффсет отрицательный
        if offset < 0:
            offset = 0
            
        big_dict_files = []
        for token in self.tokenizator.token_gen(tok_str):
            big_dict_files.append(self.get_dict(token.s))#выделяем токены и зап-ем в список
            
        files = set(big_dict_files[0])    
        for file_dict in big_dict_files[1:]:
            files = files.intersection(set(file_dict)) #пересечение названия файлов
            
        # сортирую и отсекаю результаты по лимиту и оффсету    
        resulted_files = sorted(files)[offset: limit+offset]
        # создаю результурующий словарь
        output_dict = {}
        # записываю в него нужные результаты
        for filename in resulted_files:
            for token in self.tokenizator.token_gen(tok_str):
               output_dict.setdefault(filename,[]).extend(self.database[token.s][filename])
            # sort positions
            output_dict[filename].sort()
        return output_dict
    
    def get_dict_many_tokens_limit_offset_generator(self,tok_str, limit=3, offset=0):
        """
        This function performs searching for positions of given tokens
        @param tok_str: str containing tokens
        @param limit: number of files to be returned
        @param offset: from which file to start
        @return: dictionary, where a key is a filename
        and a value is a position generator    
        """

        if not isinstance(tok_str, str):
            raise TypeError('Input has an unappropriate type!')
        
        if not isinstance(limit, int) or not isinstance (offset, int):
            raise TypeError('Input has an unappropriate type!')
        
        if not tok_str:
            return {}
        
        # в случае, если оффсет отрицательный
        if offset < 0:
            offset = 0
            
        big_dict_files = []
        # словарь вида имя файла:список позиций 
        lists = {}
        for token in self.tokenizator.token_gen(tok_str):
            # ищу токен с строковом представлении
            found = self.get_dict(token.s)
            # добавляю в список
            big_dict_files.append(set(found))
            # заполняю словарь lists
            for file in found:
                lists.setdefault(file,[]).append(found[file])
            
        files = big_dict_files[0]    
        for file_dict in big_dict_files[1:]:
            #пересечение названий файлов
            files = files.intersection(set(file_dict)) 
            
        # сортирую и отсекаю результаты по лимиту и оффсету    
        resulted_files = sorted(files)[offset: limit+offset]
        # создаю результурующий словарь
        output_dict = {}
        # записываю в него нужные результаты
        for filename in resulted_files:
            for token in self.tokenizator.token_gen(tok_str):
               output_dict[filename] = self.position_generator(lists[filename]) 
        return output_dict
            
    def unite_all(self,dictionary,win_size):
       '''
       This function unites context windows
       @param dictionary: input dictionary filename:Positions
       @param win_size: a size of a context window
       @return: a dictionary filename:Context Windows
       '''
       if not isinstance(dictionary, dict):
            raise TypeError('Input has an unappropriate type!')      
       output_dict = {}
       
       # value is an array of positions
       for key,value in dictionary.items():
           # создаем список каждый раз, чтобы у каждого окна был свой список позиций  
           win_array = output_dict.setdefault(key, [])
           pos_array = value
           # print(pos_array,'pos_array')
           # for each position in values get window()
           for num, pos in enumerate(pos_array):
               # print(pos,'pos')
               # когда мы проходим по массиву и сравниваем элемент с предыдущим надо помнить, что мы начинаем с 0 элемента и если мы сравниваем его с -1,
               # то мы сравниваем с тем элементом, который в самом конце, а это нам не надо; еще может статься, что элемент будет сравниваться сам с собой, если он там один
               # то он будет удален так, как если бы он был дубликатом(по факту он дублирует сам себя) и по итогу имеем пустой массив и все плохо!!! вот так)))
               # поэтому проверяем if num > 0
               if num>0 and pos_array[num] == pos_array[num-1]:
                   # print('positions are equal!!!')
                   continue
               # print('positions are not equal!!')
               window = Context_Window.get_window(key, pos, win_size)
               win_array.append(window)
               # print(window,'window!!!')
               
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
            raise TypeError('Input has an unappropriate type! %s, %s' % (query, win_size))
        
        to_dict = self.get_dict_many_tokens(query)
        # print(to_dict,'to_dict')
        dictionary = self.unite_all(to_dict, win_size)
        # print(dictionary,'dictionary')
        for value in dictionary.values():
            # print(value,'value')
            for window in value:
                # если функция только модифицирует и ничего не возвращает
                # вызывай ее вот так и не путай! здесь я расширяю окно до границ предложения
                window.extend_window()
                # print(window,'extended window!!!')
        # print('I want to reunite')
        for key, win_array in dictionary.items():
            # print("I am in for")
            i = 0
            while i < len(win_array)-1:
                # print('I am in while')
                if win_array[i].is_crossed(win_array[i+1]):
                    #print(win_array[i].is_crossed(win_array[i+1]),'is crossed')
                    win_array[i].get_united_window(win_array[i+1])
                    #print('get_united')
                    win_array.remove(win_array[i+1])
                else:
                    i+=1
        
        return dictionary
        
        
    def unite_extended_limit_offset(self, query, win_size, limit=3, offset=0):
        '''
        This function unites extended windows in a dictionary(this dictionary
        contains only limited number of documents starting from offset)
        It takes query and win_size, makes a dictionary from query,
        than makes a new one but with windows as values,
        extends these windows and finally unites them once again
        @param query: string query
        @param win_size: size of a window
        @param limit: number of documents to return
        @param offset: from which document to start
        @return: dictionary with extended and reunated windows
        '''
        
        if not isinstance(query, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type! %s, %s' % (query, win_size))
        if not isinstance(limit, int) or not isinstance (offset, int):
            raise TypeError('Input has an unappropriate type!')
        
        # теперь я использую новую функцию поиска по нескольким токенам,
        # которая учитывает лимит и оффсет
        to_dict = self.get_dict_many_tokens_limit_offset(query,limit,offset)
        # print(to_dict,'to_dict')
        dictionary = self.unite_all(to_dict, win_size)
        # print(dictionary,'dictionary')
        for value in dictionary.values():
            # print(value,'value')
            for window in value:
                # если функция только модифицирует и ничего не возвращает
                # вызывай ее вот так и не путай! здесь я расширяю окно до границ предложения
                window.extend_window()
                # print(window,'extended window!!!')
        # print('I want to reunite')
        for key, win_array in dictionary.items():
            # print("I am in for")
            i = 0
            while i < len(win_array)-1:
                # print('I am in while')
                if win_array[i].is_crossed(win_array[i+1]):
                    #print(win_array[i].is_crossed(win_array[i+1]),'is crossed')
                    win_array[i].get_united_window(win_array[i+1])
                    #print('get_united')
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
            raise TypeError('Input has an unappropriate type! %s, %s' % (query, win_size))
        
        output_dict = {} 
        dictionary = self.unite_extended(query, win_size=1)
        # print(dictionary,'dictionary')
        for key, value in dictionary.items():
            # print(value,'value')
            for window in value:
                string = window.highlight_window()
                # print(string,'string')
                output_dict.setdefault(key, []).append(string)
        # print(output_dict,'dict')        
        return output_dict
    
    def query_search_modified(self, query, win_size=1, limit=3, offset=0):
        '''
        This function performs searching a query in database and returs
        a dictionary filemname:query in string format
        It uses a new search function named def unite_extended_limit_offset() and
        for that it takes limit and offset as it's arguments
        @param query: query to search
        @param win_size: a size of a context window
        @param limit: number of documents to return
        @param offset: from which document to start
        @return: dictionary {filename: [query(str)]}
        '''
        if not isinstance(query, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type! %s, %s' % (query, win_size))
        
        output_dict = {} 
        dictionary = self.unite_extended_limit_offset(query, win_size,limit, offset)
        # print(dictionary,'dictionary')
        for key, value in dictionary.items():
            # print(value,'value')
            for window in value:
                string = window.highlight_window()
                # print(string,'string')
                output_dict.setdefault(key, []).append(string)
        # print(output_dict,'dict')        
        return output_dict
    
    def qulim_search(self, query, win_size, limit, offset, doc_limof):
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
      
        if not isinstance(query, str) or not isinstance(limit, int) or not isinstance(offset, int):
            raise TypeError('Input has an unappropriate type! %s, %s, %s' % (query, limit, offset))
        
        # dictionary for results
        output_dict = dict()
        # number of document
        qunum = 0
        dictionary = self.unite_extended(query, win_size)
        # print(dictionary, 'dictionary')
        # print(doc_limof,'doc_limof')
        for number, filename in enumerate(sorted(dictionary)):
            #print('I am in for circle!')
            #print(filename,'filename')
            #print(number,'number')
            if number == limit + offset:
                break;
            if number >= offset and number < limit + offset:
                #print(number,'number again!!!')
                # тут я создаю список для каждого файла
                output_dict.setdefault(filename, [])
                # get all the qoutes in file
                all_quotes  = dictionary[filename]
                # print(all_quotes,'all_quotes')
                # limit for document
                qulim = doc_limof[qunum][0]
                # print(qulim, 'qulim')
                # offset for document
                quset = doc_limof[qunum][1]
                #print(quset,'quset')
                for num, quote in enumerate (all_quotes):
                    #print('I am in the second for circle!!!')
                    #print(num,'num!!!')
                    if num == qulim + quset:
                        break;
                    if num >= quset and num < qulim + quset:
                         #print(quset,'quset')
                         #print(qulim + quset,'qulim + quset')
                         output_dict[filename].append(quote.highlight_window())
                         #print("I got a quote!") 
                         # print(quote,'quote!!!')
                qunum += 1         
        # print(output_dict, 'output_dict')        
        return output_dict 
        
   
    def qulim_search_modified(self, query, win_size=1, limit=3, offset=0, doc_limof=[(3,0),(3,0),(3,0)]):
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
      
        if not isinstance(query, str) or not isinstance(limit, int) or not isinstance(offset, int):
            raise TypeError('Input has an unappropriate type! %s, %s, %s' % (query, limit, offset))
        
        # dictionary for results
        output_dict = dict()
        # number of document
        qunum = 0
        dictionary = self.unite_extended_limit_offset(query, win_size,limit,offset)
        # мне не нужно сравнивать с лимитами и офсетами по документам,
        # так как я уже использую новую функцию, где они уже учтены
        # поэтому я просто перебираю файлы в отсортированном словаре
        for filename in sorted(dictionary):
            # тут я создаю список для каждого файла
            output_dict.setdefault(filename, [])
            # достаю все limit цитат из словаря по данному файлу
            all_quotes  = dictionary[filename]
            # print(all_quotes,'all_quotes')
            # limit for document
            qulim = doc_limof[qunum][0]
            if not qulim:
                qulim = 3
            # print(qulim, 'qulim')
            # offset for document
            quset = doc_limof[qunum][1]
            if not quset:
                quset = 0
            #print(quset,'quset')
            for num, quote in enumerate (all_quotes):
                #print('I am in the second for circle!!!')
                #print(num,'num!!!')
                if num == qulim + quset:
                    break
                if num >= quset and num < qulim + quset:
                    #print(quset,'quset')
                    #print(qulim + quset,'qulim + quset')
                    output_dict[filename].append(quote.highlight_window())
                    #print("I got a quote!") 
                    # print(quote,'quote!!!')
            qunum += 1         
        # print(output_dict, 'output_dict')        
        return output_dict 
           

    def position_generator(self, lists):
        '''
        This function generates positions
        @param lists: list of lists of positions
        It chooses a position with a min frequency upon firsts elements of each list given and yeilds it
        '''
        # превращаю списки в итераторы. итератор - генератор, осуществляющий итерацию.    
        iters = [iter(x) for x in  lists]
        # список с первыми элементами списков
        firsts = [next(it) for it in iters]
        # print(firsts,'firsts')
        while firsts:
            position_iter = min(firsts)
            yield position_iter
            # print(position_iter,'position_iter')
            # номер массива, из которого я взяла этот элемент
            position_iter_pos = firsts.index(position_iter)
            try:
                # переходим к следующему элементу в этом списке
                firsts[position_iter_pos] = next(iters[position_iter_pos]) 
            except StopIteration:
                # если один из списков закончился, то удаляем и возвращаем удаленный элемент
                # те первый элемент такого списка и его итератор нам больше не нужны и мы их удаляем
                iters.pop(position_iter_pos)
                firsts.pop(position_iter_pos)

   
