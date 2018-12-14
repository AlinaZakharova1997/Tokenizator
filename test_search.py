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

        
if __name__ == '__main__':
    unittest.main()      
