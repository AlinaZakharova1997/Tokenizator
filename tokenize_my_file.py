import csv
import nltk
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict

tokenizer = RegexpTokenizer(r'\w+')
file = open('all(1).out')


#there are the lists where different POS will be contained
s_freq = []
pr_freq = []
v_freq = []

#tokenizes every line in the given file
'''for lnumber,line in enumerate(file):
    string = line
    for num,token in enumerate(tokenizer.tokenize(string)):
        if num == 7 and token == 's':
            lemma = tokenizer.tokenize(string)   
            s_freq.append(lemma[3])
            
        elif num == 7 and token =='pr':
            lemma = tokenizer.tokenize(string) 
            pr_freq.append(lemma[3])
            
        elif num == 7 and token =='v':
            lemma = tokenizer.tokenize(string) 
            v_freq.append(lemma[3])'''

string = ''

'''for lnumber,line in enumerate(file):
    if(len(string)<3):
        line = tokenizer.tokenize(line)
        string += line[1]+' '
    
        
print(string) '''
for lnumber,line in enumerate(file):
    for num,token in enumerate(tokenizer.tokenize(line)):
        if num == 1 and len(string)<3:
            string+=token + ' '
    print(string)
    

'''s_freq_dict = {}
s_freq_dict_sorted = {}
for lemma in s_freq:
    lem_count = s_freq.count(lemma)
    s_freq_dict.setdefault(lemma,lem_count)
s_freq_dict_sorted = OrderedDict(sorted(s_freq_dict.items(), key = lambda t: t[1]))
with open('Noun_dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter= ';')
    for key, value in s_freq_dict_sorted.items():
       writer.writerow([key,value])

pr_freq_dict = {}
pr_freq_dict_sorted = {}
for lemma in pr_freq:
    lem_count = pr_freq.count(lemma)
    pr_freq_dict.setdefault(lemma,lem_count)
pr_freq_dict_sorted = OrderedDict(sorted(pr_freq_dict.items(), key = lambda t: t[1]))    
with open('Prep_dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter= ';')
    for key, value in pr_freq_dict_sorted.items():
       writer.writerow([key,value])
v_freq_dict = {}
v_freq_dict_sorted = {}
for lemma in v_freq:
    lem_count = v_freq.count(lemma)
    v_freq_dict.setdefault(lemma,lem_count)
v_freq_dict_sorted = OrderedDict(sorted(v_freq_dict.items(), key = lambda t: t[1]))    
with open('Verb_dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter= ';')
    for key, value in v_freq_dict_sorted.items():
       writer.writerow([key,value]) '''   
    
    
