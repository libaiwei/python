import tf
import os
import os.path
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def idf_dict(count,path):
    tf_idf_dict = {}
    tf_dict = tf.tf_dict()
    print tf_dict
    idf_dict = {}
    for d in tf_dict.keys():
        idf_dict[d] = 0
    for root,dirs,files in os.walk(path):
        for name in files:
            file = os.path.join(root,name)
            f =open(file)
            text = f.read()
            list = text.split()
            for key in idf_dict.keys():
                if list.__contains__(key):
                    idf_dict[key] += 1
    for key,value in tf_dict.items():
        idf_dict[key] = math.log10(float(count)/float(idf_dict[key]))
        tf_idf_dict[key] = value*idf_dict[key]
    return tf_idf_dict
def idf():
    for root,dirs,files in os.walk('/Users/baiweili/Desktop/20_Train'):
        if not root is '/Users/baiweili/Desktop/20_Train':
            tf_dict = tf.tf_dict(root)
            name = root.split('/')[-1]
            result_file = '/Users/baiweili/Desktop/result/'+name
            f = open(result_file,'wb')
            for k,v in tf_dict.items():
                f.write(str(k) + ' ' + str(v))
                f.write('\n')
            f.close()
if __name__ == '__main__':
    idf()
# if __name__ == '__main__':
#     tf_idf_dict = idf_dict(9833,'/Users/baiweili/Desktop/output')
#     tf_idf_list = sorted(tf_idf_dict.items(), key=lambda x:x[1],reverse=True)
#     tf_idf_list = tf_idf_list[:200]
#     f = open('/Users/baiweili/Desktop/result1.txt','wb')
#     for l in tf_idf_list:
#         str = unicode(l[0],'gbk')
#         f.write(str)
#         f.write('\n')
#     f.close()
