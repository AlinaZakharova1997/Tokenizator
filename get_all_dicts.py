import csv
# для перечисления всех файлов из папки
import os
# для сортировки словаря
from collections import OrderedDict
# новый словарь, где будут все словари в объединенном виде
output = {}
# перебираю все файлы из директории
for filename in os.listdir(os.getcwd()):
    # тк перебираются все файлы, включая данный, ставлю проверку на нужные файлы, те файлы csv
    if not filename.endswith('.csv'):
        continue
    file = open(filename, 'r')
    # считываю содержимое файла как словарь, учитывая разделитель
    dic = csv.reader(file, delimiter=';')
    # перебираю ключи и значения словаря
    for string in dic:
        # ключ это слово
        key = string[0]
        # значение это частота слова
        value = int(string[1])
        # если ключа нет в словаре, добавляю ключ и его значение
        if key not in output:
            output[key] = value
        else:
            # если ключ уже есть, суммирую старое значение и новое
            output[key] = output[key] + value
# сортирую словарь и записываю в результирующий файл csv с разделителем ;            
result = OrderedDict(sorted(output.items(), key = lambda t: t[1], reverse=True))            
with open('Verb_Total.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter= ';')
        for key, value in result.items():
            writer.writerow([key,value])            
            
            

