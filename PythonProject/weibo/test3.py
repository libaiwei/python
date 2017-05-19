# coding:utf8
n = raw_input()
n = int(n.strip())
l = []
d = {}
st = []
for i in range(n):
    s = raw_input()
    s = s.strip().split()
    st.append(s)
    s = range(int(s[0]),int(s[0])+int(s[1])+1)
    for j in s:
        if d.has_key(j):
            d[j] += 1
        else:
            d[j] = 1
# d = {i: l.count(i) for i in l}
d = sorted(d.items(), key=lambda x:x[1])
r1 = d[-1][0]
n1 = d[-1][1]
d1 = {}
lo = len(st)
st1 = []
for t in range(lo):
    k = st[t]
    if not (r1>=int(k[0]) and r1<=int(k[0])+int(k[1])):
        # print('*')
        st1.append(st[t])
        # st.remove(st[t])
print st1
for i in range(len(st1)):
    s = range(int(st1[i][0]),int(st1[i][0])+int(st1[i][1])+1)
    for j in s:
        if d1.has_key(j):
            d1[j] += 1
        else:
            d1[j] = 1
# d = {i: l.count(i) for i in l}
d1 = sorted(d1.items(), key=lambda x:x[1])
r2 = d1[-1][0]
n2 = d1[-1][1]
print(n1+n2)



