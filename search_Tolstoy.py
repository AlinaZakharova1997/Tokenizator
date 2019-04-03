import search
from search import SearchEngine

x = SearchEngine('data')

print(x.get_dict('Пьер'))
del x
