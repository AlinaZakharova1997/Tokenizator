"""
Context_Windows
This module returns context windows for each query word
"""
import search
from search import SearchEngine


class Context_Windows(object):
    """
    class Context_Windows
    @param positions: positions of tokens
    @param string: string representation of a token 
    """

    def __init__(self,string,positions):

        self.positions = positions
        self.string = string
        

    def __repr__(self):
        
        return self.string


    def get_window(self,tokens,win_size):
        
        if not isinstance(tokens, str) or not isinstance(win_size, int):
            raise TypeError('Input has an unappropriate type!')
        
        for token in token_gen(tokens):
            st = ''
            i = 0
            string_right=''
            string_right += token.s   
            for dikt in get_dict_many_tokens(token):
                pos = dikt.values()[i]
                st = pos.lnumber 
                for tok in token_gen(st):
                    size = 0
                    pos_right = token.pos.end
                    pos_left = token.pos.start
                    while(size < win_size*2):
                        if tok.pos.start == pos_right+1:
                            string_right += tok.s
                        pos_right = tok.pos.end
                        if tok.pos.end == pos_left-1:
                            string_left+=tok.s
                        pos_left = tok.pos.start    
                    string = string_left+ string_right               
            positions+=pos
            i += 1
            window = Context_Windows(string,positions)
            return window

            
        
