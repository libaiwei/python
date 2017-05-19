# coding:utf8
fin = open('/Users/baiweili/Desktop/C-small-1-attempt0.in','r')
fout = open('/Users/baiweili/Desktop/b1.txt','w')

count = -1
for line in fin:
    count = count + 1
    cols = line.strip().split()
    if count == 0:
        continue
    stallnum = int(cols[0])
    number = int(cols[1])
    s_list = []
    s_list.append(stallnum)
    for i in range(number):
        m_len = 0
        m_label = 0
        s_list.sort()
        m_label = len(s_list) - 1
        m_len = s_list[m_label]
        del s_list[m_label]
        if m_len != 1:
            if m_label == 0:
                l_left = []
            else:
                l_left = s_list[0:m_label]
            l_right = s_list[m_label:]
            if m_len % 2 == 1:
                l_left.append(m_len/2)
                l_left.append(m_len/2)
                s_list = []
                s_list = l_left+l_right
                if i == number - 1:
                    fout.write("Case #%d: %d %d\n" %(count, m_len/2, m_len/2))
            else:
                if m_len == 2:
                    l_left.append(m_len/2)
                    s_list = []
                    s_list = l_left+l_right
                    if i == number - 1:
                        fout.write("Case #%d: %d %d\n" %(count, m_len/2, 0))
                else:
                    l_left.append(m_len/2-1)
                    l_left.append(m_len/2)
                    s_list = []
                    s_list = l_left + l_right
                    if i == number - 1:
                        fout.write("Case #%d: %d %d\n" %(count, m_len/2, m_len/2-1))
        else:
            if i == number - 1:
                fout.write("Case #%d: %d %d\n" %(count, m_len/2, m_len/2))