import unittest
import os
import shelve
import windows
from windows import Context_Windows
import indexer
from indexer import Indexer,Position_Plus
import search
from search import SearchEngine

class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
        self.window = Context_Windows('string','positions')
        self.indexator = Indexer('database')

    def tearDown(self):
        if hasattr(self, 'search'):
            del self.search
        file_list = os.listdir(path=".")
        for i in file_list:
            if i == 'database':
                database_exists = True
                os.remove(i)
            elif i.startswith('database.'):
                database_exists= True
                os.remove(i)    

    def test_get_window_error(self):
         with self.assertRaises(TypeError):
            self.window.get_window(12,'12')
                
    def test_get_window_simple(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = self.get_window('is',1)
        cool_result = 'Zakaharova is a'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')
        
    def test_get_window_begin(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = self.get_window('Alina',1)
        cool_result = 'Alina Zakaharova'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')

    def test_get_window_end(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = self.get_window('student',1)
        cool_result = 'a student'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')

    def test_get_window_words(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write('Alina Zakharova Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.get_window('Alina Zakharova',1)
        cool_result = 'Alina Zakharova','Alina Zakharova Alina'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')   
        

    '''def test_get_window_overlap(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.get_window('Alina Zakharova',1)
        cool_result = 'Alina Zakharova is'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')

    def test_get_window_overlap_many(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina Zakharova')
        test_file_one.close()
        test_file_two = open('test_window_two.txt', 'w') 
        test_file_two.write(' Alina loves apples)))')
        test_file_two.close()
        test_file_three = open('test_window_three.txt', 'w') 
        test_file_three.write(' Ф 12 !!! @ # student)))')
        test_file_three.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        self.indexator.get_index_with_line('test_window_two.txt')
        self.indexator.get_index_with_line('test_window_three.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.get_window('Alina Zakharova',1)
        cool_result = 'Alina Zakharova loves'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')
        os.remove('test_window_two.txt')
        os.remove('test_window_three.txt')

    def test_get_window_overlap_not(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina is a student')
        test_file_one.close()
        test_file_two = open('test_window_two.txt', 'w') 
        test_file_two.write(' Little Zakaharova loves big apples)))')
        test_file_two.close()
        test_file_three = open('test_window_three.txt', 'w') 
        test_file_three.write(' Ф 12 !!! @ # student loves apples')
        test_file_three.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        self.indexator.get_index_with_line('test_window_two.txt')
        self.indexator.get_index_with_line('test_window_three.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.get_window('Alina Zakharova',1)
        cool_result = 'Alina is','Little Zakaharova loves'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')
        os.remove('test_window_two.txt')
        os.remove('test_window_three.txt')'''
        

if __name__ == '__main__':
    unittest.main()        
        

