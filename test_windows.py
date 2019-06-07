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
        self.window = Context_Window('The girl named Alina Zakharova is a student',[Position_Plus(0, 4, 20),Position_Plus(0, 9, 30)],8,20)
        
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
        result = windows.Context_Window.get_window('test_window_one.txt',Position_Plus(0, 16, 18),1)
        self.win = Context_Window('string','positions','win_start','win_end')
        self.win.string ='Alina Zakharova is a student)))'
        self.win.positions = [Position_Plus(0,16,18)]
        self.win.win_start = 6
        self.win.win_end = 20
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(result.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_one.txt')

    def test_get_window_simple_plus(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_two.txt', 'w') 
        test_file_one.write('Little Alina Zakharova is a linguist student)))')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_two.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = windows.Context_Window.get_window('test_window_two.txt',Position_Plus(0, 23, 25),2)
        self.win = Context_Window('string','positions','win_start','win_end')
        self.win.string = 'Little Alina Zakharova is a linguist student)))'
        self.win.positions = [Position_Plus(0,23,25)]
        self.win.win_start = 7
        self.win.win_end = 36
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(result.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_two.txt')
        
    def test_get_window_begin(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_three.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_three.txt')
        del self.indexator
        self.search = SearchEngine('database')  
        result = windows.Context_Window.get_window('test_window_three.txt',Position_Plus(0, 0, 5),1)
        self.win = Context_Window('string','positions','win_start','win_end')
        self.win.string = 'Alina Zakharova is a student'
        self.win.positions = [Position_Plus(0, 0, 5)]
        self.win.win_start = 0
        self.win.win_end = 15
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(result.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_three.txt')

    def test_get_window_end(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_four.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_four.txt')
        del self.indexator
        self.search = SearchEngine('database')
        result = windows.Context_Window.get_window('test_window_four.txt', Position_Plus(0, 21, 28), 3)
        self.win = Context_Window('string','positions','win_start','win_end')
        self.win.string = 'Alina Zakharova is a student'
        self.win.positions = [Position_Plus(0, 21, 28)]
        self.win.win_start = 6
        self.win.win_end = 28
        self.assertEqual(result.string,self.win.string)
        self.assertEqual(result.positions,self.win.positions)
        self.assertEqual(result.win_start,self.win.win_start)
        self.assertEqual(result.win_end, self.win.win_end)
        self.assertEqual(result, self.win)
        os.remove('test_window_four.txt')

    def test_myError_str_not_found(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_window_five.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student')
        test_file_one.close()
        self.indexator.get_index_with_line('test_window_five.txt')
        del self.indexator
        self.search = SearchEngine('database')
        with self.assertRaises(TypeError):
            result = windows.Context_Window.get_window('test_window_five.txt', Position_Plus(3, 21, 28), 3)
        os.remove('test_window_five.txt')

    def test_united_type_error(self):
       with self.assertRaises(TypeError):
            self.window.get_united_window(12, 'window)))')
            
    def test_crossed_type_error(self):
       with self.assertRaises(TypeError):
            self.window.is_crossed(12, 'window)))')         

    def test_united_window(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_united_window.txt', 'w') 
        test_file_one.write('The girl named Alina Zakharova is a student')
        test_file_one.close()
        self.indexator.get_index_with_line('test_united_window.txt')
        del self.indexator
        self.search = SearchEngine('database')
        window_A = windows.Context_Window.get_window('test_united_window.txt', Position_Plus(0, 4, 20), 1)
        window_B = windows.Context_Window.get_window('test_united_window.txt', Position_Plus(0, 9, 30), 1)
        united_AB = window_A.get_united_window(window_B)
        self.win = windows.Context_Window('The girl named Alina Zakharova is a student',[Position_Plus(0, 4, 20),Position_Plus(0, 9, 30)],9,20)
        self.assertEqual(window_A.string, self.win.string)
        self.assertEqual(window_A.win_start, self.win.win_start)
        self.assertEqual(window_A.win_end, self.win.win_end)
        os.remove('test_united_window.txt')
        
    def test_is_crossed(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_crossed_window.txt', 'w') 
        test_file_one.write('The girl named Alina Zakharova is a student')
        test_file_one.close()
        self.indexator.get_index_with_line('test_crossed_window.txt')
        del self.indexator
        self.search = SearchEngine('database')
        window_A = windows.Context_Window.get_window('test_crossed_window.txt', Position_Plus(0, 15, 20), 1)
        window_B = windows.Context_Window.get_window('test_crossed_window.txt', Position_Plus(0, 8, 14), 1)
        crossed_AB = window_A.is_crossed(window_B)
        self.assertEqual(True, crossed_AB)
        os.remove('test_crossed_window.txt')  

    def test_not_crossed(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_not_crossed_window.txt', 'w') 
        test_file_one.write('The girl named Alina Zakharova is a student')
        test_file_one.close()
        self.indexator.get_index_with_line('test_not_crossed_window.txt')
        del self.indexator
        self.search = SearchEngine('database')
        window_A = windows.Context_Window.get_window('test_not_crossed_window.txt', Position_Plus(0, 31, 33), 1)
        window_B = windows.Context_Window.get_window('test_not_crossed_window.txt', Position_Plus(0, 8, 14), 1)
        crossed_AB = window_A.is_crossed(window_B)
        self.assertEqual(False, crossed_AB)
        os.remove('test_not_crossed_window.txt')
   
            
    def test_extend_window(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_extend_window.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student!!')
        test_file_one.close()
        self.indexator.get_index_with_line('test_extend_window.txt')
        del self.indexator
        self.search = SearchEngine('database')
        window = windows.Context_Window.get_window('test_extend_window.txt', Position_Plus(0, 6, 15), 1)
        window.extend_window()
        extended_window = Context_Window('Alina Zakharova is a student!!',[Position_Plus(0, 6, 15)], 0, 30)
        self.assertEqual(window, extended_window)
        os.remove('test_extend_window.txt') 
        
    def test_already_extended_window(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_already_extended_window.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student!!')
        test_file_one.close()
        self.indexator.get_index_with_line('test_already_extended_window.txt')
        del self.indexator
        self.search = SearchEngine('database')
        window = windows.Context_Window.get_window('test_already_extended_window.txt',Position_Plus(0, 16, 18), 2)
        os.remove('test_already_extended_window.txt')
        
    def test_highlight_window_one(self):
        self.indexator = Indexer('database')
        test_file_one = open('test_highlight_window.txt', 'w') 
        test_file_one.write('Alina Zakharova is a student')
        test_file_one.close()
        self.indexator.get_index_with_line('test_highlight_window.txt')
        del self.indexator
        self.search = SearchEngine('database')
        window = windows.Context_Window.get_window('test_highlight_window.txt', Position_Plus(0, 6, 15), 1)
        result = window.highlight_window()
        output_string = 'Alina <b>Zakharova</b> is'
        self.assertEqual(result, output_string)
        os.remove('test_highlight_window.txt')
       
  


        
if __name__ == '__main__':
    unittest.main()

   
        
