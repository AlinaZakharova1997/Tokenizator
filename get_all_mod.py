# для кодировок
import codecs
# для работы с тьюплами
from collections import namedtuple
# определяет функции и классы, которые помогают открывать URL
from urllib.request import urlopen
# для работы с csv
import csv
# для сортировки словарей
from collections import OrderedDict
from lxml import html
# модуль для работы со временем 
import time
# множество функций для работы с операционной системой
import os
# предоставляет классы для обработки времени и даты разными способами
import datetime
# для декодирования суффикса
from urllib.parse import unquote

if __name__ == '__main__':
   ''' # создаю файл для конструкций 
    Constructions = open('Constructions.txt', 'w')
    # потом я его открою на дозапись и буду по очереди дозаписывать все конструкции
    Constructions.close()'''
# это ссылка для поиска слова
word_search_link = 'http://processing.ruscorpora.ru/search-explan.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=2&level3=2&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&text=word-info&requestid=1569187164845&language=ru&source='
# это тьюпл для хранения информации о слове и самого слова
Word = namedtuple("Word", "word lemma part_of_speech grammar_structure")
# глобальный словарь, играющий роль промежуточного хранилища 
global_dict = {}
# пауза отдыха после ошибки 
PAUSE_AFTER_FAILURE = 8
# максимально количество попыток что то сделать  
MAX_RETRY = 3
# файл, куда пишется вся выдача, чтобы не перегрузить консольку или IDLE 
log_file = open('ruscorpora.log', 'w')
           
def log(*args):
    '''
    This function writes information in file and also prints it on the screen
    @param *args: arguments the function takes; the number of arguments is not limited
    ''' 
    log_file.write(' '.join(str(arg) for arg in args))
    log_file.write('\n')
    log_file.flush()
    '''print(*args)'''
    
'''def get_lemma_and_params(suff):
    # это для старой версии корпуса
    This function gets lemma and params with gram info
    @param suff:string containing search suffix to find a word
    @return: lemma and params
    
    parsed_url = html.parse(word_search_link + suff)
    info = parsed_url.xpath('//td[@class="value"]/text()')
    if len(info) < 2:
        try:
            log('Failed to find lemma and params, sorry:(')
            log(html.tostring(parsed_url))
        except Exception:
            raise
    else:
        try:
            lemma = codecs.decode(info[0].encode('raw-unicode-escape'), 'cp1251').replace(' ', '').replace('\n(', '')
            log(lemma, 'lemma')
            params = codecs.decode(info[2].encode('raw-unicode-escape'), 'cp1251')
            log(params, 'params')
            return lemma, params
        except IndexError:
            log('Bad IndexError happened!') '''

def get_lemma_and_params(suff):
    # достаю лемму и грам параметры из suff
    '''log('I am in get lemma and params')'''
    # парсю ссылку на слово + suff
    parsed_url = html.parse(word_search_link + suff)
    # нахожу и запоминаю нужную информацию о слове, она там вся сразу
    # и существует в виде двух элементов леммы и параметров 
    info = parsed_url.xpath('//td[@class="value"]/text()')
    '''log(info,'info.xpath!')'''
    # если их точно два, вытаскиваю их по очереди, иначе - ошибка
    if len(info) < 2:
        try:
            log('Failed to find lemma and params, sorry:(')
            log(html.tostring(parsed_url))
        except Exception:
            raise
    else:
        # тащу и декодирую лемму
        lemma = bytes([ord(c) for c in info[0]]).decode('utf-8').replace(' ', '').replace('\n(', '')
        '''log(lemma, 'lemma')'''
        # тащу и декодирую все грамматические характеристики 
        params = bytes([ord(c) for c in info[1]]).decode('utf-8').replace(' ', '').replace('\n(', '')
        log(params, 'params')
        return lemma, params
        '''except IndexError:
            log('Bad IndexError happened!')'''
          
            
          
def get_word_info(word, suff, s_freq_dict, pr_freq_dict, v_freq_dict, a_freq_dict, adv_freq_dict):
    '''
    This function gets information about a given word and makes frequency dictionaries
    for each part of speech (noun, preposition, verb)
    @param word: string containing a word
    @param suff: string containing search suffix to find a word
    @return: csv files with frequency dictionaries 
    '''
    log('I am in word info!')
    constr_str = ''
    '''log(word,"word")
    log(suff, "suff")'''
    # начинаю пытаться создавать частотные словари
    try:
        # если suff отсутствует, добавляю в глобальный словарь
        if suff not in global_dict:
            lemma, params = get_lemma_and_params(suff)
            global_dict[suff] = (lemma, params)
        else:
            # иначе достаю его из этого словаря
            # это общий словарь, промежуточный, в нем удобнее хранить данные пока я с ними вожусь
            lemma, params = global_dict[suff]
        # это все грам параметры слова со всеми характеристиками и еще лемма   
        pr_set = set(params.split(",\xa0") )
        # ищу нужный тег и по нему добавляю лемму в соответствующий частотник, не забывая запоминать его количество
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

        elif 'a' in pr_set:
           a_freq_dict.setdefault(lemma, 0)
           a_freq_dict[lemma] += 1
           
        else:
            # на случай если тег не найден
            log('Error! Tag not found!')
            log(word)
    # поднимаю ошибку. здесь так же возникает OSError, я ее обнаружила, когда качала запрос 5   
    except OSError:
       log('BAD OSError happened!')
    except AssertionError:
       log('AssertionError')
   
def search_highlighted(url, s_freq_dict, pr_freq_dict, v_freq_dict, a_freq_dict, constr_dict, adv_freq_dict):
    '''
    This function searches all highlighted words and makes constructions
    and forms constr_dict={'construction':[lemma0,lemma1,lemma2,lemma3]}
    @param url: string adress of a searching query
    '''
    log('search')
    # парсю ссылку
    parsed_url = html.parse(url)
    log('I parsed url')
    # создаю список конструкций и открываю файл на дозапись
    constr_str = []
    '''Constructions = open('Constructions.txt', 'a')'''
    log(len(parsed_url.xpath('//div[@class="content"]/ol/li/table/tr/td/ul/li')))
    # для каждого предложения из контента, те из документа на странице начинаю искать выделенные слова
    for num, sent in enumerate (parsed_url.xpath('//div[@class="content"]/ol/li/table/tr/td/ul/li')):
        # пустая сторока куда буду плюсовать слова в конструкцию
        constr = ''
        # список всех лемм конструкции
        lemmas = []
        log(num, 'sent_num')
        # слежу за временем обработки предложения
        log(datetime.datetime.now().isoformat())
        # нахожу полное предложение
        full_sent = sent.xpath('normalize-space(.)').split(' [', 1)[0]
        # в нем нахожу выделенное слово
        for highlighted_word in sent.xpath('span[@class="b-wrd-expl g-em"]'):
            # отдыхаю, чтобы не перетрудиться
            time.sleep(3)
            '''log('I got to the word!')'''
            # достаю слово в виде текста
            word = highlighted_word.xpath('text()')
            word = ''.join(word)
            # декодирую в ютф-8
            word = bytes([ord(c) for c in word]).decode('utf-8')
            '''log(word, "word_decoded")'''
            # нахожу грамматические характеристики слова, они же suff
            suff = highlighted_word.xpath('@explain')
            # вытаскиваю суффикс
            lem_suff = suff[0] # %D0%B2%7C5%7C%D0%B2
            # декодирую суффикс
            lem_suff = unquote(lem_suff)
            '''print(type(lem_suff),'type')
            print(lem_suff,'suff')'''
            # сплит вернет список, где 1 элемент это моя лемма
            lemma = lem_suff.split('|')[0]
            log(lemma,"lemma")
            lemmas.append(lemma)
            # если то, что я нашла не пустой результат поиска, передаю
            # грамматические характеристики и пустые словари в функцию поиска нужных характеристик(частеречных тегов)
            if len(word)==0 or len(suff)==0:
                log('No such word or suff')
            else:
                get_word_info(word[0], suff[0], s_freq_dict, pr_freq_dict, v_freq_dict, a_freq_dict, adv_freq_dict)
                # не забываю отдыхать
                time.sleep(3)
                # собираю слова в конструкцию
                constr+=word+' '
        log(constr, "CONSTR!")
        log (lemmas, "Lemmas!")
        '''print(constr)'''
        # добавляю в словарь конструкцию и список ее лемм
        constr_dict.setdefault(constr, []).append(lemmas)
        '''# добавляю констрцукцию в результирующий файл
        Constructions.write(constr + '\n')'''
    '''# не забываю закрыть файл, чтобы потом снова открыть и дозаписать новую конструкцию без утраты старой    
    Constructions.close()'''   
    
def req(main_link, pages):
    '''
    This function works with the search link and pushes input into the above functions 
    @param main_link: an url string adress
    @param pages: number of pages to work with
    '''
    s_freq_dict = {}
    pr_freq_dict = {}
    v_freq_dict = {}
    a_freq_dict = {}
    adv_freq_dict = {}
    constr_dict = {}
    log('req')
    # листаю страницы выдачи, запоминаю их номера
    for i in range(pages):
        log('I got page %s'%i)
        #  делаю нужное количество попыток соединения с сайтом
        for n_try in range(MAX_RETRY):
            try:
                #  если получилось, пытаюсь найти все выделенные цветом слова - они мои будущие конструкции
                '''log('I try to search highlighted!')'''
                all_highlighted = search_highlighted(main_link+'&p=%s' % i, s_freq_dict, pr_freq_dict, v_freq_dict, a_freq_dict, constr_dict, adv_freq_dict)
                '''log('I got the link!')'''
                break
            # добавила после ошибки в 6 запросе
            # программа доработала до функции get_word_info
            # в лог файл напечаталась лемма и сообщение 'I am in word info!'
            # http://processing.ruscorpora.ru/search-explan.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=2&level3=2&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&text=word-info&requestid=1569187164845&language=ru&source=%D0%BE%D1%82%D1%82%D0%BE%D0%BA%7C53%7C%D0%BE%D1%82%D1%82%D0%BE%D0%BA
            # эта ссылка была помечена как ошибка, ссылка рабочая. Сообщение: не удалось загрузить внешний элемент
            except OSError:
                raise
                # если что то пошло не так, поднимаю ошибку и делаю паузу
                time.sleep(PAUSE_AFTER_FAILURE)
                log('BAD OSError happened!')
                
# тут я сортирую и пишу в результирующие файлы свои частотные словарики                
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
    constr_dict_sorted = OrderedDict(sorted(constr_dict.items(), key = lambda t: t[1], reverse=True))
    with open('CONSTR_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in constr_dict_sorted.items():
            writer.writerow([key,value])         
    adv_freq_dict_sorted = OrderedDict(sorted(adv_freq_dict.items(), key = lambda t: t[1], reverse=True))
    with open('Adverb_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in adv_freq_dict_sorted.items():
            writer.writerow([key,value])
    a_freq_dict_sorted = OrderedDict(sorted(a_freq_dict.items(), key = lambda t: t[1], reverse=True))
    with open('Adjective_dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in a_freq_dict_sorted.items():
            writer.writerow([key,value])
# это моя ссылка поиска и количество страниц выдачи      
req('http://processing.ruscorpora.ru/search.xml?sort=i_grtagging&out=normal&dpp=100&spd=100&seed=29547&text=lexgramm&mysent=&level1=0&level2=1&level3=2&level4=3&type4=&flags2=&type3=&type2=&flags4=&flags1=&flags3=&mysize=&mysentsize=&simple=1&env=alpha&parent2=1&link4=on&link3=on&link2=on&gramm4=S&gramm1=S&gramm2=S&gramm3=PR&min2=1&min3=1&min4=1&lang=ru&lex4=&lex1=&lex3=&max2=&max3=&lex2=&mycorp=&max4=&notag=1&parent4=3&parent3=2&mode=syntax&parent1=0'
    ,7)
