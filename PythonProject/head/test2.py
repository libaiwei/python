import numpy as np
from scipy import io
# a=np.mat('1,2,3')
# # a = np.mat([],dtype=int)
# a1 = np.mat('7,8,9;4,3,6')
# a12 = np.mat('7,8,9;4,3,6')
#
# a = np.append(a, a1,axis=0)
# a = np.append(a,a12,axis=0)
# b=np.array([[1,1,1],[2,2,2]])
# print a
# b = np.raw_stack(b,b1)
# print type(a)
# io.savemat('a.mat', {'matrix': a})
X = np.empty(shape=[0, 3L])
a = np.mat('7.1,8.1,9;3,4,5')

# a = np.mat('7,8,9;3,4,5')
b = np.append(X,a,axis=0)
# print a[0:2]
print type(a)
print a[0:1,:]
print a.shape