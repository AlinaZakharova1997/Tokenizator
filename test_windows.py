import unittest
import os
import shelve
import tokenizator
from tokenizator import Tokenizator
import windows
from windows import Context_Window
import indexer
from indexer import Indexer,Position_Plus
import search
from search import SearchEngine

class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
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
            Context_Window.get_window(12,'12')
                
    def test_get_window_simple(self):
        indexator = Indexer('database')
        test_file_one = open('test_window_one.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student)))')
        test_file_one.close()
        indexator.get_index_with_line('test_window_one.txt')
        del indexator
        search = SearchEngine('database')  
        result = Context_Window.get_window('test_window_one.txt', Position_Plus(0, 16, 18), 1)
        win = Context_Window('Alina Zakharova is a student)))', [Position_Plus(0, 16, 18)], 6, 20)
        self.assertEqual(result.string, win.string)
        self.assertEqual(result.positions, win.positions)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)
        os.remove('test_window_one.txt')

    def test_get_window_simple_plus(self):
        indexator = Indexer('database')
        test_file_one = open('test_window_two.txt', 'w') 
        test_file_one.write('Little Alina Zakharova is a linguist student)))')
        test_file_one.close()
        indexator.get_index_with_line('test_window_two.txt')
        del indexator
        search = SearchEngine('database')  
        result = Context_Window.get_window('test_window_two.txt', Position_Plus(0, 23, 25), 2)
        win = Context_Window('Little Alina Zakharova is a linguist student)))', [Position_Plus(0, 23, 25)], 7, 36)
        self.assertEqual(result.string, win.string)
        self.assertEqual(result.positions, win.positions)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result,win)
        os.remove('test_window_two.txt')
        
    def test_get_window_begin(self):
        indexator = Indexer('database')
        test_file_one = open('test_window_three.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student')
        test_file_one.close()
        indexator.get_index_with_line('test_window_three.txt')
        del indexator
        search = SearchEngine('database')  
        result = Context_Window.get_window('test_window_three.txt', Position_Plus(0, 0, 5), 2)
        win = Context_Window('Alina Zakharova is a student', [Position_Plus(0, 0, 5)], 0, 18)
        self.assertEqual(result.string, win.string)
        self.assertEqual(result.positions, win.positions)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)
        os.remove('test_window_three.txt')

    def test_get_window_end(self):
        indexator = Indexer('database')
        test_file_one = open('test_window_four.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student')
        test_file_one.close()
        indexator.get_index_with_line('test_window_four.txt')
        del indexator
        search = SearchEngine('database')
        result = Context_Window.get_window('test_window_four.txt', Position_Plus(0, 21, 28), 3)
        win = Context_Window('Alina Zakharova is a student', [Position_Plus(0, 21, 28)], 6, 28)
        self.assertEqual(result.string, win.string)
        self.assertEqual(result.positions, win.positions)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)
        os.remove('test_window_four.txt')

    def test_myError_str_not_found(self):
        indexator = Indexer('database')
        test_file_one = open('test_window_five.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student')
        test_file_one.close()
        indexator.get_index_with_line('test_window_five.txt')
        del indexator
        search = SearchEngine('database')
        with self.assertRaises(IndexError):
            result = Context_Window.get_window('test_window_five.txt', Position_Plus(3, 21, 28), 3)
        os.remove('test_window_five.txt')    
       

if __name__ == '__main__':
    unittest.main()        
        

