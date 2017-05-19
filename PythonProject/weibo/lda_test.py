#coding:utf8
import numpy as np
import lda
import lda.datasets
import os
import os.path
from sklearn.feature_extraction.text import CountVectorizer
import datetime

#数据预处理生成lda输入格式
begin = datetime.datetime.now()
sum = 0
path = '/Volumes/Transcend/output_1'
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
vectorizer = CountVectorizer()
a = vectorizer.fit_transform(corpus)
weight = a.toarray()
X = weight
# print type(weight) #<type 'numpy.ndarray'>
#shape(5839, 22834)
word = vectorizer.get_feature_names()
vocab = tuple(word)


# for i in range(len(weight)):
#     print u"-------这里输出第",i,u"类文本的词语词频权重------"
#     for j in range(len(word)):
#         print word[j],weight[i][j]
# #模板数据载入
# X = lda.datasets.load_reuters()
# vocab = lda.datasets.load_reuters_vocab()
# titles = lda.datasets.load_reuters_titles()

#训练数据，指定20个主题，500次迭代
model = lda.LDA(n_topics=10, n_iter=500, random_state=1)
model.fit_transform(X)
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 15
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    print 'Topic ', i, ':', ' '.join(topic_words)
    # print('Topic {'Topic {}: {}'}: {}'.format(i, ' '.join(topic_words)))
#前10篇最可能的topic分布
doc_topic = model.doc_topic_
end = datetime.datetime.now()
print 'run time',end-begin
# print("type(doc_topic): {}".format(type(doc_topic)))
# print("shape: {}".format(doc_topic.shape))
# for n in range(10):
#     topic_most_pr = doc_topic[n].argmax()
#     print("doc: {} topic: {}".format(n, topic_most_pr))

# import matplotlib.pyplot as plt
# f, ax= plt.subplots(5, 1, figsize=(8, 6), sharex=True)
# for i, k in enumerate([0, 1, 2, 3, 4, 5]):
#     ax[i].stem(topic_word[k,:], linefmt='b-',
#                markerfmt='bo', basefmt='w-')
#     ax[i].set_xlim(-50,6000)
#     ax[i].set_ylim(0, 0.2)
#     ax[i].set_ylabel("Prob")
#     ax[i].set_title("topic {}".format(k))
#
# ax[4].set_xlabel("word")
#
# plt.tight_layout()
# plt.show()

#
# import matplotlib.pyplot as plt
# f, ax= plt.subplots(5, 1, figsize=(8, 8), sharex=True)
# # for i, k in enumerate([0,4,1,5,2,3,14,15,6,8]):
# for i, k in enumerate([4,5,3,15,8]):
# # for i, k in enumerate([0,1,2,14,6]):
#     # print doc_topic[k,:]
#     ax[i].stem(doc_topic[k,:], linefmt='r-',
#                markerfmt='ro', basefmt='w-')
#     ax[i].set_xlim(-1, 11)
#     ax[i].set_ylim(0, 1)
#     ax[i].set_ylabel("Prob")
#     ax[i].set_title("Follower {}".format(i+1))
#
# ax[4].set_xlabel("Topic")
#
# plt.tight_layout()
# plt.show()