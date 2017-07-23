import csv,datetime
from sklearn.cluster import k_means
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import ensemble
from sklearn.externals import joblib
from data_import.qualitypredictionTools.elm import ELMClassifier, ELMRegressor, GenELMClassifier, GenELMRegressor
from data_import.qualitypredictionTools.random_layer import RandomLayer, MLPRandomLayer, RBFRandomLayer, GRBFRandomLayer
from math import sqrt
import math

'''
传入数据和各种配置文件
path_lf：传入的炉次数据
heatno：炉次号
path_kmeans：kmeans分类模型
path_k：kmeans对应的分类的预测模型
path_origin：各分类的平均值和方差数据
'''
def predict_lf_temp(data_lf,path_kmeans,path_k,path_origin):

	# data = pd.read_csv(path_lf, encoding = 'gbk')
	# data_origin = pd.read_csv(path_origin, encoding = 'gbk')
	# # data = data.dropna()
	# data = data.drop(['TIME4','TIME5','TIME9','TIME10','TIME11','TIME12'],axis=1)
	# if data.columns[0] == 'Unnamed: 0':
	#     data = data.drop('Unnamed: 0',axis=1)
	# if data.columns[0] == 'Unnamed: 0.1':
	#     data = data.drop('Unnamed: 0.1',axis=1)
	print(data_lf)
	data = data_lf
	print(data_lf['shl'])
	data1 = data.copy()

	data2 = data.copy()
	data2 = data2.fillna(0)
	data2 = data2.ix[:,['TOTSENDPOWERTIME','C_1','TEMPOFARRIVE','CONSUMINGPOWER']]
	data2 = data2.ix[:,['C_1','C_1','TEMPOFARRIVE','CONSUMINGPOWER']]
	print(data2)

	data_heat = data1.fillna(0)
	data_feature = data_heat.ix[:,['TOTSENDPOWERTIME','C_1','TEMPOFARRIVE','CONSUMINGPOWER']]
	data_feature = 1.0*(data_feature-data2.mean())/data2.std()
	model = joblib.load(path_kmeans)	
	y_predict = model.predict(data_feature)
	y_predict = int(y_predict)
	if y_predict == 0:
		path_kk = path_k[0]
		mean = data_origin['mean1']
		std = data_origin['std1']
	if y_predict == 1:
		path_kk = path_k[1]
		mean = data_origin['mean2']
		std = data_origin['std2']
	if y_predict == 2:
		path_kk = path_k[2]
		mean = data_origin['mean3']
		std = data_origin['std3']
	print(path_kk)
	data_predict = data_heat.drop(['TEMPOFTAPPING'],axis=1)
	rf = joblib.load(path_kk)
	y_predict = rf.predict(data_predict)
	y_predict_final = np.array(y_predict).copy()
	row_num = y_predict_final.shape[0]

	print(mean,std)
	for xi in range(row_num):
		data_predict =y_predict_final[xi]*std  + mean
	print('222222222')
	print(int(data_predict))

	# print(ture_heat,y_predict_final)

	result = {}
	# result["data_ture"] = int(data_ture)
	result["data_predict"] = int(data_predict)
	# print(result)
	return result
