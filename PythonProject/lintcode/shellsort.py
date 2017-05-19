#coding:utf-8
__author__ = 'baiweili'
def shell_sort(list):
    n = len(list)
    # 初始步长
    gap = int(round(n / 2))
    while gap > 0:
        for i in range(gap, n):
            # 每个步长进行插入排序
            temp = list[i]
            j = i
            # 插入排序
            while j >= gap and list[j - gap] > temp:
                list[j] = list[j - gap]
                j -= gap
            list[j] = temp
        # 得到新的步长
        gap = int(round(gap / 2))
    return list
if __name__ == '__main__':
    list = [6,4,3,8,1,7]
    print shell_sort(list)