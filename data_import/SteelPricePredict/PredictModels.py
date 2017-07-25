# -*- coding:utf-8 -*-
import math
'''
scientific calculate packages
'''
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
'''
ELM
'''
from data_import.SteelPricePredict.RegressionModels.ExtremeLM import elm_

class ExtremeLM(object):
    """docstring for ExtremeLM."""
    def __init__(self):
        super(ExtremeLM, self).__init__()
        print('ExtremeLM init')

    def log(self):
        print('ExtremeLM predict')
        return 'ExtremeLM predict'

    def predict(self,model_data,exnum):
        return elm_(model_data,0.2)



class SVM(object):
    """docstring for SVM."""
    def __init__(self):
        super(SVM, self).__init__()
        print('SVM:init')

    def log(self):
        print('SVM predict')
        return 'SVM predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.2)

class LR(object):
    """docstring for SVM."""
    def __init__(self):
        super(LR, self).__init__()
        print('LR:init')

    def log(self):
        print('LR predict')
        return 'LR predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.2)

class BP(object):
    """docstring for SVM."""
    def __init__(self):
        super(BP, self).__init__()
        print('BP:init')

    def log(self):
        print('BP predict')
        return 'BP predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.2)

class RandomForest(object):
    """docstring for SVM."""
    def __init__(self):
        super(RandomForest, self).__init__()
        print('RandomForest:init')

    def log(self):
        print('RandomForest predict')
        return 'RandomForest predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.2)

    def classify(self):

        df = pd.read_csv('sklearn_data.csv')
        train, test = df.query("is_date != -1"), df.query("is_date == -1")
        y_train, X_train = train['is_date'], train.drop(['is_date'], axis=1)
        X_test = test.drop(['is_date'], axis=1)

        model = RandomForestClassifier(n_estimators=50,
                                       criterion='gini',
                                       max_features="sqrt",
                                       min_samples_leaf=1,
                                       n_jobs=4,
                                   )
        """
        @param n_estimators：指定森林中树的颗数，越多越好，只是不要超过内存；
        @param criterion：指定在分裂使用的决策算法；
        @param max_features：指定了在分裂时，随机选取的特征数目，sqrt即为全部特征的平均根；
        @param min_samples_leaf：指定每颗决策树完全生成，即叶子只包含单一的样本；
        @param n_jobs：指定并行使用的进程数；
        """
        model.fit(X_train, y_train)
        print(model.predict(X_test))
        print(zip(X_train.columns, model.feature_importances_))


if __name__ == '__main__':
    ExtremeLM('hello')
