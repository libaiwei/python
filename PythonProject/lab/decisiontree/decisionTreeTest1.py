# -*- coding:utf-8 -*-
from pandas import Series,DataFrame
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import sklearn.tree as tree
import pydotplus

file = pd.read_csv('iris.data.set标准数据集-鸢尾花.csv')
# file = file.drop('d',axis=1)
features = file.columns
print features
index = file.index
clf = DecisionTreeClassifier(criterion='entropy',min_samples_leaf=1,min_samples_split=1,max_depth=40)
clf = clf.fit(file[features[:-1]],file[features[-1]])
res = clf.predict([1,5,12,3])
with open("iris.data.set标准数据集-鸢尾花.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)
print res

dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names=features,
                     class_names=None,
                     filled=True, rounded=True,
                     special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("iris.data.set标准数据集-鸢尾花.pdf")