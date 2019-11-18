import csv
# для перечисления всех файлов из папки
import os
# это для того, чтобы аппендить в словарь сколько угодно значений по одному ключу
from collections import defaultdict
# собственно словарь
d = defaultdict(list)
# это для сортировки
from collections import OrderedDict
# это тег
tag = 'adv'
file = open('Adverb_Total.csv', 'r')
dic = csv.reader(file, delimiter=';')
for string in dic:
    # ключ это слово
    key = string[0]
    # print(key,'key')
    # значение это частота слова
    value = int(string[1])
    # добавляю в новый словарь частоту и тег
    d[key].append(value)
    d[key].append(tag)
        
result = OrderedDict(sorted(d.items(), key = lambda t: t[1], reverse=True))            
with open('Adverb_Tag_Total.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in result.items():
            writer.writerow([key,value])            
            
