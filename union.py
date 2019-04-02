
open('all.out', 'a')
f = open('all.out', 'w')
for i in range(65):
    f.write(open('output' + str(i) + '.txt').read())

f.close()
