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
    
    @classmethod
    def get_united_window(window_A, window_B):
        '''
        This function checks if windows are crossing and unites them
        @param window_one: the first window in a pair
        @param window_two: the second window in a pair
        @return: united window or a message it was not to be done
        '''
        if not isinstance(window_A, Context_Window) or not isinstance(window_B, Context_Window):
            raise TypeError('Input has an unappropriate type!')
        if window_A.start < window_B.end and
        window_A.end > window_B.start:
            window_A.end == window_B.end
        return window_A
            
        else:
            s = 'These windows are not to be united'
            return s
        

if __name__ == '__main__':
    x = Context_Window('string','positions','win_start','win_end')
    print(x.get_window('try.txt', Position_Plus(0,16,18), 1))
