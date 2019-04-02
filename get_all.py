import codecs                         
from collections import namedtuple
from urllib.request import urlopen

from lxml import html

word_search_link = 'http://search1.ruscorpora.ru/syntax-explain.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=S&flags2=&parent3=1&level3=1&min3=&max3=&link3=on&type3=&lex3=&gramm3=PR&flags3=&text=word-info&requestid=1553071332398&language=ru&source='
Word = namedtuple("Word", "word lemma part_of_speech grammar_structure")


def word_to_str(word: Word):
    return 'word : {0}, lemma : {1}, part of speech : {2}, params : {3}'.format(word.word, word.lemma,
                                                                                word.part_of_speech,
                                                                                word.grammar_structure)


def get_word_info(word: str, suff: str, tags: list) -> Word:
    parsed_url = html.parse(word_search_link + suff)
    info = parsed_url.xpath('//td[@class="value"]/text()')
    lemma = codecs.decode(info[0].encode('raw-unicode-escape'), 'cp1251').replace(' ', '').replace('\n(', '')
    params = codecs.decode(info[2].encode('raw-unicode-escape'), 'cp1251')
    pr_list = params.split(',\xa0')
    for tag in tags:
        try:
            pr_list.remove(tag)
            return Word(word, lemma, tag, pr_list)
        except ValueError:
            continue


def search_highlighted(url: str,
                       tags: "лист строк") -> list:
    res = []
    parsed_url = html.parse(url)
    for highlighted_word in parsed_url.xpath('//span[@class="b-wrd-expl g-em"]'):
        word = highlighted_word.xpath('text()')
        suff = highlighted_word.xpath('@explain')
        if len(word) != 0:
            try:
                res.append(get_word_info(word[0], suff[0], tags))
            except AssertionError:
                res.append('Cannot get info from {0} for word {1}'.format(suff[0], word[0]))
    return res


def req(main_link: str, pages: int, tags: list):
    for i in range(pages):
        all = search_highlighted(main_link + str(i), tags)
        open('output' + str(i) + '.txt', 'a')
        f = open('output' + str(i) + '.txt', 'w')
        for a in all:
            try:
                f.write(word_to_str(a) + '\n')
            except TypeError:
                f.write(a + '\n')
        f.close()


req(
    'http://search1.ruscorpora.ru/syntax.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&text=lexgramm&mode=syntax&notag=1&simple=1&lang=ru&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=1&level2=1&min2=&max2=&link2=on&type2=&lex2=&gramm2=PR&flags2=&parent3=2&level3=2&min3=&max3=&link3=on&type3=&lex3=&gramm3=S&flags3=&p=0',
    8, ['v', 's', 'pr'])
