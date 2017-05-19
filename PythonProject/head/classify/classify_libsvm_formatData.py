import json
import os
import os.path

def loaddata():
    jsonfiles = []
    alpha_1 = []
    alpha_2 = []
    # alpha_3 = []
    beta_1 = []
    beta_2 = []
    # beta_3 = []
    for root,dirs,files in os.walk('data/'):
        for file in files:
            if file.__contains__('data_ear_head')&file.__contains__('json'):
                jsonfiles.append(file)
                path = os.path.join(root,file)
                with open(path,'r') as f:
                    data = json.load(f)
                    for d in data:
                        alpha_1.append(d['pw_alpha'])
                        beta_1.append(d['pw_beta'])
            # elif file.__contains__('data_ear_hand')&file.__contains__('json'):
            #     jsonfiles.append(file)
            #     path = os.path.join(root,file)
            #     with open(path,'r') as f:
            #         data = json.load(f)
            #         for d in data:
            #             alpha_3.append(d['pw_alpha'])
            #             beta_3.append(d['pw_beta'])
            elif file.__contains__('json'):
                jsonfiles.append(file)
                path = os.path.join(root,file)
                with open(path,'r') as f:
                    data = json.load(f)
                    for d in data:
                        alpha_2.append(d['pw_alpha'])
                        beta_2.append(d['pw_beta'])
    feature_1 = zip(alpha_1,beta_1)
    feature_2 = zip(alpha_2,beta_2)
    return feature_1,feature_2

def svm_file(feature,label):
    lines = []
    for i in feature:
        l = label + ' ' + '1' + ':' + str(i[0]) + ' ' + '2' + ':' + str(i[1])
        lines.append(l)
    return lines
if __name__ == '__main__':
    [feature_1,feature_2] = loaddata()
    lines_1 = svm_file(feature_1,'1')
    lines_2 = svm_file(feature_2,'2')
    lines = lines_1+lines_2
    f = open('headdata','w')
    f.write('\n'.join(lines))
    # os.popen('cat test_1 > test_3')
    # os.popen('cat 2 >> 3')
