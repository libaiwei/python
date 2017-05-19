# -*- coding: utf-8 -*-
# def lettercount(str_):
#     # str_='ssdasdasefadd'
#     dict_char_tmp = {i:str_.count(i) for i in str_} #得到所有单词的个数
#     return dict_char_tmp
# def traversal(str):
#     count = 0
#     # str = 'qqqaa'
#     l = len(str)/2
#     for i in range(1,l+1):
#         i = i * 2
#         # print i
#         for j in range(0,len(str)-i+1):
#             s_test = str[j:j+i]
#             d = lettercount(s_test)
#             k = 1
#             for value in d.itervalues():
#                 if (value % 2) != 0:
#                     k = 0
#                     break
#             if k == 1:
#                 count += 1
#     return count
#
# # print traversal('qqqaa')
# s = raw_input()
# str = s.strip()
# str = traversal(str)
#
# print(str)

s = 'hello world hello'
l = s.split()
d = {i: l.count(i) for i in l}
print d