#!/usr/bin/env python3.5.2
# -*- coding:utf-8 -*-
import math
from abc import ABCMeta, abstractmethod
'''
scientific calculate packages
'''
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
'''
ELM
'''
from data_import.PricePredict.RegressionModels.elm import ELMClassifier, ELMRegressor, GenELMClassifier, GenELMRegressor


class BaseModel(object, metaclass=ABCMeta):

    # TODO 更新模型，应该实现的机制是实例化具体类，调用本方法进行更新，而部分操作应该是同样的，可以考虑使用装饰器decorator.
    @abstractmethod
    def update_model(self):
        pass
    # TODO 接受需要预测的无label数据，同时给出缓存的相应模型的训练时在test数据集上的表现.
    @abstractmethod
    def predict(self,data):
        pass


class ExtremeLM(BaseModel):
    """docstring for ExtremeLM."""
    def __init__(self):
        super(ExtremeLM, self).__init__()
        print('ExtremeLM init')

    def log(self):
        print('ExtremeLM predict')
        return 'ExtremeLM predict'

    def update_model(self):
        pass

    def predict(self,model_data,exnum):
        return self.elm_(model_data,0.2)

    def elm_(self, model_data, exnum):
        # print(exnum)
        cols_all = list(model_data.columns)
        col_len = len(cols_all)
        out = cols_all[col_len - 1]
        feature = cols_all[2:col_len - 1]

        X = model_data[feature]
        Y = model_data[out]
        Y_array = np.array(Y)
        data_scale_num = len(model_data.index)
        # print(data_scale_num)
        extension_num = math.ceil((data_scale_num * (1 - exnum)))
        # print(extension_num)
        '''
        数据处理有没有更好的方式,暂时使用标准化
        '''
        origal_mean = Y_array.mean(axis=0)  # 很奇怪的在这里axis=0求列平均，1求行平均
        origal_std = Y_array.std(axis=0)
        # print(model_data[cols_all[2:]])
        data_scale = preprocessing.scale(np.array(model_data[cols_all[2:]]))
        # print(type(data_scale))
        data_scale_df = pd.DataFrame(data_scale, columns=cols_all[2:])
        # print(data_scale_df)

        X_scale = data_scale_df[feature][:extension_num]
        Y_scale = data_scale_df[out][:extension_num]

        X_extension = data_scale_df[feature][extension_num:data_scale_num]
        Y_extension = data_scale_df[out][extension_num:data_scale_num]
        Y_extension_array = np.array(Y_extension)
        # print(Y_extension_array)
        '''
        暂时还是随机划分训练集和测试集
        '''
        X_train, X_test, y_train, y_test = train_test_split(X_scale, Y_scale, test_size=0.2, random_state=1)

        elmr = ELMRegressor(activation_func='inv_tribas', random_state=0)
        elmr.fit(X_train, y_train)

        y_predict = elmr.predict(X_extension)

        timeline = model_data[cols_all[0]][extension_num:]
        timeline = timeline.map(lambda x: str(x)[0:10])
        score = elmr.score(X_test, y_test)
        result = {}
        result["score"] = score
        result["timeline"] = list(timeline)
        result["true_value"] = list(self.get_true_predict_value(Y_extension_array, origal_std, origal_mean))
        result["predict_value"] = list(
            map(lambda x: x / 1.2, list(self.get_true_predict_value(y_predict, origal_std, origal_mean))))
        # print(result)
        return result

    def get_true_predict_value(self, y_predict, origal_std, origal_mean):
        row_num = y_predict.shape[0]
        y_predict_true = y_predict.copy()
        for xi in range(row_num):
            y_predict_true[xi] = y_predict[xi] * origal_std + origal_mean
        return y_predict_true


class SVM(object):
    """docstring for SVM."""
    def __init__(self):
        super(SVM, self).__init__()
        print('SVM:init')

    def log(self):
        print('SVM predict')
        return 'SVM predict'

    def predict(self,model_data,exnum):
    	return ExtremeLM().predict(model_data,0.2)

class LR(object):
    """docstring for SVM."""
    def __init__(self):
        super(LR, self).__init__()
        print('LR:init')

    def log(self):
        print('LR predict')
        return 'LR predict'

    def predict(self,model_data,exnum):
    	return ExtremeLM().predict(model_data,0.2)

class BP(object):
    """docstring for SVM."""
    def __init__(self):
        super(BP, self).__init__()
        print('BP:init')

    def log(self):
        print('BP predict')
        return 'BP predict'

    def predict(self,model_data,exnum):
    	return ExtremeLM().predict(model_data,0.2)

class RandomForest(object):
    """docstring for SVM."""
    def __init__(self):
        super(RandomForest, self).__init__()
        print('RandomForest:init')

    def log(self):
        print('RandomForest predict')
        return 'RandomForest predict'

    def predict(self,model_data,exnum):
    	return ExtremeLM().predict(model_data,0.2)

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
    elm  = ExtremeLM()
    elm.log()
