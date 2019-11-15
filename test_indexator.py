import unittest
import os 
import indexer
import shelve
from indexer import Indexer, Position, Position_Plus


class TestMyCode(unittest.TestCase):
    
    def setUp(self):
        self.indexator = Indexer('database')
        self.maxDiff = None
       
    def tearDown(self):
        # for current directory use '.'
        file_list = os.listdir(path=".")
        for i in file_list:
            if i == 'database':
                database_exists = True
                os.remove(i)
            elif i.startswith('database.'):
                database_exists= True
                os.remove(i)
        
    def test_MyError_notFile(self):
        with self.assertRaises(TypeError):
            self.indexator.get_index(12)
          
    def test_if_file_exists(self):
        with self.assertRaises(FileNotFoundError):
            self.indexator.get_index('None.txt')
            
    def test__lt__same_line(self):
        pos = Position_Plus(0, 2, 4)
        other_pos = Position_Plus(0, 0, 1)
        result = other_pos.__lt__(pos)
        self.assertEqual(result, True)
        
    def test_lt_diff_lines(self):
        pos = Position_Plus(1, 2, 4)
        other_pos = Position_Plus(0, 0, 1)
        result = other_pos.__lt__(pos)
        self.assertEqual(result, True)
        
    def test_database_one_token(self):
        test_file = open('testfile.txt', 'w') 
        test_file.write('Alina')
        test_file.close()
        self.indexator.get_index('testfile.txt')
        del self.indexator
        base_dict = dict(shelve.open('database'))
        cool_result = {'Alina': {'testfile.txt': [Position(0,5)]}}  # perfect dictionary 
        self.assertEqual(base_dict, cool_result)
        os.remove('testfile.txt')  
        
    def test_database_many_tokens(self):
        test_file = open('testfile_many.txt', 'w') 
        test_file.write(' Ф 12 !!! @ # Alina is a student)))')
        test_file.close()
        self.indexator.get_index('testfile_many.txt')
        del self.indexator
        base_dict = dict(shelve.open('database'))
        cool_result = {
                       'Ф': {'testfile_many.txt': [Position(1, 2)]},
                       '12': {'testfile_many.txt': [Position(3, 5)]},
                       'Alina': {'testfile_many.txt':[Position(14, 19)]},
                       'is': {'testfile_many.txt': [Position(20, 22)]},
                       'a': {'testfile_many.txt': [Position(23, 24)]},
                       'student': {'testfile_many.txt': [Position(25, 32)]},
                      }                                                      
        self.assertEqual(base_dict, cool_result)
        os.remove('testfile_many.txt')           
                                                                      
    def test_many_files (self):
        file_one = open('testfile_1.txt', 'w') 
        file_one.write(' Ф 12 !!! @ # Alina is a student)))')
        file_one.close()
        file_two = open('testfile_2.txt', 'w') 
        file_two.write('Alina')
        file_two.close()                                            
        self.indexator.get_index('testfile_1.txt')
        self.indexator.get_index('testfile_2.txt') 
        del self.indexator                                                                 
        base_dict = dict(shelve.open('database'))
        cool_result = {
                       'Ф': {'testfile_1.txt': [Position(1, 2)]},
                       '12': {'testfile_1.txt': [Position(3, 5)]},
                       'Alina': {'testfile_1.txt': [Position(14, 19)],'testfile_2.txt':[Position(0, 5)]},
                       'is': {'testfile_1.txt': [Position(20, 22)]},
                       'a': {'testfile_1.txt': [Position(23, 24)]},
                       'student': {'testfile_1.txt': [Position(25, 32)]}
                      }  
        self.assertEqual(base_dict, cool_result)                                                              
        os.remove('testfile_1.txt')
        os.remove('testfile_2.txt')                                                             
                                                                          
    def test_lines(self):
        file_line = open ('testfile_line.txt','w')
        file_line.write('Ф 12 !!! @ # Alina is a student))) \n Alina likes apples 1997\n\n')
        file_line.close()
        self.indexator.get_index_with_line('testfile_line.txt')
        del self.indexator                                                                 
        base_dict = dict(shelve.open('database'))
        cool_result = {'Ф': {'testfile_line.txt': [Position_Plus(0, 0, 1)]},
                       '12': {'testfile_line.txt': [Position_Plus(0, 2, 4)]},
                       'Alina': {'testfile_line.txt': [Position_Plus(0, 13, 18),Position_Plus(1, 1, 6)]},
                       'is': {'testfile_line.txt': [Position_Plus(0, 19, 21)]},
                       'a': {'testfile_line.txt': [Position_Plus(0, 22, 23)]},
                       'student': {'testfile_line.txt': [Position_Plus(0, 24, 31)]},
                       'likes' : {'testfile_line.txt': [Position_Plus(1, 7, 12)]},
                       'apples': {'testfile_line.txt': [Position_Plus(1, 13, 19)]},
                       '1997': {'testfile_line.txt': [Position_Plus(1, 20, 24)]}
                       }
        self.assertEqual(base_dict, cool_result)
        os.remove('testfile_line.txt')

    def emptiness(self):
        file_line = open ('testfile_line.txt','w')
        file_line.write('')
        file_line.close()
        del self.indexator
        os.remove('testfile_line.txt')
        
if __name__ == '__main__':
    unittest.main() 
       

