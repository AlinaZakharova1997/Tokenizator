import unittest
import search
from search import SearchEngine
import os
import shelve
import indexer
from indexer import Indexer, Position_Plus


class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
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
        self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
            self.search.get_dict(12)
            
    def test_get_dict(self):
        self.indexator = Indexer('database')
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
        self.indexator = Indexer('database')
        test_file = open('test_search_one.txt', 'w') 
        test_file.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.search.get_dict('Laptop')
        os.remove('test_search_one.txt')
        
    def test_MyError_dive_dict_many_tokens_inp(self):
       self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
            self.search.get_dict_many_tokens(12)

    def test_get_dict_many_tokens(self):
       self.indexator = Indexer('database')
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file_one.close()
        test_file_two = open('test_search_two.txt', 'w') 
        test_file_two.write(' Ф 12 !!! @ # Alina loves apples)))')
        test_file_two.close()
        test_file_three = open('test_search_three.txt', 'w') 
        test_file_three.write(' Ф 12 !!! @ # Alina ££ student)))')
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
        test_file_three.write(' Ф 12 !!! @ # Alina ££ student)))')
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

if __name__ == '__main__':
    unittest.main()      
