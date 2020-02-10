import csv
# для перечисления всех файлов из папки
import os
# для сортировки словаря
from collections import OrderedDict
# результирующий словарь
output = {}
# будущий список списков
total_list = []
# файл, куда пишется вся выдача, чтобы не перегрузить консольку или IDLE 
log_file = open('result.log', 'w')
           
def log(*args):
    '''
    This function writes information in file and also prints it on the screen
    @param *args: arguments the function takes; the number of arguments is not limited
    ''' 
    log_file.write(' '.join(str(arg) for arg in args))
    log_file.write('\n')
    log_file.flush()
    '''print(*args)'''            
# в этом блоке кода я делаю список списков, который потом передам функции def lemma_generator(lists)       
# перебираю все файлы из директории, где есть частотные словари
for filename in os.listdir(os.getcwd()):
    # список всех троек лемма-частота-тег для каждого файла
    dictlist = []
    # тк перебираются все файлы, включая данный, ставлю проверку на нужные файлы, те файлы csv
    if not filename.endswith('Total.csv'):
        continue
    file = open(filename, 'r')
    # считываю содержимое файла как словарь, учитывая разделитель
    dic = csv.reader(file, delimiter=';')
    for string in dic:
        # lemma это лемма слова
        lemma = string[0]
        # print(lemma,'lemma')
        # часота слова
        freq = string[1]
        # print(freq,'freq')
        # грамматический тег слова
        tag = string[2]
        # print(tag,'tag')
        # добавлю лемму, частоту и тег в список
        dictlist.append((lemma,freq,tag))
        # print(dictlist,'dictlist')
        # print((key,freq,tag))
        # делаю список списков    
    total_list.append(dictlist)
# log(total_list)


def lemma_generator(lists):
    '''
    This function generates lemmas
    @param lists: list of lists of lemma:[frequency,tag] items
    It chooses a lemma with a max frequency upon firsts elements of each list given and yeilds it
    '''
    # превращаю списки в итераторы. итератор - генератор, осуществляющий итерацию.    
    iters = [iter(x) for x in  lists]
    # список с первыми элементами списков
    firsts = [next(it) for it in iters]
    # print(firsts,'firsts')
    while firsts:
        # нахожу лемму с максимальным значением частоты
        # функция key возвращает тот объект, по которому идет сортировка, у меня сортировка по частоте!!!
        lemma_iter = max(firsts, key=lambda lem_tuple: (int(lem_tuple[1])))
        # lemma_iter = max(firsts) для проги!
        yield (lemma_iter[0],lemma_iter[2])
        print(lemma_iter,'lemma_iter')
        # номер массива, из которого я взяла этот элемент
        lemma_iter_pos = firsts.index(lemma_iter)
        try:
            # переходим к следующему элементу в этом списке
            firsts[lemma_iter_pos] = next(iters[lemma_iter_pos]) 
        except StopIteration:
            # если один из списков закончился, то удаляем и возвращаем удаленный элемент
            # те первый элемент такого списка и его итератор нам больше не нужны и мы их удаляем
            iters.pop(lemma_iter_pos)
            firsts.pop(lemma_iter_pos)

# открываю файл с конструкциями и леммами
constrs = open('CONSTRS.csv', 'r')
# множество пройденных лемм            
already_found_lemmas = set()
contains = True
# начало цикла по генератору
for constr in constrs:
    # генератор берет список списков
    lemma = lemma_generator(total_list)
    already_found_lemmas.add(lemma)
    for lemma in already_found_lemmas:
        # тут у меня не строка, а генератор...
        if lemma  in constr[1][0]:
            # yield lemma
            log(lemma,'lemma')
        # yield constr[0]
        log(constr[0],'constr')
            

            

