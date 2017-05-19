import dict
import os
import os.path
def tf_dict(dir):
    dicts = {}
    for root,dirs,files in os.walk(dir):
        for name in files:
            path = os.path.join(root,name)
            D = dict.dict(path)
            for d in D:
                if dicts.has_key(d):
                    dicts[d] = int(dicts[d]) + int(D[d])
                else:
                    dicts[d] = int(D[d])
    tf_dict = {}
    tf_down = sum(dicts.values())
    for d in dicts.keys():
        tf_up = dicts[d]
        tf = float(tf_up)/float(tf_down)
        tf_dict[d] = tf
    tf_dict = sorted(tf_dict.items(),key=lambda x:x[1],reverse=True)
    # tf_dict = tf_dict[:200]
    tf_dict_1 = {}
    k=0
    for l in tf_dict:
        if len(l[0])>3:
            tf_dict_1[l[0]]=l[1]
            k+=1
            if k == 100:
                break

    # for l in tf_dict:
    #     tf_dict_1[l[0]]=l[1]


    # for l in list:
    #     tf_dict[l[0]] = l[1]
    return tf_dict_1
# if __name__ == '__main__':
#     for root,dirs,files in os.walk('/Users/baiweili/Desktop/output1'):
#         if not root is '/Users/baiweili/Desktop/output1':
#             tf_dict = tf_dict(root)
#             name = root.split('/')[-1]
#             result_file = '/Users/baiweili/Desktop/result/'+name
#             f = open(result_file,'wb')
#             for d in tf_dict.keys():
#                 f.write(d)
#                 f.write('\n')
#             f.close()