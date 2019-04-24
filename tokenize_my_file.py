import csv
import nltk
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict
from collections import Counter

tokenizer = RegexpTokenizer(r'\w+')
file = open('all.out')


#there are the lists where different POS will be contained
s_freq = []
pr_freq = []
v_freq = []
s_freq_dict = {}
#tokenizes every line in the given file
for lnumber,line in enumerate(file):
    string = line
    for num,token in enumerate(tokenizer.tokenize(string)):
        if num == 7 and token == 's':
            lemma = tokenizer.tokenize(string)
            s_freq_dict.setdefault(lemma[3], 0)
            s_freq_dict[lemma[3]] += 1
            
            
        elif num == 7 and token =='pr':
            lemma = tokenizer.tokenize(string) 
            pr_freq.append(lemma[3])
            
        elif num == 7 and token =='v':
            lemma = tokenizer.tokenize(string) 
            v_freq.append(lemma[3])

for k,l in s_freq_dict.items():
    print(k,l)
'''html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc,"lxml")
    print(soup.body.div)'''
    
    '''print(parsed_url.xpath('//html/body/div[3]/ol/li[1]/table/tbody/tr/td/ul/li[1]'))'''
    '''/html/body/div[3]/ol/li[1]/table/tbody/tr/td/ul/li[2]
    '/html/body/div[3]/ol/li[{}]/table/tbody/tr/td/ul/li[{}]'.format(document, sentence)
    /html/body/div[3]/ol/li[9]/table/tbody/tr/td/ul/li[1]/span[1]
    /html/body/div[3]/ol/li[10]/table/tbody/tr/td/ul/li[1]'''
'''##    for document in range(1,11):
##        for sentence in :
    for sent in parsed_url.xpath('/html/body/div[3]/ol/li[{}]/table/tbody/tr/td/ul/li[{}]'.format(document, sentence)):
        sentence = sent.xpath('text()')
        string = ''
        i = 0'''
            
'''s_freq_dict = Counter(s_freq)
with open('Noun_count.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for k,l in sorted([(j,i) for i,j in s_freq_dict.items()], reverse=True):
            writer.writerow([l,k])'''

'''s_freq_dict = dict(Counter(s_freq))
v_freq_dict = dict(Counter(v_freq))
pr_freq_dict = dict(Counter(pr_freq))'''
  '''s_freq_dict = Counter(s)
    with open('Noun_count.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for k,l in sorted([(j,i) for i,j in s_freq_dict.items()], reverse=True):
            writer.writerow([l,k])
    pr_freq_dict = Counter(pr)
    with open('Prep_count.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for k,l in sorted([(j,i) for i,j in pr_freq_dict.items()], reverse=True):
            writer.writerow([l,k])
    v_freq_dict = Counter(v)
    with open('Verb_count.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for k,l in sorted([(j,i) for i,j in v_freq_dict.items()], reverse=True):
            writer.writerow([l,k])'''
            

'''s_freq_dict_sorted = {}
for lemma in s_freq:
    s_freq_dict_sorted = OrderedDict(sorted(s_freq_dict.items(), key = lambda t: t[1]))
    with open('Noun_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in s_freq_dict_sorted.items():
            writer.writerow([key,value])

pr_freq_dict_sorted = {}
for lemma in pr_freq:
    pr_freq_dict_sorted = OrderedDict(sorted(pr_freq_dict.items(), key = lambda t: t[1]))
    with open('Prep_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in pr_freq_dict_sorted.items():
            writer.writerow([key,value])
       
v_freq_dict_sorted = {}
for lemma in v_freq:
    v_freq_dict_sorted = OrderedDict(sorted(v_freq_dict.items(), key = lambda t: t[1]))
    with open('Verb_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in v_freq_dict_sorted.items():
            writer.writerow([key,value])  '''
    
    
