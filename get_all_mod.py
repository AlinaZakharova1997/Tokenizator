import codecs
from collections import namedtuple
from urllib.request import urlopen
import csv
from collections import OrderedDict
from lxml import html
import time
import os
import datetime

if __name__ == '__main__':
    
    Constructions = open('Constructions.txt', 'w')
    Constructions.close()           
# search link for a word
word_search_link = 'http://search1.ruscorpora.ru/syntax-explain.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=1&level3=1&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&text=word-info&requestid=1553071332398&language=ru&source='
# tuple that contains information about word and the word itself
Word = namedtuple("Word", "word lemma part_of_speech grammar_structure")
global_dict = {}
PAUSE_AFTER_FAILURE = 3
MAX_RETRY = 3
log_file = open('ruscorpora.log', 'w')
           
def log(*args):
    log_file.write(' '.join(str(arg) for arg in args))
    log_file.write('\n')
    log_file.flush()
    print(*args)
    
def get_lemma_and_params(suff):
    '''
    This function gets lemma and params with gram info
    @param suff:string containing search suffix to find a word
    @return: lemma and params
    ''' 
    parsed_url = html.parse(word_search_link + suff)
    info = parsed_url.xpath('//td[@class="value"]/text()')
    if len(info) > 0:
        try:
            lemma = codecs.decode(info[0].encode('raw-unicode-escape'), 'cp1251').replace(' ', '').replace('\n(', '') 
            params = codecs.decode(info[2].encode('raw-unicode-escape'), 'cp1251')
            return lemma, params
        except IndexError:
            log('Bad IndexError happened!')
    else:
        log('Failed to find lemma and params, sorry:(')
          
def get_word_info(word, suff, s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict):
    '''
    This function gets information about a given word and makes frequency dictionaries
    for each part of speech (noun, preposition, verb)
    @param word: string containing a word
    @param suff: string containing search suffix to find a word
    @return: csv files with frequency dictionaries 
    '''
    constr_str = ''
    try:
        if suff not in global_dict:
            lemma, params = get_lemma_and_params(suff)
            global_dict[suff] = (lemma, params)
        else:
            lemma, params = global_dict[suff]
        pr_set = set(params.split(",\xa0") )
        if  's' in pr_set :
            s_freq_dict.setdefault(lemma, 0)
            s_freq_dict[lemma] += 1
            
        
        elif  'pr' in pr_set:
            pr_freq_dict.setdefault(lemma, 0)
            pr_freq_dict[lemma] += 1
           
      
        elif 'v' in pr_set:
            v_freq_dict.setdefault(lemma, 0)
            v_freq_dict[lemma] += 1
            
       
        elif 'adv'in pr_set:
            adv_freq_dict.setdefault(lemma, 0)
            adv_freq_dict[lemma] += 1
            
        
        else:
            log('Error! Tag not found!')
            log(word)
        
    except AssertionError:
       log('AssertionError')    
   
def search_highlighted(url, s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict):
    '''
    This function searches all highlighted words and makes constructions
    @param url: string adress of a searching query
    @return: csv file with constructions
    '''
    log('search')
    parsed_url = html.parse(url)
    constr_str = []
    Constructions = open('Constructions.txt', 'a')
    '''/html/body/div[4]/ol/li[1]/table/tbody/tr/td/ul/li[1]
    document.querySelector('body > div.content > ol > li:nth-child(1) > table > tbody > tr > td > ul > li:nth-child(1) > span:nth-child(8)')
    '''
    log(len(parsed_url.xpath('//div[@class="content"]/ol/li/table/tr/td/ul/li'))) 
    for num, sent in enumerate (parsed_url.xpath('//div[@class="content"]/ol/li/table/tr/td/ul/li')):
        constr = ''
        log(num, 'sent_num')
        log(datetime.datetime.now().isoformat())
        full_sent = sent.xpath('normalize-space(.)').split(' [', 1)[0]
        for highlighted_word in sent.xpath('span[@class="b-wrd-expl g-em"]'):
            word = highlighted_word.xpath('text()')
            suff = highlighted_word.xpath('@explain')
            if len(word)==0 or len(suff)==0:
                log('No such word or suff')
            else:
                get_word_info(word[0], suff[0], s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict)
                constr+=word[0]+' '
        log(constr)
        Constructions.write(constr + '\n')
    Constructions.close()   
    
def req(main_link, pages):
    '''
    This function works with the search link and pushes input into the above functions 
    @param main_link: an url string adress
    @param pages: number of pages to work with
    '''
    s_freq_dict = {}
    pr_freq_dict = {}
    v_freq_dict = {}
    adv_freq_dict = {}
    log('req')
    for i in range(pages):
        log('I got page %s'%i)
        for n_try in range(MAX_RETRY):
            try:
                all_highlighted = search_highlighted(main_link+'&p=%s' % i, s_freq_dict, pr_freq_dict, v_freq_dict, adv_freq_dict)
                break
            except OSError:
                time.sleep(PAUSE_AFTER_FAILURE)
                log('BAD OSError happened!')
              
                
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
    
    
req('http://search1.ruscorpora.ru/syntax.xml?out=normal&kwsz=4&dpp=50&spd=100&spp=100&seed=24208&env=alpha&mycorp=&mysent=&mysize=&mysentsize=&text=lexgramm&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=1&level3=1&min3=1&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&parent4=3&level4=2&min4=1&max4=&link4=on&type4=&lex4=&gramm4=S&flags4=',
    13)                    
