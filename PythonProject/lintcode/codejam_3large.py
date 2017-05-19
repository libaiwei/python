# coding:utf8
import math
fin = open('/Users/baiweili/Desktop/C-small-1-attempt0.in'
           '','r')
fout = open('/Users/baiweili/Desktop/b2.txt','w')
N = int(fin.readline())

for i in range(1, N + 1):
    avg_position_1 = ''
    flag = 0
    nums = fin.readline().strip().split()
    position = int(nums[0])
    person = int(nums[1])
    cell = int(math.log(float(person+1))/math.log(float(2)))
    if pow(2,cell)-1 == person:
        person_1 = pow(2,cell)-1
    else:
        person_1 = pow(2,cell+1)-1
    if position <= person_1:
        flag = 1
        avg_position = 0
        avg_position_1 = 0
    else:
        position_remain = position - person_1
        if position_remain == person_1:
            avg_position = 1
        else:
            avg_position = position_remain/(person_1+1)
    if position%4 == 0 and flag == 0:
        avg_position_1 = avg_position + 1
    if position%4 == 1 and flag == 0:
        avg_position_1 = avg_position + 1
    if not avg_position_1:
        avg_position_1 = avg_position
    if position < 2*person:
        avg_position_1 = 0
        avg_position = 0
    if position > 2*person and avg_position_1 == 0:
        avg_position_1 = 1
    print avg_position_1,avg_position
fin.close()
fout.close()