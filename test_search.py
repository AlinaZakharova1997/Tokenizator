import unittest
import search
from search import SearchEngine
import os
import shelve
import indexer
from indexer import Indexer, Position_Plus
from windows import Context_Window
from collections.abc import Generator

class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
        self.indexator = Indexer('database')

    def tearDown(self):
        if hasattr(self, 'search'):
            del self.search
        # for current directory use '.'
        file_list = os.listdir(path=".")
        for i in file_list:
            if i == 'database':
                database_exists = True
                os.remove(i)
            elif i.startswith('database.'):
                database_exists= True
                os.remove(i)    

    def test_MyError_give_dict_inp(self):
        del self.indexator
        self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
            self.search.get_dict(12)
            
    def test_get_dict(self):
        test_file = open('test_search_one.txt', 'w') 
        test_file.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict('Alina')
        cool_result = {'test_search_one.txt': [Position_Plus(0,14,19)]}
        self.assertEqual(result, cool_result)
        os.remove('test_search_one.txt')
        
    def test_dict_no_such_token(self):
        test_file = open('test_search_one.txt', 'w') 
        test_file.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict('Laptop')
        os.remove('test_search_one.txt')

    def test_MyError_dive_dict_many_tokens_inp(self):
        del self.indexator
        self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
            self.search.get_dict_many_tokens(12)

    def test_get_dict_many_tokens(self):
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file_one.close()
        test_file_two = open('test_search_two.txt', 'w') 
        test_file_two.write(' Ф 12 !!! @ # Alina loves apples)))')
        test_file_two.close()
        test_file_three = open('test_search_three.txt', 'w') 
        test_file_three.write(' Ф 12 !!! @ # Alina student)))')
        test_file_three.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        self.indexator.get_index_with_line('test_search_two.txt')
        self.indexator.get_index_with_line('test_search_three.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict_many_tokens('Alina is a student')
        cool_result = {'test_search_one.txt': [Position_Plus(0,14,19),Position_Plus(0,20,22),
                                               Position_Plus(0,23,24),Position_Plus(0,25,32)]}
        self.assertEqual(result, cool_result)
        os.remove('test_search_one.txt')
        os.remove('test_search_two.txt')
        os.remove('test_search_three.txt')

    def test_dict_no_tokens_found(self):
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file_one.close()
        test_file_two = open('test_search_two.txt', 'w') 
        test_file_two.write(' Ф 12 !!! @ # Alina loves apples)))')
        test_file_two.close()
        test_file_three = open('test_search_three.txt', 'w') 
        test_file_three.write(' Ф 12 !!! @ # Alina student)))')
        test_file_three.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        self.indexator.get_index_with_line('test_search_two.txt')
        self.indexator.get_index_with_line('test_search_three.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict('Find my laptop Alina')
        os.remove('test_search_one.txt')
        os.remove('test_search_two.txt')
        os.remove('test_search_three.txt')
        
    def test_dict_many_files(self):
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file_one.close()
        test_file_two = open('test_search_two.txt', 'w') 
        test_file_two.write(' Ф 12 !!! @ # Alina loves apples)))')
        test_file_two.close()
        test_file_three = open('test_search_three.txt', 'w') 
        test_file_three.write(' Ф 12 !!! @ # Alina student)))')
        test_file_three.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        self.indexator.get_index_with_line('test_search_two.txt')
        self.indexator.get_index_with_line('test_search_three.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict_many_tokens('Alina student')
        cool_result = {'test_search_one.txt': [Position_Plus(0,14,19),Position_Plus(0,25,32)],
                       'test_search_three.txt':[Position_Plus(0,14,19),Position_Plus(0,20,27)]}
        self.assertEqual(result, cool_result)
        os.remove('test_search_one.txt')
        os.remove('test_search_two.txt')
        os.remove('test_search_three.txt')
   
    def test_dict_many_files_limit_offset_one(self):
        test_file_one = open('test_search_1.txt', 'w') 
        test_file_one.write(' Ф 12 !!! @ # Alina Zakharova is a student)))')
        test_file_one.close()
        test_file_two = open('test_search_2.txt', 'w') 
        test_file_two.write('Alina Zakharova loves big and red apples)))')
        test_file_two.close()
        test_file_three = open('test_search_3.txt', 'w') 
        test_file_three.write('Little Alina Zakharova is a student)))')
        test_file_three.close()
        self.indexator.get_index_with_line('test_search_1.txt')
        self.indexator.get_index_with_line('test_search_2.txt')
        self.indexator.get_index_with_line('test_search_3.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict_many_tokens_limit_offset('Alina Zakharova', limit=3, offset=0)
        cool_result = {'test_search_1.txt': [Position_Plus(0,14,19), Position_Plus(0,20,29)],
                       'test_search_2.txt':[Position_Plus(0,0,5),Position_Plus(0,6,15)],
                       'test_search_3.txt':[Position_Plus(0,7,12),Position_Plus(0,13,22)]}
        self.assertEqual(result, cool_result)
        os.remove('test_search_1.txt')
        os.remove('test_search_2.txt')
        os.remove('test_search_3.txt')
        
    def test_dict_many_files_limit_offset_two(self):
        test_file_one = open('test_search_1.txt', 'w') 
        test_file_one.write(' Ф 12 !!! @ # Alina Zakharova is a student)))')
        test_file_one.close()
        test_file_two = open('test_search_2.txt', 'w') 
        test_file_two.write('Alina Zakharova loves big and red apples)))')
        test_file_two.close()
        test_file_three = open('test_search_3.txt', 'w') 
        test_file_three.write('Little Alina Zakharova is a student)))')
        test_file_three.close()
        self.indexator.get_index_with_line('test_search_1.txt')
        self.indexator.get_index_with_line('test_search_2.txt')
        self.indexator.get_index_with_line('test_search_3.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict_many_tokens_limit_offset('Alina Zakharova', limit=2, offset=0)
        cool_result = {'test_search_1.txt': [Position_Plus(0,14,19), Position_Plus(0,20,29)],
                       'test_search_2.txt':[Position_Plus(0,0,5),Position_Plus(0,6,15)]}
        self.assertEqual(result, cool_result)
        os.remove('test_search_1.txt')
        os.remove('test_search_2.txt')
        os.remove('test_search_3.txt')
        
    def test_position_generator(self):
        lists = [[Position_Plus(0,1,5),Position_Plus(20,4,5),Position_Plus(30,0,6)],
                 [Position_Plus(10,4,9),Position_Plus(10,9,15)]]
        del self.indexator
        self.search = SearchEngine('database')
        result = list(self.search.position_generator(lists))
        fine_result = [Position_Plus(0,1,5),Position_Plus(10,4,9),Position_Plus(10,9,15),
                       Position_Plus(20,4,5),Position_Plus(30,0,6)]
        self.assertEqual(result, fine_result)        

    def test_isgenerator(self):
        lists = [[Position_Plus(0,1,5),Position_Plus(20,4,5),Position_Plus(30,0,6)],
                 [Position_Plus(10,4,9),Position_Plus(10,9,15)]]
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.position_generator(lists)
        self.assertIsInstance(result, Generator)

        
    def test_input_generator_error(self):
        del self.indexator
        self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
            self.search.position_generator(1997, "acb",'12')
     
    def test_context_generator(self):
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        positions = [Position_Plus(0,0,5),Position_Plus(0,16,18)]
        result = list(self.search.context_generator('test_window_one.txt',positions,1))
        cool_result = [Context_Window('Alina Zakharova is a student)))',[Position_Plus(0,0,5)],0,15),
                       Context_Window('Alina Zakharova is a student)))',[Position_Plus(0,16,18)],6,20)]
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')
        
    def test_context_generator_wrong_input(self):
        del self.indexator
        self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
            self.search.context_generator(1997, '12')
            
    def test_context_gen_uniter_one(self):
        del self.indexator
        self.search = SearchEngine('database')
        generated_input = [
                       Context_Window('Alina Zakharova is a student.',[Position_Plus(0,0,5)],0,15),
                       Context_Window('Alina Zakharova is a student.',[Position_Plus(0,16,18)],6,20),
                       Context_Window('Live fast, die young.',[Position_Plus(1,0,4)],0,8),
                       Context_Window('Live fast, die young.',[Position_Plus(1,15,20)],11,20)]
        result = list(self.search.context_gen_uniter(generated_input))
        cool_result = [Context_Window('Alina Zakharova is a student.',[Position_Plus(0,0,5),Position_Plus(0,16,18)],0,20),
                       Context_Window('Live fast, die young.',[Position_Plus(1,0,4)],0,8),
                       Context_Window('Live fast, die young.',[Position_Plus(1,15,20)],11,20)]
        self.assertEqual(result, cool_result)
        
    def test_context_gen_uniter_two(self):
        del self.indexator
        self.search = SearchEngine('database')
        generated_input = [
                       Context_Window('Live fast, die young.',[Position_Plus(0,0,4)],0,8),
                       Context_Window('Live fast, die young.',[Position_Plus(0,15,20)],11,20),
                       Context_Window('Alina Zakharova is a student.',[Position_Plus(1,0,5)],0,15),
                       Context_Window('Alina Zakharova is a student.',[Position_Plus(1,16,18)],6,20)]
        result = list(self.search.context_gen_uniter(generated_input))
        cool_result = [
                       Context_Window('Live fast, die young.',[Position_Plus(0,0,4)],0,8),
                       Context_Window('Live fast, die young.',[Position_Plus(0,15,20)],11,20),
                       Context_Window('Alina Zakharova is a student.',[Position_Plus(1,0,5),Position_Plus(1,16,18)],0,20)]
        self.assertEqual(result, cool_result)    

    """def test_sentence_generator(self):
        del self.indexator
        self.search = SearchEngine('database')
        generated_input = [Context_Window('Alina Zakharova is a student)))',[Position_Plus(0,0,5),Position_Plus(0,16,18)],0,20),
                       Context_Window('Live fast, die young',[Position_Plus(1,0,4)],0,8)]
        result = list(self.search.sentence_generator(generated_input))
        cool_result = [Context_Window('Alina Zakharova is a student.',[Position_Plus(0,0,5),Position_Plus(0,16,18)],0,29),
                       Context_Window('Live fast, die young.',[Position_Plus(1,0,4)],0,21)]
        self.assertEqual(result, cool_result)"""
        
    def test_dict_many_files_limit_generator(self):
        test_file_one = open('test_search_1.txt', 'w') 
        test_file_one.write(' Ф 12 !!! @ # Alina Zakharova is a student)))')
        test_file_one.close()
        test_file_two = open('test_search_2.txt', 'w') 
        test_file_two.write('Alina Zakharova loves big and red apples)))')
        test_file_two.close()
        test_file_three = open('test_search_3.txt', 'w') 
        test_file_three.write('Little Alina Zakharova is a student)))')
        test_file_three.close()
        self.indexator.get_index_with_line('test_search_1.txt')
        self.indexator.get_index_with_line('test_search_2.txt')
        self.indexator.get_index_with_line('test_search_3.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict_many_tokens_limit_offset_generator('Alina Zakharova', limit=2, offset=0)
        cool_result = {'test_search_1.txt': [Position_Plus(0,14,19), Position_Plus(0,20,29)],
                       'test_search_2.txt':[Position_Plus(0,0,5),Position_Plus(0,6,15)]}
        for res in result:
            self.assertEqual(list(result[res]), cool_result[res])
        os.remove('test_search_1.txt')
        os.remove('test_search_2.txt')
        os.remove('test_search_3.txt')     

    def test_emptiness(self):
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write('')
        test_file_one.close()
        del self.indexator
        os.remove('test_search_one.txt')
    
    def test_TypeError_unite_all(self):
        del self.indexator
        self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
             self.search.unite_all(12, 'window)))')

    def test_unite_all_one(self):
        test_file = open('test_unite_all.txt', 'w') 
        test_file.write('Alina Zakharova is a student')
        test_file.close()
        self.indexator.get_index_with_line('test_unite_all.txt')
        del self.indexator
        self.search = SearchEngine('database')
        dictionary = self.search.get_dict_many_tokens('Alina Zakharova is a student')
        input_dictionary = {'test_unite_all.txt':[Position_Plus(0, 0, 5),Position_Plus(0, 6, 15),
                                                  Position_Plus(0, 16, 18),Position_Plus(0, 19, 20),
                                                  Position_Plus(0, 21, 28)]}
        self.assertEqual(dictionary, input_dictionary)
        dict_to_function =  self.search.unite_all(dictionary, 1)
        output_dict = {'test_unite_all.txt':[Context_Window('Alina Zakharova is a student',[Position_Plus(0, 0, 5), Position_Plus(0, 6, 15),
                                                                                            Position_Plus(0, 16, 18), Position_Plus(0, 19, 20),
                                                                                            Position_Plus(0, 21, 28)], 0, 28)]}
                                            
        self.assertEqual(dict_to_function,output_dict)
        os.remove('test_unite_all.txt')
        
    def test_unite_all(self):
        test_file = open('test_unite_all.txt', 'w') 
        test_file.write('Alina Zakharova is a student')
        test_file.close()
        test_file_one = open('test_unite_all_one.txt', 'w') 
        test_file_one.write('Little Zakharova loves big apples')
        test_file_one.close()
        self.indexator.get_index_with_line('test_unite_all.txt')
        self.indexator.get_index_with_line('test_unite_all_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        dictionary = {'test_unite_all.txt':[Position_Plus(0, 0, 5),Position_Plus(0, 6, 15),
                                                  Position_Plus(0, 16, 18),Position_Plus(0, 19, 20),
                                                  Position_Plus(0, 21, 28)],
                      'test_unite_all_one.txt':[Position_Plus(0, 0, 6),Position_Plus(0, 7, 16),
                                                Position_Plus(0, 17, 22), Position_Plus(0, 23, 26),
                                                Position_Plus(0, 27, 33)]}
        dict_to_function = self.search.unite_all(dictionary, 1)
        output_dict = {'test_unite_all.txt':[Context_Window('Alina Zakharova is a student',[Position_Plus(0, 0, 5), Position_Plus(0, 6, 15),
                                                                                            Position_Plus(0, 16, 18), Position_Plus(0, 19, 20),
                                                                                            Position_Plus(0, 21, 28)], 0, 28)],
                       'test_unite_all_one.txt':[Context_Window('Little Zakharova loves big apples',[Position_Plus(0, 0, 6),Position_Plus(0, 7, 16),
                                                                                                     Position_Plus(0, 17, 22), Position_Plus(0, 23, 26),
                                                                                                     Position_Plus(0, 27, 33)], 0, 33)]}
                                            
        self.assertEqual(dict_to_function, output_dict)
        os.remove('test_unite_all.txt')
        os.remove('test_unite_all_one.txt')

    def test_unite(self):
        test_file = open('test_unite.txt', 'w') 
        test_file.write('Alina Zakharova is a student')
        test_file.close()
        self.indexator.get_index_with_line('test_unite.txt')
        del self.indexator
        self.search = SearchEngine('database')
        dictionary = {'test_unite.txt':[Position_Plus(0, 0, 5),Position_Plus(0, 6, 15),
                                            Position_Plus(0, 21, 28)]}
        dict_to_function =  self.search.unite_all(dictionary, 1)
        output_dict = {'test_unite.txt':[Context_Window('Alina Zakharova is a student',[Position_Plus(0, 0, 5), Position_Plus(0, 6, 15)], 0, 18),
                                         Context_Window('Alina Zakharova is a student',[Position_Plus(0, 21, 28)], 19, 28)]}             
        self.assertEqual(dict_to_function, output_dict)
        os.remove('test_unite.txt')
        
   
    def test_TypeError_unite_extended(self):
        del self.indexator
        self.search = SearchEngine('database')
        s = [1,2,3]
        with self.assertRaises(TypeError):
            self.search.unite_extended('window)))', s)

    def test_unite_extended_all_words(self):
        test_file_one = open('test_unite_extended.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student!!')
        test_file_one.close()
        self.indexator.get_index_with_line('test_unite_extended.txt')
        del self.indexator
        self.search = SearchEngine('database')
        query = 'Alina Zakharova is a student!!'
        result = self.search.unite_extended(query, 1)
        fine_result = {'test_unite_extended.txt':[Context_Window('Alina Zakharova is a student!!',[Position_Plus(0, 0, 5), Position_Plus(0, 6, 15),
                                                                                            Position_Plus(0, 16, 18), Position_Plus(0, 19, 20),
                                                                                            Position_Plus(0, 21, 28)], 0, 30)]}
        self.assertEqual(result, fine_result)
        os.remove('test_unite_extended.txt')
        
    def test_unite_extended(self):
        test_file_one = open('test_unite_extended.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student!! Smart Student Alina Zakharova tries to write programs.')
        test_file_one.close()
        self.indexator.get_index_with_line('test_unite_extended.txt')
        del self.indexator      
        self.search = SearchEngine('database')
        query = 'Alina Zakharova'
        result = self.search.unite_extended(query, 1)
        fine_result = {'test_unite_extended.txt':[Context_Window('Alina Zakharova is a student!! Smart Student Alina Zakharova tries to write programs.',[Position_Plus(0, 0, 5), Position_Plus(0, 6, 15)], 0, 30),
                                                  Context_Window('Alina Zakharova is a student!! Smart Student Alina Zakharova tries to write programs.',[Position_Plus(0,45,50),Position_Plus(0,51,60)], 31, 85)]}
        self.assertEqual(result, fine_result)
        os.remove('test_unite_extended.txt')
        
    def test_unite_extended_limit_offset(self):
        test_file_one = open('test_unite_extended.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student!! Smart Student Alina Zakharova tries to write programs.')
        test_file_one.close()
        self.indexator.get_index_with_line('test_unite_extended.txt')
        del self.indexator      
        self.search = SearchEngine('database')
        query = 'Alina Zakharova'
        result = self.search.unite_extended_limit_offset(query, win_size=1, limit=2, offset=0)
        fine_result = {'test_unite_extended.txt':[Context_Window('Alina Zakharova is a student!! Smart Student Alina Zakharova tries to write programs.',[Position_Plus(0, 0, 5), Position_Plus(0, 6, 15)], 0, 30),
                                                  Context_Window('Alina Zakharova is a student!! Smart Student Alina Zakharova tries to write programs.',[Position_Plus(0,45,50),Position_Plus(0,51,60)], 31, 85)]}
        self.assertEqual(result, fine_result)
        os.remove('test_unite_extended.txt')
            
    def test_unite_extended_two_files(self):
        test_file_one = open('test_unite_extended.txt', 'w') 
        test_file_one.write('Smart Student Alina Zakharova tries to write programs.')
        test_file_one.close()
        test_file_two = open('test_unite_extended_two.txt', 'w') 
        test_file_two.write('Alina Zakharova is a student!!')
        test_file_two.close()
        self.indexator.get_index_with_line('test_unite_extended.txt')
        self.indexator.get_index_with_line('test_unite_extended_two.txt')
        del self.indexator      
        self.search = SearchEngine('database')
        query = 'Zakharova'
        result = self.search.unite_extended(query, 1)
        fine_result = {'test_unite_extended.txt':[Context_Window('Smart Student Alina Zakharova tries to write programs.',[Position_Plus(0,20,29)], 0, 54)],
                       'test_unite_extended_two.txt':[Context_Window('Alina Zakharova is a student!!',[Position_Plus(0,6,15)], 0, 30)]}
        self.assertEqual(result, fine_result)
        os.remove('test_unite_extended.txt')
        os.remove('test_unite_extended_two.txt')
        
    def test_unite_extended_limit_offset_two_files(self):
        test_file_one = open('test_unite_extended_1.txt', 'w') 
        test_file_one.write('Smart Student Alina Zakharova tries to write programs.')
        test_file_one.close()
        test_file_two = open('test_unite_extended_2.txt', 'w') 
        test_file_two.write('Alina Zakharova is a student!!')
        test_file_two.close()
        test_file_three = open('test_unite_extended_3.txt', 'w') 
        test_file_three.write('Alina Zakharova loves rock music')
        test_file_three.close()
        self.indexator.get_index_with_line('test_unite_extended_1.txt')
        self.indexator.get_index_with_line('test_unite_extended_2.txt')
        self.indexator.get_index_with_line('test_unite_extended_3.txt')
        del self.indexator      
        self.search = SearchEngine('database')
        query = 'Zakharova'
        result = self.search.unite_extended_limit_offset(query, win_size=1,limit=2,offset=0)
        fine_result = {'test_unite_extended_1.txt':[Context_Window('Smart Student Alina Zakharova tries to write programs.',[Position_Plus(0,20,29)], 0, 54)],
                       'test_unite_extended_2.txt':[Context_Window('Alina Zakharova is a student!!',[Position_Plus(0,6,15)], 0, 30)]}
        self.assertEqual(result, fine_result)
        os.remove('test_unite_extended_1.txt')
        os.remove('test_unite_extended_2.txt')
        os.remove('test_unite_extended_3.txt')
           
  
    def test_query_search(self):
       test_file_one = open('test_query_search.txt', 'w') 
       test_file_one.write('Alina Zakharova is a student!! Smart Student Alina Zakharova tries to write programs.')
       test_file_one.close()
       self.indexator.get_index_with_line('test_query_search.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Alina Zakharova'
       result = self.search.query_search(query, 1)
       fine_result = {'test_query_search.txt':['<b>Alina</b> <b>Zakharova</b> is a student!!',
                                               'Smart Student <b>Alina</b> <b>Zakharova</b> tries to write programs.']}
       self.assertEqual(result, fine_result)
       os.remove('test_query_search.txt')

    def test_query_two_files(self):
       test_file_one = open('test_query_search_one.txt', 'w') 
       test_file_one.write('Alina Zakharova is a student!!')
       test_file_one.close()
       test_file_two = open('test_query_search_two.txt', 'w') 
       test_file_two.write('Little Zakharova loves big apples.')
       test_file_two.close()
       self.indexator.get_index_with_line('test_query_search_one.txt')
       self.indexator.get_index_with_line('test_query_search_two.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.query_search(query, 1)
       fine_result = {'test_query_search_one.txt':['Alina <b>Zakharova</b> is a student!!'],
                      'test_query_search_two.txt':['Little <b>Zakharova</b> loves big apples.']}
       self.assertEqual(result, fine_result)
       os.remove('test_query_search_one.txt')
       os.remove('test_query_search_two.txt')
       
    def test_query_search_modified(self):
       test_file_one = open('test_query_search_one.txt', 'w') 
       test_file_one.write('Alina Zakharova is a student!!')
       test_file_one.close()
       test_file_two = open('test_query_search_two.txt', 'w') 
       test_file_two.write('Little Zakharova loves big apples.')
       test_file_two.close()
       self.indexator.get_index_with_line('test_query_search_one.txt')
       self.indexator.get_index_with_line('test_query_search_two.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.query_search_modified(query, win_size=1, limit=3, offset=0)
       fine_result = {'test_query_search_one.txt':['Alina <b>Zakharova</b> is a student!!'],
                      'test_query_search_two.txt':['Little <b>Zakharova</b> loves big apples.']}
       self.assertEqual(result, fine_result)
       os.remove('test_query_search_one.txt')
       os.remove('test_query_search_two.txt')        
       
    def test_qulim_search(self):
       test_file_one = open('test_qulim_search_one.txt', 'w') 
       test_file_one.write('Alina Zakharova is a student!! We are gonna rock, we are gonna rock around the clock tonight. Smart Student Alina Zakharova tries to write programs. Python is easy, Zakharova, keep calm caaalm!!!')
       test_file_one.close()
       test_file_two = open('test_qulim_search_two.txt', 'w') 
       test_file_two.write('Little Zakharova loves big apples. Also student Alina Zakharova loves rock music.')
       test_file_two.close()
       self.indexator.get_index_with_line('test_qulim_search_one.txt')
       self.indexator.get_index_with_line('test_qulim_search_two.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.qulim_search(query, win_size=1, limit=2, offset=0, doc_limof =[(3,1), (3,1)] )
       fine_result = {'test_qulim_search_one.txt':['Smart Student Alina <b>Zakharova</b> tries to write programs.',
                                                   'Python is easy, <b>Zakharova</b>, keep calm caaalm!!!'],
                      'test_qulim_search_two.txt':['Also student Alina <b>Zakharova</b> loves rock music.']}
       self.assertEqual(result, fine_result)
       os.remove('test_qulim_search_one.txt')
       os.remove('test_qulim_search_two.txt')

       
    def test_qulim_search_one(self):
       test_file_one = open('test_qulim_search_one.txt', 'w') 
       test_file_one.write('Smart Student Alina Zakharova is a linguist!! We are gonna rock, we are gonna rock around the clock tonight. Smart Student Alina Zakharova tries to write programs. Python is easy, Zakharova, keep calm caaalm!!!')
       test_file_one.close()
       test_file_two = open('test_qulim_search_two.txt', 'w') 
       test_file_two.write('Little Zakharova loves big apples. Also student Alina Zakharova loves rock music.')
       test_file_two.close()
       self.indexator.get_index_with_line('test_qulim_search_one.txt')
       self.indexator.get_index_with_line('test_qulim_search_two.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.qulim_search(query, win_size=1, limit=2, offset=0, doc_limof =[(2,0), (3,3)] )
       fine_result = {'test_qulim_search_one.txt':['Smart Student Alina <b>Zakharova</b> is a linguist!!',
                                                   'Smart Student Alina <b>Zakharova</b> tries to write programs.'],
                      'test_qulim_search_two.txt': []}
       self.assertEqual(result, fine_result)
       os.remove('test_qulim_search_one.txt')
       os.remove('test_qulim_search_two.txt')


    def test_qulim_search_two(self):
       test_file_one = open('test_qulim_search_1.txt', 'w') 
       test_file_one.write('Smart Student Alina Zakharova is a linguist!! We are gonna rock, we are gonna rock around the clock tonight. Smart Student Alina Zakharova tries to write programs. Python is easy, Zakharova, keep calm caaalm!!!')
       test_file_one.close()
       test_file_two = open('test_qulim_search_2.txt', 'w') 
       test_file_two.write('Little Alina Zakharova loves big apples. Also student Alina Zakharova loves rock music.')
       test_file_two.close()
       test_file_three = open('test_qulim_search_3.txt', 'w') 
       test_file_three.write('Beautiful Alina Zakharova loves sweets and black coffee. Also cute Alina Zakharova loves Disney cartoons.')
       test_file_three.close()
       self.indexator.get_index_with_line('test_qulim_search_1.txt')
       self.indexator.get_index_with_line('test_qulim_search_2.txt')
       self.indexator.get_index_with_line('test_qulim_search_3.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.qulim_search(query, win_size=1, limit=2, offset=1, doc_limof =[(2,0), (2,0)] )
       fine_result = {
                      'test_qulim_search_2.txt': ['Little Alina <b>Zakharova</b> loves big apples.',
                                                    'Also student Alina <b>Zakharova</b> loves rock music.'],
                      'test_qulim_search_3.txt':['Beautiful Alina <b>Zakharova</b> loves sweets and black coffee.',
                                                     'Also cute Alina <b>Zakharova</b> loves Disney cartoons.']}
       self.assertEqual(result, fine_result)
       os.remove('test_qulim_search_1.txt')
       os.remove('test_qulim_search_2.txt')
       os.remove('test_qulim_search_3.txt')
       
    def test_qulim_search_three(self):
        test_file_one = open('test_qulim_search_1.txt', 'w') 
        test_file_one.write('Smart Student Alina Zakharova is a linguist!! Smart Student Alina Zakharova tries to write programs. Python is easy, Zakharova, keep calm caaalm!!!')
        test_file_one.close()
        test_file_two = open('test_qulim_search_2.txt', 'w') 
        test_file_two.write('Little funny girl Alina loves big apples. Also extra smart student Alina Zakharova loves rock music.')
        test_file_two.close()
        test_file_three = open('test_qulim_search_3.txt', 'w') 
        test_file_three.write('Beautiful and perfect Alina Zakharova loves sweets and black coffee. Also cute and nice Alina Zakharova loves Disney cartoons.')
        test_file_three.close()
        self.indexator.get_index_with_line('test_qulim_search_1.txt')
        self.indexator.get_index_with_line('test_qulim_search_2.txt')
        self.indexator.get_index_with_line('test_qulim_search_3.txt')
        del self.indexator

        self.search = SearchEngine('database')
        query = 'Alina Zakharova'
        result = self.search.qulim_search(query, win_size=1, limit=2, offset=1, doc_limof =[(2,0), (1,0)] )
        fine_result = {
                      'test_qulim_search_2.txt': ['Little funny girl <b>Alina</b> loves big apples.',
                                                    'Also extra smart student <b>Alina</b> <b>Zakharova</b> loves rock music.'],
                      'test_qulim_search_3.txt':['Beautiful and perfect <b>Alina</b> <b>Zakharova</b> loves sweets and black coffee.']}
        self.assertEqual(result, fine_result)
        os.remove('test_qulim_search_1.txt')
        os.remove('test_qulim_search_2.txt')
        os.remove('test_qulim_search_3.txt')
        
    def test_qulim_search_four(self):
        test_file_one = open('test_qulim_search_1.txt', 'w') 
        test_file_one.write('Умная ученица Алина Захарова - лингвист !! Умная ученица Алина Захарова пытается писать программы. Питон - это просто, Захарова, сохраняй спокойствие!')
        test_file_one.close()
        test_file_two = open('test_qulim_search_2.txt', 'w') 
        test_file_two.write('Маленькая смешная девочка Алина любит большие яблоки. Также очень умная ученица Алина Захарова любит рок-музыку.')
        test_file_two.close()
        test_file_three = open('test_qulim_search_3.txt', 'w') 
        test_file_three.write('Прекрасная и идеальная Алина Захарова любит сладости и черный кофе. Также милая и милая Алина Захарова любит мультфильмы Диснея.')
        test_file_three.close()
        self.indexator.get_index_with_line('test_qulim_search_1.txt')
        self.indexator.get_index_with_line('test_qulim_search_2.txt')
        self.indexator.get_index_with_line('test_qulim_search_3.txt')
        del self.indexator

        self.search = SearchEngine('database')
        query = 'Алина Захарова'
        result = self.search.qulim_search(query, win_size=1, limit=2, offset=1, doc_limof =[(2,0), (1,0)] )
        fine_result = {
                      'test_qulim_search_2.txt': ['Маленькая смешная девочка <b>Алина</b> любит большие яблоки.',
                                                    'Также очень умная ученица <b>Алина</b> <b>Захарова</b> любит рок-музыку.'],
                      'test_qulim_search_3.txt':['Прекрасная и идеальная <b>Алина</b> <b>Захарова</b> любит сладости и черный кофе.']}
        self.assertEqual(result, fine_result)
        os.remove('test_qulim_search_1.txt')
        os.remove('test_qulim_search_2.txt')
        os.remove('test_qulim_search_3.txt')
        
    def test_qulim_search_five(self):
     
        test_file_two = open('test_qulim_search_1.txt', 'w') 
        test_file_two.write('Узнав, что Безухов в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне. Вилларский скучал в Орле и был счастлив, встретив человека одного с собой круга и с одинаковыми, как он полагал, интересами. Умный и смелый Пьер хочет быть декабристом.')
        test_file_two.close()
        test_file_three = open('test_qulim_search_2.txt', 'w') 
        test_file_three.write('Кому, в особенности ему, какое дело было до того, что узнают или не узнают, что имя их пленного было граф Безухов? Узнав, что Безухов в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне. В числе отбитых Денисовым и Долоховым русских пленных был Пьер Безухов.' )
        test_file_three.close()
        self.indexator.get_index_with_line('test_qulim_search_1.txt')
        self.indexator.get_index_with_line('test_qulim_search_2.txt')
        del self.indexator
        self.search = SearchEngine('database')
        query = 'Пьер Безухов'
        result = self.search.qulim_search(query, win_size=1, limit=2, offset=0, doc_limof =[(1,0), (2,0)] )
        fine_result = {'test_qulim_search_1.txt': ['Узнав, что <b>Безухов</b> в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне.'],
                      'test_qulim_search_2.txt':['Кому, в особенности ему, какое дело было до того, что узнают или не узнают, что имя их пленного было граф <b>Безухов</b>? Узнав, что <b>Безухов</b> в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне.',
                                                 'В числе отбитых Денисовым и Долоховым русских пленных был <b>Пьер</b> <b>Безухов</b>.']}
        self.assertEqual(result, fine_result)
        os.remove('test_qulim_search_1.txt')
        os.remove('test_qulim_search_2.txt')
        
    def test_qulim_search_six(self):
     
        test_file_two = open('test_qulim_search_1.txt', 'w') 
        test_file_two.write('Узнав, что Безухов в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне. Вилларский скучал в Орле и был счастлив, встретив человека одного с собой круга и с одинаковыми, как он полагал, интересами. Умный и смелый Пьер хочет быть декабристом.')
        test_file_two.close()
        test_file_three = open('test_qulim_search_2.txt', 'w') 
        test_file_three.write('Кому, в особенности ему, какое дело было до того, что узнают или не узнают, что имя их пленного было граф Безухов? Узнав, что Безухов в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне. В числе отбитых Денисовым и Долоховым русских пленных был Пьер Безухов.' )
        test_file_three.close()
        self.indexator.get_index_with_line('test_qulim_search_1.txt')
        self.indexator.get_index_with_line('test_qulim_search_2.txt')
        del self.indexator
        self.search = SearchEngine('database')
        query = 'Пьер Безухов Пьер'
        result = self.search.qulim_search(query, win_size=1, limit=2, offset=0, doc_limof =[(1,0), (2,0)] )
        fine_result = {'test_qulim_search_1.txt': ['Узнав, что <b>Безухов</b> в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне.'],
                      'test_qulim_search_2.txt':['Кому, в особенности ему, какое дело было до того, что узнают или не узнают, что имя их пленного было граф <b>Безухов</b>? Узнав, что <b>Безухов</b> в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне.',
                                                 'В числе отбитых Денисовым и Долоховым русских пленных был <b>Пьер</b> <b>Безухов</b>.']}
        self.assertEqual(result, fine_result)
        os.remove('test_qulim_search_1.txt')
        os.remove('test_qulim_search_2.txt')
        
    def test_qulim_search_modified(self):
        test_file_two = open('test_qulim_search_1.txt', 'w') 
        test_file_two.write('Узнав, что Безухов в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне. Вилларский скучал в Орле и был счастлив, встретив человека одного с собой круга и с одинаковыми, как он полагал, интересами. Умный и смелый Пьер хочет быть декабристом.')
        test_file_two.close()
        test_file_three = open('test_qulim_search_2.txt', 'w') 
        test_file_three.write('Кому, в особенности ему, какое дело было до того, что узнают или не узнают, что имя их пленного было граф Безухов? Узнав, что Безухов в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне. В числе отбитых Денисовым и Долоховым русских пленных был Пьер Безухов.' )
        test_file_three.close()
        self.indexator.get_index_with_line('test_qulim_search_1.txt')
        self.indexator.get_index_with_line('test_qulim_search_2.txt')
        del self.indexator
        self.search = SearchEngine('database')
        query = 'Пьер Безухов Пьер'
        result = self.search.qulim_search_modified(query, win_size=1, limit=2, offset=0, doc_limof =[(1,0), (2,0)] )
        fine_result = {'test_qulim_search_1.txt': ['Узнав, что <b>Безухов</b> в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне.'],
                      'test_qulim_search_2.txt':['Кому, в особенности ему, какое дело было до того, что узнают или не узнают, что имя их пленного было граф <b>Безухов</b>? Узнав, что <b>Безухов</b> в Орле, Вилларский, хотя и никогда не был коротко знаком с ним, приехал к нему с теми заявлениями дружбы и близости, которые выражают обыкновенно друг другу люди, встречаясь в пустыне.',
                                                 'В числе отбитых Денисовым и Долоховым русских пленных был <b>Пьер</b> <b>Безухов</b>.']}
        self.assertEqual(result, fine_result)
        os.remove('test_qulim_search_1.txt')
        os.remove('test_qulim_search_2.txt')
        
    def test_qulim_search_modified_one(self):
        test_file_one = open('test_qulim_search_1.txt', 'w') 
        test_file_one.write('Smart Student Alina Zakharova is a linguist!! Smart Student Alina Zakharova tries to write programs. Python is easy, Zakharova, keep calm caaalm!!!')
        test_file_one.close()
        test_file_two = open('test_qulim_search_2.txt', 'w') 
        test_file_two.write('Little funny girl Alina loves big apples. Also extra smart student Alina Zakharova loves rock music.')
        test_file_two.close()
        test_file_three = open('test_qulim_search_3.txt', 'w') 
        test_file_three.write('Beautiful and perfect Alina Zakharova loves sweets and black coffee. Also cute and nice Alina Zakharova loves Disney cartoons.')
        test_file_three.close()
        self.indexator.get_index_with_line('test_qulim_search_1.txt')
        self.indexator.get_index_with_line('test_qulim_search_2.txt')
        self.indexator.get_index_with_line('test_qulim_search_3.txt')
        del self.indexator

        self.search = SearchEngine('database')
        query = 'Alina Zakharova'
        result = self.search.qulim_search_modified(query, win_size=1, limit=2, offset=1, doc_limof =[(2,0), (1,0)] )
        fine_result = {
                      'test_qulim_search_2.txt': ['Little funny girl <b>Alina</b> loves big apples.',
                                                    'Also extra smart student <b>Alina</b> <b>Zakharova</b> loves rock music.'],
                      'test_qulim_search_3.txt':['Beautiful and perfect <b>Alina</b> <b>Zakharova</b> loves sweets and black coffee.']}
        self.assertEqual(result, fine_result)
        os.remove('test_qulim_search_1.txt')
        os.remove('test_qulim_search_2.txt')
        os.remove('test_qulim_search_3.txt')    

    def test_qulim_search_empty(self):
        test_file_one = open('test_qulim_search_1.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student!! Zakharova tries to write programs. Python is easy, Zakharova, keep calm!!!')
        test_file_one.close()
        test_file_two = open('test_qulim_search_2.txt', 'w') 
        test_file_two.write('Little Zakharova loves big apples. Also Zakharova loves rock music.')
        test_file_two.close()
        self.indexator.get_index_with_line('test_qulim_search_1.txt')
        self.indexator.get_index_with_line('test_qulim_search_2.txt')
        del self.indexator
        self.search = SearchEngine('database')
        query = 'Scorpions'
        result = self.search.qulim_search(query, win_size=1, limit=2, offset=0, doc_limof =[(3,0), (3,0)] )
        fine_result = {}
        self.assertEqual(result, fine_result)
        os.remove('test_qulim_search_1.txt')
        os.remove('test_qulim_search_2.txt')
        
    
        

                    
       
if __name__ == '__main__':
    unittest.main()        


