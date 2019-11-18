import make_selection
import unittest

class TestMyCode(unittest.TestCase):
   
    def test_one(self):
        
        lists = [[('собака', 23,'noun'),('кот', 15,'noun'), ('девочка', 30,'noun')],
                 [('бегать', 20,'verb'),('быть', 45,'verb'), ('дискутировать', 3,'verb'), ('булдыжничать', 1,'verb')],
                 [('с', 10,'prep'),('в', 56,'prep')]]
        
        result = list(make_selection.lemma_generator(lists))
        cool = [('в','prep'),('быть','verb'),('девочка','noun'),('собака','noun'),('бегать','verb'),('кот','noun'),('с','prep'),('дискутировать','verb'),('булдыжничать', 1,'verb')]
        self.assertEqual(result, cool)


if __name__ == '__main__':
    unittest.main()    
