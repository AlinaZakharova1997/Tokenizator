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


class Context_Windows(object):
    """
    class Context_Windows
    @param positions: positions of tokens
    @param string: string representation of a token
    @param win_start: position where window starts
    @param win_end: position where window ends
    """

    def __init__(self,string,positions,win_start,win_end):

        self.string = string
        self.positions = positions
        self.win_start = win_start
        self.win_end = win_end
        

    def __eq__(self, window):

         return self.string == window.string and self.positions == window.positions and self.win_start == window.win_start and self.win_end == window.win_end
        
    def __repr__(self):
        
        return str(self.string) + ' ' + str(self.positions) + ' ' + str(self.win_start) + ' ' + str(self.win_end)
        
    position = Position_Plus('lnumber','start','end')
    @classmethod
    def get_window(cls,filename,position,win_size):
        """
        This function returns a context window of a given token's position 
        """
        if not isinstance(filename, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
        cls.tokenizator = Tokenizator()
        positions = []
        positions.append(position)
        win_end = 0
        win_start = 0
        string = ""
        str_num = position.lnumber
        my_file = open(filename)
        for lnumber,my_string in enumerate(my_file):
            if lnumber == str_num:
                string = my_string
                break
        
        for tok_num,token in enumerate (cls.tokenizator.token_gen(string[position.start:])):
            if tok_num==win_size:
                win_end=token.position+ len(token.s)
                break                               
        for tok_num,token in enumerate (cls.tokenizator.token_gen(string[position.end::-1])):

             if tok_num==win_size:
                win_start = token.position
                break                               
        return cls(string,positions,win_start,win_end)

if __name__ == '__main__':
    x=Context_Windows('string','positions','win_start','win_end')
    print(x.get_window('try.txt',Position_Plus(0,15,20),3))
