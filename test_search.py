import unittest
import search
from search import SearchEngine
import os
import shelve
import indexer
from indexer import Indexer, Position_Plus

class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.database = SearchEngine('database')
        self.indexator = Indexer('database')
        self.maxDiff = None

    def test_MyError_give_dict_inp(self):
        with self.assertRaises(TypeError):
            self.database.get_dict(12)
            
    def test_get_dict(self):
        test_file = open('test_search_one.txt', 'w',encoding='utf-8') 
        test_file.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file.close()
        self.indexator.get_index('test_search_one.txt')
        del self.indexator
        database = dict(shelve.open('database'))
        self.database.get_dict('Alina')
        cool_result = {'test_search_one.txt': [Position_Plus(0,14,19)]}
        self.assertEqual(database, cool_result)
        os.remove('test_search_one.txt')
        
if __name__ == '__main__':
    unittest.main()    
