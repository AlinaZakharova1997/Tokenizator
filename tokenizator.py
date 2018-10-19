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
    
    @staticmethod
    def tokens_type_definition(x):
       """
       This is a static method, which defines a type of a token
       @return: type of a token
       """
       if x.isalpha():
           tp = 'alpha'
       if x.isdigit():
           tp = 'digit'
       if x.isspace():
           tp = 'space'
       if unicodedata.category(x)[0] == 'P':
           tp = 'punct'
       return tp      
      
    def tokens_generator_plus_type (self, strim):
        """
        This is a generator.
        @param strim:strim is a text given
        @return: tokens from the given text plus their type
        """
        if  not isinstance(strim, str):
            raise ValueError('Input has an unappropriate type, it should be str')
        position=0
        for i,c in enumerate(strim):  # i is a number c is a letter
            # here it's just checks if types are equal
            if self.tokens_type_definition(c) != self.tokens_type_definition(strim[i-1]) and i>0:
                tp = self.tokens_type_definition(strim[i-1])
                s = strim[position:i]
                position = i
                t = Token_Type(s,tp)                        
                yield(t)
        # last if for the very last substring in strim        
        if self.tokens_type_definition(c):
            tp = self.tokens_type_definition(c)
            s = strim[position:i+1]
            t = Token_Type(s,tp)
            yield(t)
            
    def tokens_generator_plus_type_optimized (self, strim):
        """
        This is a generator.
        @param strim:strim is a text given
        @return: tokens from the given text plus their type
        """
        if  not isinstance(strim, str):
            raise ValueError('Input has an unappropriate type, it should be str')
        position=0
        tp_of_c=self.tokens_type_definition(strim[0])
        for i,c in enumerate(strim):  # i is a number c is a letter
            # here it's just checks if types are equal
            if self.tokens_type_definition(c) != tp_of_c and i>0:
                tp = self.tokens_type_definition(strim[i-1])
                tp_of_c = self.tokens_type_definition(c)
                s = strim[position:i]
                position = i
                t = Token_Type(s,tp)                        
                yield(t)    
        # last if for the very last substring in strim        
        if self.tokens_type_definition(c):
            tp = self.tokens_type_definition(c)
            s = strim[position:i+1]
            t = Token_Type(s,tp)
            yield(t)        
    
x=Tokenizator()
for i in x.tokens_generator(' Ф 12 !!! @ # Alina is a student)))'):
    print(i)


