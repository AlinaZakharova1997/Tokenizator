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
        @param filename: a name of a file
        @param position: object of Position_Plus, contains position of a token in file
        @param win_size: size of a context window
        """
        if not isinstance(filename, str) or not isinstance(win_size, int) or not type(position) is Position_Plus:
            raise TypeError('Input has an unappropriate type!')
        positions = []
        positions.append(position)
        win_end = 0
        win_start = 0
        string = None
        str_num = position.lnumber
        my_file = open(filename)
        # searhes for string with a given number
        for lnumber, my_string in enumerate(my_file):
            if lnumber == str_num:
                string = my_string
                break
        # if there is no such string - raises an error    
        if string is None:
            my_file.close() 
            raise IndexError('This string was not found!')
            
        # here it moves on the string from token start 
        # and breaks when finds needed number of tokens
        for tok_num, token in enumerate(cls.tokenizator.token_gen(string[position.start:])):
            if tok_num == win_size:
                break
        # counts window end   
        win_end = token.position + len(token.s) + position.start
        
        # here it moves on the reversed string
        # from position.end - 1 to exclude space after the token end
        # and breaks when finds needed number of tokens
        for tok_num, token in enumerate(cls.tokenizator.token_gen(string[position.end-1::-1])):
            if tok_num == win_size:
                break
        # counts window start    
        win_start = position.end - token.position - len(token.s)
        
        my_file.close()    
        return cls(string, positions, win_start, win_end)

if __name__ == '__main__':
    x = Context_Window('string','positions','win_start','win_end')
    print(x.get_window('try.txt', Position_Plus(0,16,18), 1))
