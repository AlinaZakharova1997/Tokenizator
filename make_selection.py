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
        # print(lemma_iter[1],'lemma_iter[1]')
        yield (lemma_iter[0],lemma_iter[1],lemma_iter[2])
        # print(lemma_iter,'lemma_iter')
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
    
# в этом блоке кода я делаю список списков, который потом передам функции def lemma_generator(lists)       
# перебираю все файлы из директории, где есть частотные словари
for filename in os.listdir(os.getcwd()):
    # список всех троек лемма-частота-тег для каждого файла
    dictlist = []
    # тк перебираются все файлы, включая данный, ставлю проверку на нужные файлы, те файлы csv
    if not filename.endswith('_1.csv'):
        continue
    file = open(filename, 'r')
    # считываю содержимое файла как словарь, учитывая разделитель
    dic = csv.reader(file, delimiter=',')
    for string in dic:
        # print(string,'string')
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




# множество пройденных лемм            
already_found_lemmas = set()
# множество конструкций, в которые вошли все леммы из множества лемм
constr_set = list()
# множество лемм, которые я буду обрабатывать в онтологии
lemmas_for_ontology = set()
# результирующий файл со списком конструкций
final_list_constr = open("fina_list_constr.txt", "w")
# финальный список лемм, которые надо проверить в онтологии
final_list_of_lemmas = open("lina_lemmas_list","w")
# сумма частот в процессе генерации лемм
summary = 0
# общая сумма всех частот по всем частям речи
# total = 122377
total = 117483
# начало цикла по генератору
# генератор берет список списков
for lemmas_info in list(lemma_generator(total_list)):
    lemma = lemmas_info[0]
    # print(lemmas_info)
    freq = int(lemmas_info[1])
    summary += freq
    if float(summary)/ total >= 0.8:
        break
    # log(lemma,'lemma after generator')
    if lemma not in already_found_lemmas:
        already_found_lemmas.add(lemma)
        
        # print(lemma)
        # открываю файл с конструкциями и леммами
        constrs = open('CONSTRS.csv', 'r')
        for constr in constrs:
            constr, lemmas = constr.split(" ;")
            lemmas = eval(lemmas)
            # это строка, тут по индексам будут только буквы
            # log(constr,'constr')
            constr_ok = True
            for constr_lemma in lemmas[0]:
                if constr_lemma not in  already_found_lemmas:
                    constr_ok = False
                    break
            if constr_ok and constr not in constr_set:
                for constr_lemma in lemmas[0]:
                    if constr_lemma not in lemmas_for_ontology:
                        lemmas_for_ontology.add(constr_lemma)
                        final_list_of_lemmas.write(constr_lemma + '\n' )
                        print(constr_lemma,'constr_lemma')
                # log(lemma,'lemma')
                constr_set.append(constr)
                final_list_constr.write(constr + '\n')
    
# не забудь закрыть файл        
final_list_constr.close()        
final_list_of_lemmas.close()        
            

   
      
