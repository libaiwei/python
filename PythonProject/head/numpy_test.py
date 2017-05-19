# from numpy import *
import numpy as np
class test:
    def __init__(self,a):
        self.a = a
    def list_to_reshape(self):
        a = np.arange(15).reshape(3,5)
        for l in a:
            print l
        print np.arange(15)
        print a.shape
        print self.a
    def list_demo(self):
        list = [1,2,3,4,5,6]
        list.reshape(2,3)
        print list
    def start(self):
        self.list_to_reshape()

spider = test('a')
spider.start()
