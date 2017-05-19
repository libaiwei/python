# n = raw_input()
from enum import Enum
try:
    Animal = Enum('Animal', 'ant bee cat dog dog')
except:
    print 'a'
# print(Animal.bee.value)
