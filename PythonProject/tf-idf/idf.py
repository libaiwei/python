import tf
import os
import os.path
def idf():
    for root,dirs,files in os.walk('/Users/baiweili/Desktop/output_20_Train'):
        if not root is '/Users/baiweili/Desktop/output_20_Train':
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