import unittest
import search
from search import SearchEngine
import os
import shelve
import indexer
from indexer import Indexer, Position_Plus
from windows import Context_Window

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

    def test_unite_all(self):
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
        self.indexator.get_index_with_line('test_unite_all.txt')
        del self.indexator
        self.search = SearchEngine('database')
        dictionary = self.search.get_dict_many_tokens('Alina Zakharova is a student')
        input_dictionary = {'test_unite_all.txt':[Position_Plus(0, 0, 5),Position_Plus(0, 6, 15),
                                                  Position_Plus(0, 16, 18),Position_Plus(0, 19, 20),
                                                  Position_Plus(0, 21, 28)]}
        self.assertEqual(dictionary, input_dictionary)
        dict_to_function =   self.search.unite_all(dictionary, 1)
        output_dict = {'test_unite_all.txt':[Context_Window('Alina Zakharova is a student',[Position_Plus(0, 0, 5), Position_Plus(0, 6, 15),
                                                                                            Position_Plus(0, 16, 18), Position_Plus(0, 19, 20),
                                                                                            Position_Plus(0, 21, 28)], 0, 28)]}
                                            
        self.assertEqual(dict_to_function, output_dict)
        os.remove('test_unite_all.txt')

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

    def test_unite_extended(self):
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
        
    def test_query_search(self):
       test_file_one = open('test_query_search.txt', 'w') 
       test_file_one.write('Alina Zakharova is a student!!')
       test_file_one.close()
       self.indexator.get_index_with_line('test_query_search.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.query_search(query, 1)
       fine_result = {'test_query_search.txt':['Alina <b>Zakharova</b> is a student!!']}
       self.assertEqual(result, fine_result)
       os.remove('test_query_search.txt')
    
    def test_qulim_search(self):
       test_file_one = open('test_qulim_search_one.txt', 'w') 
       test_file_one.write('Alina Zakharova is a student!! /n Zakharova tries to write programs /n Python is easy, Zakharova, keep calm!!!'')
       test_file_one.close()
       test_file_two = open('test_qulim_search_two.txt', 'w') 
       test_file_two.write('Little Zakharova loves big apples /n Also Zakharova loves rock music')
       test_file_two.close()
       self.indexator.get_index_with_line('test_qulim_search_one.txt')
       self.indexator.get_index_with_line('test_qulim_search_two.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.qulim_search(query, win_size=1, limit=2, offset=0, doc_limof =[(2,1), (3,0)] )
       fine_result = {'test_qulim_search_one.txt':['<b>Zakharova</b> tries to write programs',
                                                   'Python is easy, <b>Zakharova</b>, keep calm!!!'],
                      'test_qulim_search_two.txt':['Little <b>Zakharova</b> loves big apples',
                                                   'Also <b>Zakharova</b> loves rock music']}
       self.assertEqual(result, fine_result)
       os.remove('test_qulim_search_one.txt')
       os.remove('test_qulim_search_two.txt')

    def test_qulim_search_empty(self):
       test_file_one = open('test_qulim_search_one.txt', 'w') 
       test_file_one.write('Alina Zakharova is a student!! /n Zakharova tries to write programs /n Python is easy, Zakharova, keep calm!!!'')
       test_file_one.close()
       test_file_two = open('test_qulim_search_two.txt', 'w') 
       test_file_two.write('Little Zakharova loves big apples /n Also Zakharova loves rock music')
       test_file_two.close()
       self.indexator.get_index_with_line('test_qulim_search_one.txt')
       self.indexator.get_index_with_line('test_qulim_search_two.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Scorpions'
       result = self.search.qulim_search(query, win_size=1, limit=2, offset=0, doc_limof =[(3,0), (3,0)] )
       fine_result = {}
       self.assertEqual(result, fine_result)
       os.remove('test_qulim_search_one.txt')
       os.remove('test_qulim_search_two.txt')                       

          
   
        
if __name__ == '__main__':
    unittest.main()     

