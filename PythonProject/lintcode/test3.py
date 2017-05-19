__author__ = 'baiweili'
def decidecontain(A,B):
    A = list(A)
    for s in B:
        if not A.__contains__(s):
            return False
        else:
            n = A.index(s)
            A = A[:n]+A[n+1:]
    return True
if __name__ == '__main__':
    print decidecontain('ad','dd')