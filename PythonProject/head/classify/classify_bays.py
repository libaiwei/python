import json
import os
import os.path


def train():
    jsonfiles = []
    alpha = []
    alpha_1 = []
    alpha_2 = []
    beta = []
    for root,dirs,files in os.walk('../train'):
        for file in files:
            if file.__contains__('json'):
                jsonfiles.append(file)
                path = os.path.join(root,file)
                with open(path,'r') as f:
                    data = json.load(f)
                    for d in data:
                        alpha.append(d['pw_alpha'])
                        beta.append(d['pw_beta'])
    for root,dirs,files in os.walk('../train/label_1'):
        for file in files:
            if file.__contains__('json'):
                jsonfiles.append(file)
                path = os.path.join(root,file)
                with open(path,'r') as f:
                    data = json.load(f)

                    for d in data:
                        alpha_1.append(d['pw_alpha'])
    for root,dirs,files in os.walk('../train/label_2'):
        for file in files:
            if file.__contains__('json'):
                jsonfiles.append(file)
                path = os.path.join(root,file)
                with open(path,'r') as f:
                    data = json.load(f)
                    for d in data:
                        alpha_2.append(d['pw_alpha'])
    # print len(alpha)
    bins = 100
    # print min(alpha),max(alpha)
    width = (max(alpha)-min(alpha))/bins

    # alpha_1_feature
    alpha_1_feature = {}
    for a in alpha_1:
        x = int(a/width)
        if alpha_1_feature.has_key(x):
            alpha_1_feature[x] += 1.0/len(alpha_1)
        else:
            alpha_1_feature[x] = 1.0/len(alpha_1)

    # alpha_2_feature
    alpha_2_feature = {}
    for a in alpha_2:
        x = int(a/width)
        if alpha_2_feature.has_key(x):
            alpha_2_feature[x] += 1.0/len(alpha_2)
        else:
            alpha_2_feature[x] = 1.0/len(alpha_2)
    constant = min(alpha_1_feature.values()+alpha_2_feature.values())
    return alpha_1_feature,alpha_2_feature,width,constant
if __name__ == '__main__':
    [alpha_1_feature,alpha_2_feature,width,constant] = train()

    # testdata
    jsonfiles = []
    alpha = []
    alpha_1_p = 1
    alpha_2_p = 1
    count_1 = 0
    count_2 = 0
    for root,dirs,files in os.walk('../test/label_2/'):
        for file in files:
            if file.__contains__('json'):
                jsonfiles.append(file)
                path = os.path.join(root,file)
                with open(path,'r') as f:
                    data = json.load(f)
                    for d in data:
                        alpha.append(d['pw_alpha'])
    length = len(alpha)
    for i in range(5,length,5):
        test = alpha[i-5:i]
        for t in test:
            t = int(t/width)
            if alpha_1_feature.has_key(t):
                alpha_1_p *= alpha_1_feature[t]
            else:
                alpha_1_p *= constant
            if alpha_2_feature.has_key(t):
                alpha_2_p *= alpha_2_feature[t]
            else:
                alpha_2_p *= constant
        alpha_1_p = pow(alpha_1_p,0.2)
        alpha_2_p = pow(alpha_2_p,0.2)
        if alpha_1_p > alpha_2_p:
            count_1 += 1
            print 'label 1',alpha_1_p,alpha_2_p
        else:
            print 'label 2',alpha_1_p,alpha_2_p
            count_2 += 1
    print 'label 1:',count_1
    print 'label 2:',count_2