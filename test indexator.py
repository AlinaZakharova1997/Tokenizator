import unittest
import os 
import indexer
import shelve
from indexer import Indexer
class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.x = Indexer()
       ''' file = open('testfile.txt', 'w') # there the file is created
        file.write('Alina is a student')
        file.close()''' # надо это здесь писать?
        
    def test_MyError_notFile(self):
        with self.assertRaises(ValueError):
          self.x.get_index(12)
          
    def test_if_file_exists(self):
        with self.assertRaises(ValueError):
          self.x.get_index('None.txt')
          
    def test_database_one_token(self):
        file = open('testfile.txt', 'w') 
        file.write('Alina')
        file.close()
        self.x.get_index('testfile.txt')
        # for current directory use '.'
        file_list= os.listdir(path=".")
        assert_true=False
        for i in file_list:
            if i startswith('database'):
               assert_true= True
            elif i startswith('database.'):
                assert_true= True
            else:
                assert_true= False
        self.assertEqual(assert_true, True)
        base_dict = dict(shelve.open('database.'))
        cool_result = {'Alina':{'testfile.txt':[Position(0,5)]}} # perfect dictionary element
        self.assertEqual(base_dict,cool_result)
        os.remove(file)
        
   def test_database_many_tokens(self):
        file = open('testfile.txt', 'w') 
        file.write(' Ф 12 !!! @ # Alina is a student)))')
        file.close()
        self.x.get_index('testfile.txt')
        # for current directory use '.'
        file_list= os.listdir(path=".")
        assert_true=False
        for i in file_list:
            if i startswith('database'):
               assert_true= True
            elif i startswith('database.'):
                assert_true= True
            else:
                assert_true= False
        self.assertEqual(assert_true, True)
        base_dict = dict(shelve.open('database.'))
        cool_result = {' ':{'testfile.txt':[Position(0,1)]},{'Ф':{'testfile.txt':[Position(1,2)]},
                       {' ':{'testfile.txt':[Position(2,3)]},{'12':{'testfile.txt':[Position(3,5)]},
                       {' ':{'testfile.txt':[Position(5,6)]},{'!!!':{'testfile.txt':[Position(6,3)]},
                       {' ':{'testfile.txt':[Position(6,7)]},{'@':{'testfile.txt':[Position(7,8)]},
                       {' ':{'testfile.txt':[Position(8,9)]},{'#':{'testfile.txt':[Position(9,10)]},
                       {'Alina':{'testfile.txt':[Position(10,15)]},{' ':{'testfile.txt':[Position(15,16)]},
                       {'is':{'testfile.txt':[Position(16,18)]},{' ':{'testfile.txt':[Position(18,19)]},
                       {'a':{'testfile.txt':[Position(19,20)]},{' ':{'testfile.txt':[Position(20,21)]},
                       {'student':{'testfile.txt':[Position(21,28)]},{')))':{'testfile.txt':[Position(28,31)]} # perfect dictionary 
        self.assertEqual(base_dict,cool_result)
        os.remove(file)
                                                                      
  def test_many_files(self):
        file_one = open('testfile_1.txt', 'w') 
        file_one.write(' Ф 12 !!! @ # Alina is a student)))')
        file_one.close()
        file_two = open('testfile_2.txt', 'w') 
        file_two.write('Alina')
        file_two.close()                                            
        self.x.get_index('testfile_1.txt')
        self.x.get_index('testfile_2.txt')                                                              
        # for current directory use '.'
        file_list= os.listdir(path=".")
        assert_true=False
        for i in file_list:
            if i startswith('database_one'):
               assert_true= True
            elif i startswith('database_one.'):
                assert_true= True                                                          
            else:
                assert_true= False
        self.assertEqual(assert_true, True)
            if i  startswith('database_two'):
               assert_true= True
            elif i startswith('database_two.'):
                assert_true= True                                                          
            else:
                assert_true= False
        self.assertEqual(assert_true, True)                                                       
        base_dict_one = dict(shelve.open('database.'))
        cool_result_one = {' ':{'testfile.txt':[Position(0,1)]},{'Ф':{'testfile.txt':[Position(1,2)]},
                       {' ':{'testfile.txt':[Position(2,3)]},{'12':{'testfile.txt':[Position(3,5)]},
                       {' ':{'testfile.txt':[Position(5,6)]},{'!!!':{'testfile.txt':[Position(6,3)]},
                       {' ':{'testfile.txt':[Position(6,7)]},{'@':{'testfile.txt':[Position(7,8)]},
                       {' ':{'testfile.txt':[Position(8,9)]},{'#':{'testfile.txt':[Position(9,10)]},
                       {'Alina':{'testfile.txt':[Position(10,15)]},{' ':{'testfile.txt':[Position(15,16)]},
                       {'is':{'testfile.txt':[Position(16,18)]},{' ':{'testfile.txt':[Position(18,19)]},
                       {'a':{'testfile.txt':[Position(19,20)]},{' ':{'testfile.txt':[Position(20,21)]},
                       {'student':{'testfile.txt':[Position(21,28)]},{')))':{'testfile.txt':[Position(28,31)]} # perfect dictionary 
        self.assertEqual(base_dict,cool_result)                                                              
        os.remove(file_one)
        base_dict_two = dict(shelve.open('database.'))
        cool_result_two = {'Alina':{'testfile.txt':[Position(0,5)]}} # perfect dictionary element
        self.assertEqual(base_dict_two,cool_result_two)
        os.remove(file_two)                                                              
            
if __name__ == '__main__':
    unittest.main()        
