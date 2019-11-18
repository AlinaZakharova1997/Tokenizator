import make_selection
import unittest

class TestMyCode(unittest.TestCase):
   
    def test_one(self):
        
        lists = [[('собака', 23),('кот', 15), ('девочка', 30)],
                 [('тигр', 20),('мальчик', 45), ('конфета', 3), ('хор', 1)],
                 [('лингвист', 10),('программист', 56)]]
        
        result = list(make_selection.lemma_generator(lists))
        cool = ['программист','мальчик','девочка','собака','тигр','кот','лингвист','конфета','хор']
        self.assertEqual(result, cool)


if __name__ == '__main__':
    unittest.main()    
