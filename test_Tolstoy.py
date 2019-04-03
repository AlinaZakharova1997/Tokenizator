import indexer
from indexer import Indexer, Position, Position_Plus

x = Indexer('C:\\Users\\Алина\\Desktop\\Моя папка))))\\Змий))')

print(x.get_index_with_line('толстой1.txt'))
print(x.get_index_with_line('толстой2.txt'))
print(x.get_index_with_line('толстой3.txt'))
print(x.get_index_with_line('толстой4.txt'))
del x
