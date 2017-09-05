from time import time
import csv,datetime
from sklearn.cluster import k_means
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn import linear_model
from data_import.ironstonepriceTools.elm import ELMClassifier, ELMRegressor, GenELMClassifier, GenELMRegressor
from data_import.ironstonepriceTools.random_layer import RandomLayer, MLPRandomLayer, RBFRandomLayer, GRBFRandomLayer
from math import sqrt

import math

'''
predict（）:预测函数
shuchu：预测值
data：传入的数据

'''
def predict(shuchu,data,algorithm):
	# print('222')
	output = [shuchu]
	Y = data[shuchu]
	Y_array=np.array(Y)
	origal_mean=Y_array.mean(axis=0)#0表示列，1表示行
	origal_std=Y_array.std(axis=0)
	columns = list(data.columns)
	columns_feature=columns.copy()
	out_and_else = ['tkszs_l1','tkszs_l2','tkszs_l3']
	for col in out_and_else:
	    columns_feature.remove(col)
	data_scale=preprocessing.scale(np.array(data))
	data_scale_df=pd.DataFrame(data_scale,columns=columns)
	X_scale=data_scale_df[columns_feature]
	Y_scale=data_scale_df[output]
	x_train = X_scale[0:-3]
	y_train = Y_scale[0:-3]
	data_index = data.index
	x_test = X_scale.loc[list(data_index)[-1]]
	x_train = np.array(x_train)
	y_train = np.array(y_train)
	# algorithm：算法
	if algorithm == "logistic_regression":
		algorithm = linear_model.LinearRegression()
	# algorithm = linear_model.SGDRegressor(loss='squared_loss')
	if algorithm == "svm":
		algorithm = svm.SVR()
	if algorithm == "random_forest":
		algorithm = ensemble.RandomForestRegressor(n_estimators=20)

	if algorithm == "elm":
		algorithm = ELMRegressor(activation_func='inv_tribas', random_state=0)




	rf1 = algorithm
	rf1.fit(x_train,y_train)
	y_predict_1 = rf1.predict(x_test)
	y_predict_final = np.array(y_predict_1).copy()
	row_num = y_predict_final.shape[0]
	for xi in range(row_num):
	    y_predict_final[xi]=y_predict_final[xi]*origal_std+origal_mean
	return y_predict_final
'''
传入数据
algorithm：选择的算法
'''
def predict_day(path,algorithm):
	data = pd.read_csv(path, encoding = 'gbk')
	# data = data.dropna()
	data1 = data.copy()
	if data.columns[0] == 'Unnamed: 0':
	    data = data.drop('Unnamed: 0',axis=1)
	data = data.drop(['date','psjgzs','feigang','haiyun_BDI','haiyun_BDTI','pugang_zhishu','tegang_zonghe_zhishu','meiyuan'],axis=1)
	algorithm = linear_model.SGDRegressor(loss='squared_loss')
	# 输入的时间序列
	data_index = data1.index
	data_last10 = data1.loc[list(data_index)[-10:]]
	data_last10['date'] = data_last10['date'].map(lambda x : str(x))
	data_last10['date'] = data_last10['date'].map(lambda x : datetime.datetime.strptime(x, '%Y/%m/%d'))
	data_last10['date'][data_last10.index[-1]+1]=data_last10['date'][data_last10.index[-1]]+datetime.timedelta(days=1)
	data_last10['date'][data_last10.index[-1]+2]=data_last10['date'][data_last10.index[-1]+1]+datetime.timedelta(days=1)
	data_last10['date'][data_last10.index[-1]+3]=data_last10['date'][data_last10.index[-1]+2]+datetime.timedelta(days=1)
	list_time = []
	a = data_last10['date']
	for i in a:
	    list_time.append(str(i)[0:10])
	# 历史值
	data_tkszs_10 = data1.loc[list(data_index)[-10:]]
	data_tkszs_10['tkszs_qdg'][data_tkszs_10.index[-1]+1]='-'
	data_tkszs_10['tkszs_qdg'][data_tkszs_10.index[-1]+2]='-'
	data_tkszs_10['tkszs_qdg'][data_tkszs_10.index[-1]+3]='-'
	# 预测值
	list_predict = ['-','-','-','-','-','-','-','-','-']
	list_predict.append(0)
	list_predict.append(round(float(predict( 'tkszs_l1',data,algorithm)),1))
	list_predict.append(round(float(predict( 'tkszs_l2',data,algorithm)),1))
	list_predict.append(round(float(predict( 'tkszs_l3',data,algorithm)),1))
	result = {}
	result["score"] = 0.4
	result["timeline"] = list_time
	result["true_value"] = list(data_tkszs_10['tkszs_qdg'])
	result["predict_value"] = list_predict
	# print(result)
	return result
