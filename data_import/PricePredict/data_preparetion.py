# -*- coding: utf-8 -*-
#!/usr/bin/env python3.5.2
import datetime
import os

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from data_import.PricePredict import pre_config
from data_import import models
from QinggangManageSys import settings


MEDIA_ROOT = settings.MEDIA_ROOT
BASE_DIR = settings.BASE_DIR
TABLE_NAMES = pre_config.table_name

time_fields = {
            'tkszs': 'tkszs_date',
            'meiyuan': 'meiyuan_date',
            'steelprice': 'updatetime',
            'meitan_ljm': 'coal_ljm_date',
            'jkk_qingdao': 'jkk_date',
            'fgzs': 'fgzs_date',
            'gtcl': 'gangtie_date',
        }
price_field = {
    'tkszs': 'tkszs_qdg',
    'meiyuan': 'meiyuan_zhishu',
    'steelprice': 'price',
    'meitan_ljm': 'coal_ljm_jiage',
    'jkk_qingdao': 'jkk_jizhunjia',
    'fgzs': 'fgzs_zhi',
    'gtcl': 'gangtie_gangcai',
}

class Data_Preparetion(object):

    _table_names = None
    _time_fields = pre_config.time_fields
    _price_field = pre_config.price_field

    def __init__(self, table_names=TABLE_NAMES):
        self.data_root = os.path.join(MEDIA_ROOT, 'files', 'data')
        print(self.data_root)
        print(BASE_DIR)
        self._table_names = table_names

    def intergrate_data_from_db(self):

        """

        Args:
            table_names: a list contains tablenames need to be intergrated

        Returns:
            train_data: a dataframe contains training data
            train_label: a series contains labels data

        """
        # TODO 会存在不存在的表名
        # table_names.remove("tiejingfen")
        dfs = self.integrate_db_dataframe()
        # 按时间生成模型数据
        model = self.create_model_data(dfs)
        model.to_csv('model.csv', encoding='utf-8')
        model_prepared = self.dfs_preproccess(model)
        model_prepared.to_csv('model_prepared.csv', encoding='utf-8')
        return model_prepared

    def integrate_db_dataframe(self):
        dfs = dict()
        sqlVO = dict()
        bsm = models.BaseManage()

        @models.transaction_decorator
        def inner_exe(bsm):
            for tname in self._table_names:
                if tname == 'steelprice':
                    desc, rs = self._steelprice_custom(bsm)
                    print(desc)
                else:
                    sqlVO['sql'] = 'SELECT * FROM {0}'.format(tname)
                    desc = bsm.direct_get_description(sqlVO)
                    rs = bsm.select_single(sqlVO)  # 必须是字典类型，否则无法匹配dataframe列名
                if rs:
                    # print(rs[:2])
                    try:
                        df = pd.DataFrame(rs, columns=pd.Series(desc[0]))
                        # exceler.save_csv_pd(df,tname,table_name_means)
                        dfs[tname] = df  # 'fgzs'暂时无数据
                    except Exception as e:
                        print('ERROR:[', e, ']')
        inner_exe(bsm)
        return dfs

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


    def create_model_data(self, dfs):
        pricedf = dfs['steelprice']
        # 以钢材价格的时间周期取值
        begin = pricedf['updatetime'].min()
        end = pricedf['updatetime'].max()
        model = pd.DataFrame()
        for col in dfs.keys():
            model[col] = pd.Series()
        model['time'] = pd.Series()
        model['time'] = pricedf['updatetime']
        for ele in self._table_names:
            if ele not in dfs:
                self._table_names.remove(ele)
        i = 0
        for row in model.index:
            cur_time = model.ix[row, 'time']
            for tname in self._table_names:
                eledf = dfs[tname]
                try:
                    value = eledf[eledf[self._time_fields.get(tname, None)] == cur_time]
                    # model.ix[row, tname] = value[price_field.get(tname, None)]
                except Exception as e:
                    print('ERROR:[', e, ']')
                if len(value) > 0:
                    try:
                        price = value[self._price_field.get(tname, None)]
                        model.ix[row, tname] = list(price)[0]
                    except Exception as e:
                        print('ERROR:[', e, ']')
                    if i % 50 == 0:
                        pass
                    i = i + 1
        print(i)
        return model

    # 清洗异常数据
    def dfs_preproccess(self, model):
        model_fill = model.fillna(method='ffill')
        model_fill = model_fill.fillna(method='bfill')

        def extra_unexcepted_symbol(x):
            if str(x).find('-') > -1:
                nums = str(x).split('-')
                print(len(nums))
                for i in range(len(nums)):
                    print(nums[i])
                    if not nums[i]:
                        nums[i] = 0
                return (float(nums[0]) + float(nums[1])) / 2
            else:
                return x

        for col in model_fill.columns:
            try:
                if col == 'fgzs':
                    model_fill[col] = model_fill[col].map(lambda x: x.replace(',', ''))
                if col != 'time':
                    model_fill[col] = model_fill[col].map(lambda x: extra_unexcepted_symbol(x))
                    model_fill[col] = model_fill[col].map(lambda x: float(x))
            except Exception as e:
                print("ERROR:[", e, ']')
        return model_fill

    # @models.transaction_decorator
    def _steelprice_custom(self, bsm):
        """定制steelprice选择条件，方便后续方法测试
        
        Args:
            bsm： models.BaseManage object
        Returns:
            desc：a list contains clumns
            rs: sql resulte
        """
        @models.transaction_decorator
        def inner_exe(bsm):
            sqlVO = dict()
            sqlVO['sql'] = 'SELECT * FROM steelprice where region=%s and factory=%s and delivery=%s and steeltype=%s\
                    and tradeno=%s and specification=%s  and updatetime >= %s and updatetime <= %s'
            history_begin = "2010-06-03"
            history_end = "2017-10-14"
            params = ['全国', '鞍钢', '热轧', '弹簧钢', '65Mn', 'Φ6.5-25']
            params.append(datetime.datetime.strptime(history_begin, '%Y-%m-%d'))
            params.append(datetime.datetime.strptime(history_end, '%Y-%m-%d'))
            sqlVO['vars'] = params
            global desc, rs
            desc = bsm.direct_get_description(sqlVO)
            rs = bsm.select_single(sqlVO)

        inner_exe(bsm)
        return desc, rs


    def test_steelprice_custom(self, bsm):
        return self._steelprice_custom(bsm)
    
    def standard_split_train_test(self, *data, test_ratio=0.1, random_state=None):
        """sklearn.select_model的方法进行训练集和测试集的划分
        
        Args:
            *data, test_ratio,
            random_state: 每次传入相同的int值以保证得到相同的随机序列
           
        Returns:
            datas(data_train, data_test[, labels_train, labels_test])
        """
        return train_test_split(*data, test_size=test_ratio, random_state=random_state)
        

    def _shuffled_split_train_test(self, data, test_ratio):
        """随机生成索引序列，按比例生成训练数据集和测试数据集
        
        Args:
            data:array like
            test_ratio: float
           
        Returns:
            train_data, test_data
        """
        shuffled_indices = np.random.permutation(len(data)) # 序列，排列 permutation(5) [4,2,3,0,1]
        test_set_size = int(len(data) * test_ratio)
        test_indices = shuffled_indices[:test_set_size]
        train_indices = shuffled_indices[test_set_size:]
        return data.iloc[train_indices], data.iloc[test_indices]



    def load_data(self, filename):
        csv_path = os.path.join(BASE_DIR, filename)
        return pd.read_csv(csv_path)

# TODO 增加一些数据可视化及洞见数据特征的一些方法，
class Data_Discover_Visualize(object):
    pass


'''
条件筛选？
housing["income_cat"].where(housing["income_cat"] < 5, 5.0, inplace=True)
'''

if __name__ == '__main__':
    data = Data_Preparetion()
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QinggangManageSys.settings")
    # pass