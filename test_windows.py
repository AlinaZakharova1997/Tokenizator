import unittest
import os
import shelve
import tokenizator
from tokenizator import Tokenizator
import windows
from windows import Context_Windows
import indexer
from indexer import Indexer,Position_Plus
import search
from search import SearchEngine

class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
        self.window = Context_Windows('string','positions','win_start','win_end')

    def tearDown(self):
        if hasattr(self, 'search'):
            del self.search
        file_list = os.listdir(path=".")
        for i in file_list:
            if i == 'database':
                database_exists = True
                os.remove(i)
            elif i.startswith('database.'):
                database_exists = True
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
        result = self.window.get_window('test_window_one.txt',Position_Plus(0, 16, 18),1)
        self.win = Context_Windows('string','positions','win_start','win_end')
        self.win.string ='Zakaharova is a'
        self.win.positions = [Position_Plus(0,6,15),Position_Plus(0,16,18),Position_Plus(0,19,20)]
        self.win.win_start = Position_Plus(0,6,15)
        self.win.win_end = Position_Plus(0,19,20)
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(resutl.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_one.txt')

    def test_get_window_simple_plus(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Little Alina Zakharova is a linguist student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = self.window.get_window('test_window_one.txt',Position_Plus(0, 23, 24),2)
        self.win = Context_Windows('string','positions','win_start','win_end')
        self.win.string = 'Alina Zakharova is a linguist'
        self.win.positions = [Position_Plus(0,7,12),Position_Plus(0,13,22),Position_Plus(0,23,24),Position_Plus(0,25,26),Position_Plus(0,27,35)]
        self.win.win_start = Position_Plus(0,7,12)
        self.win.win_end = Position_Plus(0,27,35)
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(resutl.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_one.txt')
        
    def test_get_window_begin(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_one.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = self.window.get_window('test_window_one.txt',Position_Plus(0, 0, 5),1)
        self.win = Context_Windows('string','positions','win_start','win_end')
        self.win.string = 'Alina Zakaharova'
        self.win.positions = [Position_Plus(0, 0, 5),Position_Plus(0, 6, 15)]
        self.win.win_start = Position_Plus(0, 0, 5)
        self.win.win_end = Position_Plus(0, 6, 15)
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(resutl.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_one.txt')

    def test_get_window_end(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = self.window.get_window('test_window_one.txt',Position_Plus(0, 21, 28),3)
        self.win = Context_Windows('string','positions','win_start','win_end')
        self.win.string = 'Zakharova is a student'
        self.win.positions = [Position_Plus(0,6,15),Position_Plus(0,16,18),Position_Plus(0,19,20),Position_Plus(0, 21, 28)]
        self.win.win_start = Position_Plus(0,6,15)
        self.win.win_end = Position_Plus(0, 21, 28)
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(resutl.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_one.txt')

    """def test_get_window_words(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_search_one.txt', 'w') 
        test_file_one.write('Alina Zakharova Alina Zakharova is a student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_search_one.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = self.window.get_window('Alina Zakharova',1)
        cool_result = 'Alina Zakharova','Alina Zakharova Alina'
        self.assertEqual(result, cool_result)
        os.remove('test_window_one.txt')"""
        

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
        os.remove('test_window_three.txt')
'''
        

if __name__ == '__main__':
    unittest.main()        
        

