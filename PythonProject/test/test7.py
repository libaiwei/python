import scipy.io as sio
data = sio.loadmat('/Users/lbw/PycharmProjects/python/PythonProject/tensorFlowTest/mycnn/data.mat')
images = data['train']
print len(images)