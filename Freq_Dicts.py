import tokenizator
from tokenizator import Tokenizator
from collections import OrderedDict

x = Tokenizator()
file = open('all(1).out')


#there are the lists where different POS will be contained
s_freq = []
pr_freq = []
v_freq = []

#tokenizes every line in the given file
for lnumber,line in enumerate(file):
    string = line
    for num,token in enumerate(x.token_gen(string)):
        if num == 7 and token.s == 's':
            lemma = string[3]
            s_freq.append(lemma)
            
        elif num == 7 and token.s =='pr':
            lemma = string[3]
            pr_freq.append(lemma)
            
        elif num == 7 and token.s =='v':
            lemma = string[3]
            v_freq.append(lemma)
            
print(s_freq)

s_freq_dict = {}
s_freq_dict_sorted = {}
for lemma in s_freq:
    lem_count = s_freq.count(lemma)
    s_freq_dict.setdefault(lemma,lem_count)
s_freq_dict_sorted = OrderedDict(sorted(s_freq_dict.items(), key=lambda t: t[0]))

pr_freq_dict = {}
pr_freq_dict_sorted = {}
for lemma in pr_freq:
    lem_count = pr_freq.count(lemma)
    pr_freq_dict.setdefault(lemma,lem_count)
pr_freq_dict_sorted = OrderedDict(sorted(pr_freq_dict.items(), key=lambda t: t[0]))    

v_freq_dict = {}
v_freq_dict_sorted = {}
for lemma in v_freq:
    lem_count = v_freq.count(lemma)
    v_freq_dict.setdefault(lemma,lem_count)
v_freq_dict_sorted = OrderedDict(sorted(v_freq_dict.items(), key=lambda t: t[0]))     
    
    
    
