from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn import cross_validation
import sklearn.tree as tree
import pydotplus

if __name__  == '__main__':
    file = pd.read_csv('./treedata.csv')
    f = file.drop('d',axis =1)
    f = file.drop('r',axis =1)
    p = file['r']
    clf = DecisionTreeClassifier(criterion='entropy')
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(f, p, test_size=0.2, random_state=0)
    clf = clf.fit(X_train,y_train)
    result = clf.predict(X_test)
    print(clf.feature_importances_)
    features = f.columns

    with open("iris.dot", 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)

    dot_data = tree.export_graphviz(clf, out_file=None,
                         feature_names=features,
                         class_names=['0','1'],
                         filled=True, rounded=True,
                         special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf("iris.pdf")