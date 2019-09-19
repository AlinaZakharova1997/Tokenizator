
"""
Context_Windows
This module returns context windows for each query word
"""
import tokenizator
from tokenizator import Tokenizator
import indexer
from indexer import Indexer,Position_Plus
import re


# make a pattern for re.match()
PATTERN_RIGHT = re.compile(r'[.!?] [A-ZА-Я]') 
PATTERN_LEFT = re.compile(r'[A-ZА-Я] [.!?]')

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
            
        for tok_num,token in enumerate (cls.tokenizator.token_gen(string[:position.end][::-1])):
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
        if self.win_start < window_B.win_end and self.win_end > window_B.win_start and self.positions[0].lnumber == window_B.positions[0].lnumber:
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
        self.positions.extend(window_B.positions)
        

    def extend_window(self):
        '''
        This function extends a given window to sentence
        @return: an extended window
        ''' 
        to_right = self.string[self.win_end+1:]
        print(to_right, 'to right')
        to_left = self.string[:self.win_start+1][::-1]
        print(to_left, 'to left')
        left = PATTERN_LEFT.search(to_left)
        right = PATTERN_RIGHT.search(to_right)
        if right is not None:
            self.win_end += right.end()
            print(right, 'right')
        else:
            self.win_end = len(self.string)
        if left is not None:
            self.win_start =  self.win_start - left.start()-1
            print(left, 'left')
            print( self.win_start, ' self.win_start')
        else:
            self.win_start = 0
       
                

    def highlight_window(self):
        '''
        This function takes a substring of window string,
        which corresponds to the window size and highlights it 
        '''
        win_string = self.string[self.win_start:self.win_end]
        fin = '</b>'
        st = '<b>'
        for position in reversed(self.positions):
            end = position.end - self.win_start
            begin = position.start - self.win_start
            win_string_one = win_string[:end] + fin + win_string[end:]
            win_string = win_string_one[:begin] + st + win_string_one[begin:]
        return win_string


if __name__ == '__main__':
    window_A = Context_Window('string','positions','win_start','win_end')
    window_B = Context_Window('string','positions','win_start','win_end')
    window_X = window_A.get_window('test.txt', Position_Plus(0, 4, 20), 1)
    window_Y = window_B.get_window('test.txt', Position_Plus(0, 9, 30), 1)
    print(type(window_X))
    print(window_X.positions,'positions')
    print(window_X.win_start, 'start')
    '''window_X.get_united_window(window_Y)'''
    window_X.extend_window()
    print(window_X.positions,'positions')
    print(window_X.win_start, 'start')
   
   

