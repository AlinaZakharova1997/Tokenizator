import codecs                         
from collections import namedtuple
from urllib.request import urlopen
import csv
from collections import OrderedDict
from lxml import html
import time

# search link for a word
word_search_link = 'http://search1.ruscorpora.ru/syntax-explain.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=1&level3=1&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&text=word-info&requestid=1553071332398&language=ru&source='
# tuple that contains information about word and the word itself
Word = namedtuple("Word", "word lemma part_of_speech grammar_structure")
Constructions = open('Constructions.csv', 'w')
Constructions.close()
PAUSE_AFTER_FAILURE = 3
MAX_RETRY = 3
def get_word_info(word: str, suff: str, s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict):
    '''
    This function gets information about a given word and makes frequency dictionaries
    for each part of speech (noun, preposition, verb)
    @param word: string containing a word
    @param suff: string containing search suffix to find a word
    @return: csv files with frequency dictionaries 
    '''
    print('getwordinfo')
    constr_str = ''
    parsed_url = html.parse(word_search_link + suff)
    info = parsed_url.xpath('//td[@class="value"]/text()')
    lemma = codecs.decode(info[0].encode('raw-unicode-escape'), 'cp1251').replace(' ', '').replace('\n(', '')
    params = codecs.decode(info[2].encode('raw-unicode-escape'), 'cp1251')
    pr_list = params.split(',\xa0')
    if params[0] == 's':
        s_freq_dict.setdefault(lemma, 0)
        s_freq_dict[lemma] += 1
        print(params[0])
    elif params[0] == 'pr' or params[0] == 'p':
        pr_freq_dict.setdefault(lemma, 0)
        pr_freq_dict[lemma] += 1
        print(params[0])
    elif params[0] == 'v' or params[0] == '3':
        v_freq_dict.setdefault(lemma, 0)
        v_freq_dict[lemma] += 1
        print(params[0])
    elif params[0] == 'adv'or params[0] == 'a':
        adv_freq_dict.setdefault(lemma, 0)
        adv_freq_dict[lemma] += 1
        print(params[0])
    else:
        print('Error! Tag not found!')
        print(params[0])
        print(word)
        
    pr_freq_dict_sorted = OrderedDict(sorted(pr_freq_dict.items(), key = lambda t: t[1], reverse=True))
    with open('Prep_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in pr_freq_dict_sorted.items():
            writer.writerow([key,value])
    s_freq_dict_sorted = OrderedDict(sorted(s_freq_dict.items(), key = lambda t: t[1],reverse=True))
    with open('Noun_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in s_freq_dict_sorted.items():
            writer.writerow([key,value])
    print('v_dict')        
    v_freq_dict_sorted = OrderedDict(sorted(v_freq_dict.items(), key = lambda t: t[1], reverse=True))
    with open('Verb_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in v_freq_dict_sorted.items():
            writer.writerow([key,value]) 
    adv_freq_dict_sorted = OrderedDict(sorted(adv_freq_dict.items(), key = lambda t: t[1], reverse=True))
    with open('Adverb_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in adv_freq_dict_sorted.items():
            writer.writerow([key,value])         
            
                                  
def search_highlighted(url: str, s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict):
    '''
    This function searches all highlighted words and makes constructions
    @param url: string adress of a searching query
    @return: csv file with constructions
    '''
    print('search')
    parsed_url = html.parse(url)
    constr_str = []
    for sent in parsed_url.xpath('//div[@class="content"]/ol/li/table/tr/td/ul/li'):
        constr = ''
        full_sent = sent.xpath('normalize-space(.)').split(' [', 1)[0]
        time.sleep(300) 
        for highlighted_word in sent.xpath('span[@class="b-wrd-expl g-em"]'):
            word = highlighted_word.xpath('text()')
            suff = highlighted_word.xpath('@explain')
            if len(word)==0 or len(suff)==0:
                print('No such word or suff')
            else:
                get_word_info(word[0], suff[0], s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict)
                constr+=word[0]+' '
        constr_str.append(constr)    
        print(constr)
        print('I got constr_str!')
        
    with open('Constructions.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for constr in constr_str:
            writer.writerow([constr])
        '''time.sleep(300)''' 
def req(main_link: str, pages: int):
    '''
    This function works with the search link and pushes input into the above functions 
    @param main_link: an url string adress
    @param pages: number of pages to work with
    '''
    s_freq_dict = {}
    pr_freq_dict = {}
    v_freq_dict = {}
    adv_freq_dict = {}
    print('req')
    for i in range(pages):
        try:
            for n_try in range(MAX_RETRY):
                all_highlighted = search_highlighted(main_link+'&p=%s' % i, s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict)
            break
        except Exception:
            time.sleep(PAUSE_AFTER_FAILURE)  
# this is the main link
req(
'http://search1.ruscorpora.ru/syntax.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=200&spp=200&spd=&text=lexgramm&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S%2C%E2%E8%ED&flags2=&parent3=2&level3=2&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&parent4=3&level4=3&min4=&max4=&link4=on&type4=&lex4=&gramm4=S&flags4=',
4)
# http://search1.ruscorpora.ru/syntax.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&text=lexgramm&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=2&level3=2&min3=&max3=&link3=on&type3=&lex3=&gramm3=%EF%F0%E8%F7&flags3=&parent4=3&level4=3&min4=&max4=&link4=on&type4=&lex4=&gramm4=ADV&flags4=
# http://search1.ruscorpora.ru/syntax.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&text=lexgramm&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=2&level3=2&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&parent4=3&level4=3&min4=&max4=&link4=on&type4=&lex4=&gramm4=S&flags4=


