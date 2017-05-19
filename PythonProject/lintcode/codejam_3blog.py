from collections import defaultdict
import Queue

fin = open('/Users/baiweili/Desktop/C-small-1-attempt0.txt', 'r')
fout = open('/Users/baiweili/Desktop/b2.txt', 'w')
T = int(fin.readline())
for ti in range(1, T + 1, 1):
    nums = fin.readline().strip().split()
    N, K = map(int, nums)
    ans_l, ans_r = -1, -1
    que = Queue.Queue()
    que.put([N, 1])
    q = que
    while K > 0:
        cnt = defaultdict(int)
        while K > 0 and not que.empty():
            n, c = que.get()
            K -= c
            ans_l, ans_r = n >> 1, n - 1 >> 1
            cnt[ans_l] += c
            cnt[ans_r] += c
        for v in sorted(cnt.keys(), reverse=True):
            if v == 0:
                break
            else:
                que.put([v, cnt[v]])
    print( "Case #%d: %d %d" % (ti, ans_l, ans_r ) )