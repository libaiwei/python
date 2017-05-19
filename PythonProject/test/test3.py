file = open('test2.py')
lines = file.readlines()
list = []
for l in lines:
    if l.startswith('From'):
        l = l.rstrip('\n')
        words = l.split(' ')
        list += words[1:2]
for i in range(0,len(list)):
    print list[i],i
