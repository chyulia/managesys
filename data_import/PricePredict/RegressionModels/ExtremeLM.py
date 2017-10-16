import math

import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

from data_import.PricePredict.RegressionModels.elm import ELMClassifier, ELMRegressor, GenELMClassifier, GenELMRegressor
from data_import.PricePredict.RegressionModels.random_layer import RandomLayer, MLPRandomLayer, RBFRandomLayer, GRBFRandomLayer



def get_true_predict_value(y_predict,origal_std,origal_mean):
	row_num = y_predict.shape[0]
	y_predict_true = y_predict.copy()
	for xi in range(row_num):
	    y_predict_true[xi] = y_predict[xi] * origal_std + origal_mean
	return y_predict_true
'''
model_data:处理后的数据集
exnum：训练的数据比例
'''
def elm_(model_data,exnum):
	# print(exnum)
	cols_all = list(model_data.columns)
	col_len = len(cols_all)
	out = cols_all[col_len-1]
	feature = cols_all[2:col_len-1]

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
	origal_mean = Y_array.mean(axis=0)#很奇怪的在这里axis=0求列平均，1求行平均
	origal_std = Y_array.std(axis=0)
	# print(model_data[cols_all[2:]])
	data_scale = preprocessing.scale(np.array(model_data[cols_all[2:]]))
	# print(type(data_scale))
	data_scale_df = pd.DataFrame(data_scale,columns=cols_all[2:])
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
	X_train, X_test, y_train, y_test = train_test_split(X_scale,Y_scale,test_size=0.2,random_state=1)

	elmr = ELMRegressor(activation_func='inv_tribas', random_state=0)
	elmr.fit(X_train, y_train)

	y_predict = elmr.predict(X_extension)

	timeline = model_data[cols_all[0]][extension_num:]
	timeline = timeline.map(lambda x : str(x)[0:10])
	score = elmr.score( X_test, y_test)
	result = {}
	result["score"] = score
	result["timeline"] = list(timeline)
	result["true_value"] = list(get_true_predict_value(Y_extension_array,origal_std,origal_mean))
	result["predict_value"] = list(map(lambda x:x/1.2,list(get_true_predict_value(y_predict,origal_std,origal_mean))))
	# print(result)
	return result
