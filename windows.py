
"""
Context_Windows
This module returns context windows for each query word
"""
import tokenizator
from tokenizator import Tokenizator
import search
from search import SearchEngine
import indexer
from indexer import Indexer,Position_Plus


class Context_Window(object):
    """
    class Context_Window 
    """
    tokenizator = Tokenizator()
    
    def __init__(self, string, positions, win_start, win_end):
        """
        Constructor of a context window
        @param positions: positions of tokens
        @param string: string representation of a token
        @param win_start: position where window starts
        @param win_end: position where window ends
        """

        self.string = string
        self.positions = positions
        self.win_start = win_start
        self.win_end = win_end
        
        

    def __eq__(self, window):

         return self.string == window.string and self.positions == window.positions and self.win_start == window.win_start and self.win_end == window.win_end
        
    def __repr__(self):
        
        return str(self.string) + ' ' + str(self.positions) + ' ' + str(self.win_start) + ' ' + str(self.win_end)
        
    @classmethod
    def get_window(cls, filename, position, win_size):
        """
        This function returns a context window of a given token's position
        @param filename: a name of a file where token is to be found
        @param position: a position of a token
        @param win_size: desirable size of the context window
        @return: a context window
        """
        if not isinstance(filename, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
        positions = []
        positions.append(position)
        win_end = 0
        win_start = 0
        string = None
        str_num = position.lnumber
        my_file = open(filename)
        for lnumber,my_string in enumerate(my_file):
            if lnumber == str_num:
                string = my_string
                break
            
        if string == None:
            my_file.close() 
            raise TypeError('This string was not found!')
            
        for tok_num,token in enumerate (cls.tokenizator.token_gen(string[position.start:])):
            if tok_num == 0:
                win_end = position.end
            if tok_num == win_size:
                win_end = token.position + len(token.s) + position.start
                break
            
        for tok_num,token in enumerate (cls.tokenizator.token_gen(string[position.end::-1])):
            if tok_num == win_size:
                win_start = position.end - token.position - len(token.s)
                break
        my_file.close()    
        return cls(string, positions, win_start, win_end)
    
    def is_crossed(self, window_B):
        '''
        This function checks if windows are crossed
        @param window_B: the second window
        @return: True or False
        '''
        if not isinstance(window_B, Context_Window):
            raise TypeError('Input has an unappropriate type!')
        if self.win_start < window_B.win_end and self.win_end > window_B.win_start:
            return True
        else:
            return False
        
    def get_united_window(self, window_B):
        
        '''
        This function unites two windows
        @param window_B: the second window 
        '''
        
        if not isinstance(window_B, Context_Window):
            raise TypeError('Input has an unappropriate type!')
        
        self.win_end = window_B.win_end
        self.positions.append(window_B.positions)
        
    def unite_all(self,dictionary,win_size):
       '''
       This function unites context windows
       @param dictionary: input dictionary filename:Positions
       @param win_size: a size of a context window
       @return: a dictionary filename:Context Windows
       '''
       if not isinstance(dictionary, dict) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
      
       output_dict = {}
       win_array = []
       # value is an array of positions
       for key,value in dictionary.items():
           pos_array = value
           # for each position in values get window()
           for pos in pos_array:
               window = self.get_window(key, pos, win_size)
               win_array.append(window)
           # add key and win_array into output_dict    
           output_dict.setdefault(key, win_array)
           
       i = 0
       for key, win_array in output_dict.items():
           while i < len(win_array)-1:
               if win_array[i].is_crossed(win_array[i+1]):
                   win_array[i].get_united_window(win_array[i+1])
                   win_array.remove(win_array[i+1])
               else:
                   i+=1

       return output_dict            
                   
               
if __name__ == '__main__':
    window_A = Context_Window('string','positions','win_start','win_end')
    window_B = Context_Window('string','positions','win_start','win_end')
    window_X = window_A.get_window('test.txt', Position_Plus(0, 4, 20), 1)
    window_Y = window_B.get_window('test.txt', Position_Plus(0, 9, 30), 1)
    window_X.get_united_window(window_Y)
