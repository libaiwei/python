import dict
import os
import os.path
list = []
dicts = {}
for root,dirs,files in os.walk('/Users/baiweili/Desktop/output'):
    if not root is '/Users/baiweili/Desktop/test':
        print root
    # print dirs
    # for name in files:
    #     path = os.path.join(root,name)