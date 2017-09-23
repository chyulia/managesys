import os
import datetime, time

import numpy as np
import pandas as pd


#from sklearn.cross_validation import train_test_split



def get_history_price(path,begin,end):
	dfori = pd.read_csv(path, encoding = 'gbk')
	cols = list(dfori.columns)
	cols_len = len(cols)
	print(path)
	print(begin)
	print(end)
	'''
	时间字符串转时间格式
	'''
	begin = datetime.datetime.strptime(begin, '%Y-%m-%d')
	end = datetime.datetime.strptime(end, '%Y-%m-%d')

	'''
	datetime format
	'''
	dfori[cols[0]] = dfori[cols[0]].map(lambda x : str(x))
	dfori[cols[0]] = dfori[cols[0]].map(lambda x : datetime.datetime.strptime(x, '%Y%m%d'))

	dfori[cols[1]] = pd.to_numeric(dfori[cols[1]].map(lambda x : x.replace(',','')))
	'''
	根据起止时间选择数据
	'''
	dfori = dfori[(dfori[cols[0]] > begin) & (dfori[cols[0]] < end)]

	history_price = pd.DataFrame()
	history_price = dfori[cols[0:2]]
	result = {}
	history_price[cols[0]] = history_price[cols[0]].map(lambda x : str(x)[0:10])
	result['timeline'] = list(history_price[cols[0]])
	result['price'] = list(history_price[cols[1]])
	return result

def create_single_model(path,PRE_DAYS):
	'''
	120视为半年24周
	'''
	#,80,100,120,240,360
	dfori = pd.read_csv(path, encoding = 'gbk')
	cols = list(dfori.columns)
	cols_len = len(cols)

	dfori[cols[1]] = pd.to_numeric(dfori[cols[1]].map(lambda x : x.replace(',','')))

	'''
	datetime format
	'''

	dfori[cols[0]] = dfori[cols[0]].map(lambda x : str(x))
	dfori[cols[0]] = dfori[cols[0]].map(lambda x : datetime.datetime.strptime(x, '%Y%m%d'))


	'''
	初始化数据集
	model['end'] = dfori[cols[0]][:len(dfori.index)- PRE_DAYS[i] ] + datetime.timedelta(days= PRE_DAYS[i])
	这种时间拼接方式的漏洞在于会凭空增加没有数据的日期
	'''
	models = []
	for i in range(len(PRE_DAYS)):
	    day = PRE_DAYS[i]
	    model = pd.DataFrame()
	    model['begin'] = dfori[cols[0]][:len(dfori.index)-day]
	    model['end'] = pd.Series()
	    for m in range(len(model['begin'])):
	        model.ix[m,'end'] = dfori.ix[m + day,cols[0]]
	    models.append(model.copy())
	'''
	按照天数组织数据，得到训练第一层模型所需要的数据集，训练数据比例以最长天数为基准取0.4比例保留，其他数据集参照
	'''
	for i in range(len(PRE_DAYS)):
		day = PRE_DAYS[i]
		for k in range(len(dfori.index)-day):
		    models[i].ix[k, str(day) + 'plus0'] = dfori.ix[k,cols[1]]
		    for j in range(day):
		        models[i].ix[k, str(day) + 'plus' + str(j+1)] = dfori.ix[k+j+1,cols[1]]
	return models

def create_models(path,PRE_DAYS):

	# path = os.path.dirname(os.path.abspath('__file__'))

	'''
	120视为半年24周
	'''

	#,80,100,120,240,360
	dfori = pd.read_csv(path, encoding = 'gbk')
	cols = list(dfori.columns)
	cols_len = len(cols)

	dfori[cols[1]] = pd.to_numeric(dfori[cols[1]].map(lambda x : x.replace(',','')))

	'''
	datetime format
	'''

	dfori[cols[0]] = dfori[cols[0]].map(lambda x : str(x))
	dfori[cols[0]] = dfori[cols[0]].map(lambda x : datetime.datetime.strptime(x, '%Y%m%d'))


	'''
	初始化数据集
	model['end'] = dfori[cols[0]][:len(dfori.index)- PRE_DAYS[i] ] + datetime.timedelta(days= PRE_DAYS[i])
	这种时间拼接方式的漏洞在于会凭空增加没有数据的日期
	'''
	models = []
	for i in range(len(PRE_DAYS)):
	    day = PRE_DAYS[i]
	    model = pd.DataFrame()
	    model['begin'] = dfori[cols[0]][:len(dfori.index)-day]
	    model['end'] = pd.Series()
	    for m in range(len(model['begin'])):
	        model.ix[m,'end'] = dfori.ix[m + day,cols[0]]
	    models.append(model.copy())
	'''
	按照天数组织数据，得到训练第一层模型所需要的数据集，训练数据比例以最长天数为基准取0.4比例保留，其他数据集参照
	'''
	for i in range(len(PRE_DAYS)):
		day = PRE_DAYS[i]
		for k in range(len(dfori.index)-day):
		    models[i].ix[k, str(day) + 'plus0'] = dfori.ix[k,cols[1]]
		    for j in range(day):
		        models[i].ix[k, str(day) + 'plus' + str(j+1)] = dfori.ix[k+j+1,cols[1]]

	'''
	 使用elm分别建立模型
	 PRE_DAYS = [1,2,5,10,15,20,40,60]
	'''


	'''
	得到训练第二层模型所需要的数据集
	'''
	pre_model_data = pd.DataFrame()
	mlength = len(PRE_DAYS)

	standatd_model = models[mlength-1]
	standatd_model_cols = list(standatd_model)
	'''
	终止时间及当天的价格为最终所需预测值
	'''
	nicecols = [standatd_model_cols[1],standatd_model_cols[-1]]
	pre_model_data[[standatd_model_cols[1],'outprice']] = standatd_model[nicecols].copy()

	'''
	对每一个数据集进行合并，按照end日期合并数据
	'''

	for i in range(len(PRE_DAYS)):
	    mergecols = list(models[i].columns)[2:len(models[i].columns)]
	    '''
	    初始化列
	    '''
	    for col in mergecols:
	        pre_model_data[col] = pd.Series()
	    '''
	    按照end匹配并填充数据
	    '''
	    for date in pre_model_data['end']:   
	        index = pre_model_data[pre_model_data['end'] == date].index[0]
	        for col in mergecols:
	            value = models[i][models[i]['end'] == date][col].values
	            if len(value) > 0:
	                pre_model_data.ix[index,col] = value[0]
	
	print(pre_model_data.head(5))

	return pre_model_data,models,len(standatd_model)

def get_stone_history_price(path,begin,end,yinsu_type):
	dfori = pd.read_csv(path, encoding = 'gbk')
	dfori = dfori.dropna()
	cols = list(dfori.columns)
	cols_len = len(cols)

	'''
	时间字符串转时间格式
	'''
	# begin= '2005-05-01'
	# end= '2015-05-01'
	begin = datetime.datetime.strptime(begin, '%Y-%m-%d')
	end = datetime.datetime.strptime(end, '%Y-%m-%d')
	print(yinsu_type)
	print(type(yinsu_type))
	'''
	datetime format
	'''
	dfori['date'] = dfori['date'].map(lambda x : str(x))
	dfori['date'] = dfori['date'].map(lambda x : datetime.datetime.strptime(x, '%Y/%m/%d'))

	dfori[yinsu_type] = pd.to_numeric(dfori[yinsu_type])
	'''
	根据起止时间选择数据
	'''
	dfori = dfori[(dfori['date'] > begin) & (dfori['date'] < end)]
	history_price = pd.DataFrame()
	history_price = dfori[['date',yinsu_type]]
	result = {}
	history_price['date'] = history_price['date'].map(lambda x : str(x)[0:10])
	result['timeline'] = list(history_price['date'])
	result['price'] = list(history_price[yinsu_type])
	return result

if __name__ == '__main__':
	create_models([10])

