import csv
# для перечисления всех файлов из папки
import os
# для сортировки словаря
from collections import OrderedDict
# результирующий словарь
output = {}
# будущий список списков
total_list = []
# перебираю все файлы из директории, где есть частотные словари
for filename in os.listdir(os.getcwd()):
    dictlist = []
    # тк перебираются все файлы, включая данный, ставлю проверку на нужные файлы, те файлы csv
    if not filename.endswith('Total.csv'):
        continue
    file = open(filename, 'r')
    # считываю содержимое файла как словарь, учитывая разделитель
    dic = csv.reader(file, delimiter=';')
    for string in dic:
        # ключ это слово
        key = string[0]
        # значение это частота слова
        value = int(string[1])
        # добавлю и ключ, и значение
        dictlist.append([key,value])
    # делаю список списков    
    total_list.append(dictlist)
    
# открываю файл с конструкциями и леммами
constrs = open('CONSTRS.csv', 'r')



def lemma_generator(lists):
    '''
    This function generates lemmas
    @param lists: list of lists of lemma:frequency pairs
    It chooses a lemma with a max frequency upon firsts elements of each list given and yeilds it
    '''
    # превращаю списки в итераторы. итератор - генератор, осуществляющий итерацию.    
    iters = [iter(x) for x in  lists]
    # список с первыми элементами списков
    firsts = [next(it) for it in iters]
    # нахожу лемму с максимальным значением частоты
    lemma_iter = max(firsts, key=lambda lemma, freq: freq)
    yield (lemma_iter)
    print(lemma_iter,'lemma_iter')
    lemma_iter.pos = firsts.index(lemma_iter)
    # переходим к следующему элементу в этом списке
    firsts[lemma_iter.pos] = next(iters[lemma_iter.pos]) 
    if StopIteration:
        iters.pop(lemma_iter.pos)
        firsts.pop(lemma_iter.pos)
        
        

   
