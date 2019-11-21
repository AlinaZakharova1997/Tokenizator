import make_selection
import unittest

class TestMyCode(unittest.TestCase):
   
    def test_one(self):
        
        lists = [[('девочка', 30,'noun'),('собака', 23,'noun'),('кот', 15,'noun')],
                 [('быть', 45,'verb'),('бегать', 20,'verb'),('дискутировать', 3,'verb'), ('булдыжничать', 1,'verb')],
                 [('в', 56,'prep'),('с', 10,'prep')]]
        
        result = list(make_selection.lemma_generator(lists))
        cool = [('в','prep'),('быть','verb'),('девочка','noun'),('собака','noun'),('бегать','verb'),('кот','noun'),('с','prep'),('дискутировать','verb'),('булдыжничать','verb')]
        self.assertEqual(result, cool)


if __name__ == '__main__':
    unittest.main()    
