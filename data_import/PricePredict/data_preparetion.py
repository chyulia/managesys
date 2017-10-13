import os

import pandas as pd
from sklearn.model_selection import train_test_split
# from django.conf import settings
# MEDIA_ROOT = settings.MEDIA_ROOT

from QinggangManageSys.choose_settings import MEDIA_ROOT



class Data_Preparetion(object):
    def __init__(self):
        self.data_root = os.path.join(MEDIA_ROOT, 'files', 'data')
        print(self.data_root)

    def load_data(self, filename):
        csv_path = os.path.join(self.data_root, filename)
        return pd.read_csv(csv_path)

# TODO 增加一些数据可视化及洞见数据特征的一些方法，
class Data_Discover_Visualize(object):
    pass

class ModelTrain(object):
    def __init__(self):
        pass

    def split_train_test(self, data):
        train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
        return train_set, test_set

'''
条件筛选？
housing["income_cat"].where(housing["income_cat"] < 5, 5.0, inplace=True)
'''

if __name__ == '__main__':
    data = Data_Preparetion().load_data('tegang.csv')
    print(data.columns)