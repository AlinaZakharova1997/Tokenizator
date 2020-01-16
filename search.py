
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
            # выделяем токены и зап-ем в список
            big_dict_files.append(self.get_dict(token.s))  
            
        files = set(big_dict_files[0])    
        for file_dict in big_dict_files[1:]:
            # пересечение названия файлов
            files = files.intersection(set(file_dict))
            
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
            # пересечение названий файлов
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
       @return: a dictionary filename:Context Windows генератор контекстных окон
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
        @return: dictionary with extended and reunated windows генератор окон!!!
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
                    # print(win_array[i].is_crossed(win_array[i+1]),'is crossed')
                    win_array[i].get_united_window(win_array[i+1])
                    # print('get_united')
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
                    # print(win_array[i].is_crossed(win_array[i+1]),'is crossed')
                    win_array[i].get_united_window(win_array[i+1])
                    # print('get_united')
                    win_array.remove(win_array[i+1])
                else:
                    i+=1
        
        return dictionary
    

    def get_context_gen(self, query, win_size, limit, offset):
        '''
        This function uses a generator of context windows
        to produce a dictionary with windows generator
        windows are extended and reunited
        @param query: string query
        @param win_size: size of a window
        @param limit: number of documents to return
        @param offset: from which document to start
        @return: dictionary with a generator of extended and reunated windows
        '''
        
        if not isinstance(query, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type! %s, %s' % (query, win_size))
        if not isinstance(limit, int) or not isinstance (offset, int):
            raise TypeError('Input has an unappropriate type!')
        
        # получаю словарь вида имя файла - генератор позиций
        position_gen_dict = self.get_dict_many_tokens_limit_offset_generator(query,limit,offset)
        # делаю словарь вида имя файла - генератор окон
        window_gen_dict = dict()
        for filename in position_gen_dict:
            window_gen_dict[filename] = self.context_generator(filename, position_gen_dict[filename],win_size)          
        # делаю словарь вида имя файла - генератор расширенных
        # и объединенных окон
        context_dict = dict()
        # print('i am here')
        for filename in window_gen_dict:
            # print('i am extending')
            context_dict[filename] = self.context_gen_uniter(window_gen_dict[filename])
            # print(context_dict[filename],'the result of extension')
        # это результат работы данной функции
        return context_dict
        
    def get_sentence_gen(self, query, win_size, limit, offset):
        '''
        This function uses a generator of sentences
        to produce a dictionary with sentence generator
        sentences are extended and reunited
        @param query: string query
        @param win_size: size of a window
        @param limit: number of documents to return
        @param offset: from which document to start
        @return: dictionary with a generator of extended and reunated sentences
        '''
        if not isinstance(query, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type! %s, %s' % (query, win_size))
        if not isinstance(limit, int) or not isinstance (offset, int):
            raise TypeError('Input has an unappropriate type!')

        # получаю словарь вида имя файла - генератор расширенных
        # и объединенных окон
        context_dict = self.get_context_gen(query, win_size, limit, offset)
        print(list(context_dict), 'context_dict')
        # создаю словарь вида имя файла - генератор предложений
        sentence_dict = dict()
        for filename in context_dict:
            sentence_dict[filename] = self.sentence_generator(context_dict[filename])
            print(list(sentence_dict[filename]),'sentence_dict[filename]')
        # создаю результурующий словарь с расширенными
        # и объединенными предложеиями
        final_sentence_dict = dict()
        for filename in sentence_dict:
            try:
                final_sentence_dict[filename] = self.sentence_generator_uniter(sentence_dict[filename])
                print(list(final_sentence_dict[filename]),'final!!!!')
            except StopIteration:
                break
        # это результат работы данной функции    
        return final_sentence_dict
    
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
        @return: dictionary {filename: [query(str)]} тут тоже генератор
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
    
    def qulim_search_modified_gen(self, query, win_size=1, limit=3, offset=0, doc_limof=[(3,0),(3,0),(3,0)]):
        """
        This function performs searching a query in database and returs
        a dictionary filemname:query in string format
        It uses generators to work faster than the previous function
        named qulim_search_modified
        @param query: query to search
        @param win_size: a size of a context window
        @param limit: max number of documents to show
        @param offset: document number to start with
        @param doc_limof: list of pairs that show limit and offset of each concrete document,
        no more quotes can be shown than this doclimit
        @return: dictionary {filename: [query(str)]} 
        """
        
        if not isinstance(query, str) or not isinstance(limit, int) or not isinstance(offset, int):
            raise TypeError('Input has an unappropriate type! %s, %s, %s' % (query, limit, offset))
        
        # dictionary for results
        output_dict = dict()
        # number of document
        qunum = 0
        # using brand new function with generator))
        dictionary = self.get_sentence_gen(query, win_size,limit,offset)
        for filename in sorted(dictionary):
            qulim = doc_limof[qunum][0]
            if not qulim:
                qulim = 3
            # print(qulim, 'qulim')
            # offset for document
            quset = doc_limof[qunum][1]
            if not quset:
                quset = 0
            # print(quset,'quset')
            output_dict.setdefault(filename, [])
            for item in range(quset):
                next(dictionary[item])
            for item in range(qulim):
                try:
                    output_dict[filename].append(next(dictionary[item]).highlight_window())
                    
                except StopIteration:
                    break

            qunum += 1                
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


    def context_generator(self, filename, position_generator, win_size):
        """
        This function creates context windows from a given
        file using the position generator
        @param filename: a name of a file
        @param position_generator: generator which generates positions
        @param win_size: a size of a future context window
        @return: contexts windows, i.e. objects of Context_Window class
        """
        if not isinstance(filename, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
        for pos in position_generator:
            window = Context_Window.get_window(filename, pos, win_size)
            yield window


    def context_gen_uniter(self, context_generator):
        """
        This function checks if generated windows intersect and unites them
        @param context_generator: generator of context windows
        @return: united context windows
        """
        # делаю из входных данных итератор, чтобы итераторить))
        iterator = context_generator.__iter__()
        # первое окно в итераторе, начало прохода
        previous = iterator.__next__()
        # print(previous,'previous')
        for window in context_generator:
            # заворачиваю в блок, чтобы избежать ошибки
            try:
                # второе окно после первого
                next_window = iterator.__next__()
                # print(next_window,'next_window')
                # проверяю на пересечение и если что - объединяю
                if previous.is_crossed(next_window):
                    previous.get_united_window(next_window)
                    # print('united window yielded') 
                else:
                    yield previous
                    # print(previous,'I just yield window')
                    previous = next_window        
            except StopIteration:
                break
                # print('I stop the iteration')
        yield previous       
            

    def sentence_generator(self, context_gen_uniter):
       """
       This function generates sentences using the context_gen_uniter
       @param context_gen_uniter: generator of united context windows
       @return: extended windows
       """
       for window in context_gen_uniter:
           window.extend_window()
           yield window


    def sentence_generator_uniter(self,sentence_generator):
       """
       This function checks if generated sentences intersect and unites them
       @param sentence_generator: generator of sentences
       @return: extended windows after thier union
       """ 
       iterator = sentence_generator.__iter__()
       previous = iterator.__next__()
       for extended_window in sentence_generator:
           print(extended_window,'extended_window')
           try:
               # если на вход было всего одно предложение, то в этом месте будет StopIteration?
               next_window = iterator.__next__()
               print(next_window,'next_window')
               if previous.is_crossed(next_window):
                   previous.get_united_window(next_window)
                   print(previous,'i united windows!')
               else:
                   yield previous
                   print(previous,'I could not unite so this is just a window')
                   previous = next_window   
           except StopIteration:
               break
               print('I stop the iteration')
       yield previous       
            

         
