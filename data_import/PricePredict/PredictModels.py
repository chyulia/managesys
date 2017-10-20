#!/usr/bin/env python3.5.2
# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
import os

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

from data_import.PricePredict.RegressionModels.elm import ELMClassifier, ELMRegressor, GenELMClassifier, GenELMRegressor
from QinggangManageSys import settings

BASE_DIR = settings.BASE_DIR

class BaseModel(object, metaclass=ABCMeta):
    _model = None
    _model_pkl_dir = os.path.join(BASE_DIR, 'data_import', 'PricePredict', 'model_pkl')
    _model_pkl_path = os.path.join(_model_pkl_dir, "default.pkl")
    _model_name_plk = dict()

    # 更新模型，应该实现的机制是实例化具体类，调用本方法进行更新，而部分操作应该是同样的，可以考虑使用装饰器decorator.
    @abstractmethod
    def update_model(self, data_train, data_test, label_train, label_test):
        pass

    # TODO 接受需要预测的无label数据，同时给出缓存的相应模型的训练时在test数据集上的表现.
    def predict(self, data_feature):
        self.load_model_pkl()
        predict = self._model.predict(data_feature)
        return predict

    def save_model_pkl(self):
        """save model to pkl

        Args:
            model:
        Returns:

        """
        joblib.dump(self._model, self._model_pkl_path)

    def load_model_pkl(self):
        """load model from pkl
        """
        print(self._model_pkl_path)
        self._model = joblib.load(self._model_pkl_path)

    # 测试使用
    def load_data(self, filename):
        csv_path = os.path.join(BASE_DIR, filename)
        return pd.read_csv(csv_path)

    def standard_split_train_test(self, *data, test_ratio=0.1, random_state=None):
        """sklearn.select_model的方法进行训练集和测试集的划分

        Args:
            *data, test_ratio,
            random_state: 每次传入相同的int值以保证得到相同的随机序列

        Returns:
            datas(data_train, data_test[, label_train, label_test])
        """
        return train_test_split(*data, test_size=test_ratio, random_state=random_state)

    def create_data_label(self, model_data):
        labels = model_data['steelprice']
        cols = list(model_data.columns)
        cols.remove('steelprice')
        cols.remove('time')
        print(cols)
        model_data_scaler_notime = model_data[cols]
        model_data_scaler = preprocessing.scale(model_data_scaler_notime)  # ('numpy.ndarray')
        model_fill_scaler_tr = pd.DataFrame(model_data_scaler, columns=cols)
        return model_fill_scaler_tr, labels

class ExtremeLM(BaseModel):
    """docstring for ExtremeLM."""

    def __init__(self):
        self._model_pkl_path = os.path.join(self._model_pkl_dir, "elmr.pkl")
        print(self._model_pkl_path)

    def update_model(self, data_train, data_test, label_train, label_test):
        """接收已经过预处理的数据进行模型学习

        Args:
            data_train, data_test, label_train, label_test

        Returns:

        """
        elmr = ELMRegressor(activation_func='inv_tribas', random_state=0)
        elmr.fit(data_train, label_train)
        # test_predict = elmr.predict(data_test)
        score = elmr.score(data_test, label_test)
        print(score)
        # TODO 增加一个模型寻优过程，获取最佳的模型后保存，每个模型只保存最新的模型（最新的模型是在载入旧模型的基础上进行继续训练的）
        self._model = elmr
        self.save_model_pkl()


class SVR_(BaseModel):
    """docstring for SVR_."""
    def __init__(self):
        self._model_pkl_path = os.path.join(self._model_pkl_dir, "svr.pkl")
        print(self._model_pkl_path)


    def update_model(self, data_train, data_test, label_train, label_test):
        svm_reg = SVR(kernel="linear")
        svm_reg.fit(data_train, label_train)
        data_prediction = svm_reg.predict(data_test)
        svm_mse = mean_squared_error(label_test, data_prediction)
        score = svm_reg.score(data_test, label_test)
        svm_rmse = np.sqrt(svm_mse)
        # print(svm_rmse)
        print(score)
        self._model = svm_reg
        self.save_model_pkl()


class RandomForest(BaseModel):
    """docstring for RandomForest."""
    def __init__(self):
        self._model_pkl_path = os.path.join(self._model_pkl_dir, "rmf.pkl")
        print(self._model_pkl_path)

    def update_model(self, data_train, data_test, label_train, label_test):
        forest_reg = RandomForestRegressor(random_state=42)
        forest_reg.fit(data_train, label_train)
        data_prediction = forest_reg.predict(data_test)
        forest_mse = mean_squared_error(label_test, data_prediction)
        forest_rmse = np.sqrt(forest_mse)
        # print(forest_rmse)
        score = forest_reg.score(data_test, label_test)
        print(score)
        self._model = forest_reg
        self.save_model_pkl()


if __name__ == '__main__':
    # elm  = ExtremeLM()
    # model_prepared = elm.load_data("model_prepared.csv")
    # data, label = elm.create_data_label(model_prepared)
    # data_train, data_test, label_train, label_test = elm.standard_split_train_test(data, label, test_ratio=0.2, random_state=42)
    # elm.update_model(data_train, data_test, label_train, label_test)
    RandomForest()