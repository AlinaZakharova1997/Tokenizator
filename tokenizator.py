"""
Tokenizator
This module performs the morphological analyses of a text and extracts tokens.
Tokens here are words or letters
As a result it returns a list of tokens
and a position of the first element of each token.
"""
class Token(object):
    """
    Class of tokens taken from a given text
    """
    def __init__(self,position,s):
        """
        Consrtuctor for token.
        @param self: self is an odject(here:token) with attributes
        @param position: position is an index of the first element of token
        @param s: s is a string view of a token
        @return: token
        """
        self.position=position  
        self.s=s
        
    def __repr__(self):
        """
        The way the programm returns the final result.
        """
        return self.s+'_'+str(self.position)

    
class Tokenizator(object):
    """
    Class that returns tokens
    """
    def tokenize(self,strim):
        """
        This is a function.
        @param strim:strim is a text given
        @return: a list of tokens from the given text
        """
        if  not isinstance(strim,str):
            raise ValueError('Input has an unappropriate type, it should be str')
        tokensback=[]
        for i,c in enumerate(strim):  # i is a number c is a letter
            # here it's just shifts to the position where token starts
            if c.isalpha() and (not strim[i-1].isalpha() or i==0):   
                position=i
            # here it takes section from the beginning to the end of the token
            # and adds token to the list
            if not c.isalpha()and i>0 and strim[i-1].isalpha():   
                s=strim[position:i]
                # constructor for token is working here
                t=Token(position,s)                        
                tokensback.append(t)
        # last if for the very last substring in strim        
        if c.isalpha():                   
            s=strim[position:i+1]
            t=Token(position,s)
            tokensback.append(t)
        return tokensback
    
    def tokens_generator(self, strim):
        """
        This is a generator.
        @param strim:strim is a text given
        @return: tokens from the given text
        """
        if  not isinstance(strim, str):
            raise ValueError('Input has an unappropriate type, it should be str')
        for i,c in enumerate(strim):  # i is a number c is a letter
            # here it's just shifts to the position where token starts
            if c.isalpha() and (not strim[i-1].isalpha() or i==0):   
                position = i
            # here it takes section from the beginning to the end of the token
            # and adds token to the list
            if not c.isalpha()and i>0 and strim[i-1].isalpha():   
                s = strim[position:i]
                # constructor for token is working here
                t=  Token(position, s)                        
                yield(t)
        # last if for the very last substring in strim        
        if c.isalpha():                   
            s=strim[position:i+1]
            t=Token(position, s)
            yield(t)
    
  
    
x=Tokenizator()
for i in x.tokens_generator(' Ф 12 !!! @ # Alina is a student)))'):
    print(i)


