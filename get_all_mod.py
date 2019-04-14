import codecs                         
from collections import namedtuple
from urllib.request import urlopen
import csv
from collections import OrderedDict
from lxml import html




# search link for a word
word_search_link = 'http://search1.ruscorpora.ru/syntax-explain.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=1&level3=1&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&text=word-info&requestid=1553071332398&language=ru&source='
# tuple that contains information about word and the word itself
Word = namedtuple("Word", "word lemma part_of_speech grammar_structure")

def word_to_str(word: Word):
    return 'word : {0}, lemma : {1}, part of speech : {2}, params : {3}'.format(word.word, word.lemma,
                                                                                word.part_of_speech,
                                                                                word.grammar_structure)

def get_word_info(word: str, suff: str, tags: list) -> Word:
    '''
    This function gets information about a given word and makes frequency dictionaries
    for each part of speech (noun, preposition, verb)
    @param word: string containing a word
    @param suff: string containing search suffix to find a word
    @param tags: list of word's  grammar tags
    @return: csv files with frequency dictionaries 
    '''
    print('getwordinfo')
    s_freq_dict = {}
    pr_freq_dict = {}
    v_freq_dict = {}
    parsed_url = html.parse(word_search_link + suff)
    info = parsed_url.xpath('//td[@class="value"]/text()')
    lemma = codecs.decode(info[0].encode('raw-unicode-escape'), 'cp1251').replace(' ', '').replace('\n(', '')
    params = codecs.decode(info[2].encode('raw-unicode-escape'), 'cp1251')
    pr_list = params.split(',\xa0')
    for tag in tags:
        try:
            pr_list.remove(tag)
            word = Word(word, lemma, tag, pr_list)
            if tag == 's':
                s_freq_dict.setdefault(lemma, 0)
                s_freq_dict[lemma] += 1
            if tag == 'pr':
                pr_freq_dict.setdefault(lemma, 0)
                pr_freq_dict[lemma] += 1
            if tag == 'v':
                v_freq_dict.setdefault(lemma, 0)
                v_freq_dict[lemma] += 1

        except ValueError:
               continue
    
    s_freq_dict_sorted = {}
    pr_freq_dict_sorted = {}
    v_freq_dict_sorted = {}  
    s_freq_dict_sorted = OrderedDict(sorted(s_freq_dict.items(), key = lambda t: t[1]))
    with open('Noun_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in s_freq_dict_sorted.items():
            writer.writerow([key,value])
    pr_freq_dict_sorted = OrderedDict(sorted(pr_freq_dict.items(), key = lambda t: t[1]))        
    with open('Prep_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in pr_freq_dict_sorted.items():
            writer.writerow([key,value])
    v_freq_dict_sorted = OrderedDict(sorted(v_freq_dict.items(), key = lambda t: t[1]))        
    with open('Verb_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in v_freq_dict_sorted.items():
            writer.writerow([key,value])     
        
def search_highlighted(url: str, tags: "лист строк"):
    '''
    This function searches all highlighted words and makes constructions
    @param url: string adress of a searching query
    @param tags: a list of POS tags
    @return: csv file with constructions
    '''
    print('search')
    parsed_url = html.parse(url)
    print('I parsed url')
    for sent in parsed_url.xpath('//div[@class="content"]/ol/li/table/tr/td/ul/li'):
        print(sent)
        print('I parsed sent')
        sent = parsed_url.xpath('text()')
        full_sent = sent.xpath('normalize-space(.)').split(' [', 1)[0]
        constr = []
        for highlighted_word in sent.xpath('//span[@class="b-wrd-expl g-em"]'):
            word = highlighted_word.xpath('text()')
            suff = highlighted_word.xpath('@explain')
            get_word_info(word[0], suff[0], tags)
            print(get_word_info(word[0], suff[0], tags))
            print('hello')
            constr.append(word[0])
        constr_str = ' '.join(constr)     
        with open('Constructions.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter= ' ')
            for constr in constr_str:
                writer.writerow([constr, full_sent])            
        print('I found constr!')         
                    
def req(main_link: str, pages: int, tags: list):
    '''
    This function works with the search link and pushes input into the above functions 
    @param main_link: an url string adress
    @param pages: number of pages to work with
    @param tags: a list of POS tags
    '''
    print('req')
    for i in range(pages):
        all_highlighted = search_highlighted(main_link + str(i), tags)

# this is the main link
req(
    'http://search1.ruscorpora.ru/syntax.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&text=lexgramm&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=2&level3=2&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&parent4=3&level4=3&min4=&max4=&link4=on&type4=&lex4=&gramm4=S&flags4=',
2, ['v', 's', 'pr'])
