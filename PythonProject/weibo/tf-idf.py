#coding:utf8
__author__ = 'baiweili'
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import os
import os.path
import matplotlib.pyplot as plt

import datetime



if __name__ == "__main__":
    begin = datetime.datetime.now()
    sum = 0
    path = '/Users/baiweili/Desktop/output_1'
    corpus = []
    namelist = []
    for root,dirs,files in os.walk(path):
        for name in files:
            if not name.__contains__('.DS_Store'):
                if not name.__contains__('count.txt'):
                    result = ''
                    file = os.path.join(root,name)
                    f = open(file,'r')
                    lines = f.readlines()
                    for l in lines:
                        words = l.split()
                        key = words[0]
                        value = words[1]
                        s = (key+' ')*int(value)
                        result = result + s
                    result = result.strip()
                    result=result.decode('gbk').encode('utf-8')
                    corpus.append(result)
                    namelist.append(name)

                    # result.strip()
                    # file = '/Users/baiweili/Desktop/output1/' + name
                    # f = open(file,'w')
                    # f.write(result)



    # corpus=["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开
    #     "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果
    #     "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果
    #     "我 爱 北京 天安门"]#第四类文本的切词结果
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵


    # #存储tf-idf向量
    # word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
    # weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    # for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    #     print u"-------这里输出第",i,u"类文本的词语tf-idf权重------"
    #     s = []
    #     for j in range(len(word)):
    #         print word[j],weight[i][j]
    #         s.append(weight[i][j])
    #     f = open('/Users/baiweili/Desktop/result/'+str(namelist[i]),'w')
    #     f.write(str(s))
    #     f.close()

    # kmeans 聚类
    num_clusters = 10
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40, \
                    init='k-means++',n_jobs=-1)

    # print km_cluster.fit(tfidf).cluster_centers_
    '''
    n_clusters: 指定K的值
    max_iter: 对于单次初始值计算的最大迭代次数
    n_init: 重新选择初始值的次数
    init: 制定初始值选择的算法
    n_jobs: 进程个数，为-1的时候是指默认跑满CPU
    注意，这个对于单个初始值的计算始终只会使用单进程计算，
    并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40,
    服务器上面有20个CPU可以开40个进程，最终只会开10个进程
    '''
    #返回各自文本的所被分配到的类索引
    result = km_cluster.fit_predict(tfidf)
    #Sum of distances of samples to their closest cluster center.
    print km_cluster.inertia_
    print "Predicting result: ", result
    print "Sample number: ", len(result)

    # for i in xrange(len(tfidf)):
    #     #markIndex = int(clusterAssment[i, 0])
    #     plt.plot(tfidf[i][0], tfidf[i][1], corpus[km_cluster.labels_[i]]) #mark[markIndex])
    #     mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']

    for k in range(num_clusters):
        position = 0

        wordlist = []
        list = []
        list_1 = []
        for i in result:
            if i==k:
                # print i,position
                word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
                weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
                if len(list)==0:
                    list = weight[position]
                else:
                    list = map(lambda (a,b):a+b, zip(list,weight[position]))
            position += 1
        for l in list:
            list_1.append(l)
        for i in range(10):
            index = list_1.index(max(list_1))
            wordlist.append(word[index])
            # print word[index]
            list_1[index] = 0
        # print wordlist
        # print k
        print 'Topic ', k+1, ':', ' '.join(wordlist)
        # print wordlist
        # print list
        end = datetime.datetime.now()
    print 'run time',end-begin






