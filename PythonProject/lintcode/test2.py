__author__ = 'baiweili'

def anagram(s,t):
    list1 = []
    list2 = []
    for s0 in s:
        list1.append(s0)
        list1.sort()
    for s1 in t:
        list2.append(s1)
        list2.sort()
    return cmp(list1,list2)
if __name__ == '__main__':
    print anagram('acssb','abcd')
    print int('a')