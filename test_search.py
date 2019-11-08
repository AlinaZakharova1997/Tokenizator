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
       test_file_two.write('Little Zakharova loves big apples')
       test_file_two.close()
       self.indexator.get_index_with_line('test_query_search_one.txt')
       self.indexator.get_index_with_line('test_query_search_two.txt')
       del self.indexator
       self.search = SearchEngine('database')
       query = 'Zakharova'
       result = self.search.query_search(query, 1)
       fine_result = {'test_query_search_one.txt':['Alina <b>Zakharova</b> is a student!!'],
                      'test_query_search_two.txt':['Little <b>Zakharova</b> loves big apples']}
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
        test_file_two.write('Little funny girl Alina Zakharova loves big apples. Also extra smart student Alina Zakharova loves rock music.')
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
                      'test_qulim_search_2.txt': ['Little funny girl <b>Alina</b> <b>Zakharova</b> loves big apples.',
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
        test_file_two.write('Маленькая смешная девочка Алина Захарова любит большие яблоки. Также очень умная ученица Алина Захарова любит рок-музыку.')
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
                      'test_qulim_search_2.txt': ['Маленькая смешная девочка <b>Алина</b> <b>Захарова</b> любит большие яблоки.',
                                                    'Также очень умная ученица <b>Алина</b> <b>Захарова</b> любит рок-музыку.'],
                      'test_qulim_search_3.txt':['Прекрасная и идеальная <b>Алина</b> <b>Захарова</b> любит сладости и черный кофе.']}
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
