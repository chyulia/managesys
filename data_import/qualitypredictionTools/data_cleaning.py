import os
import datetime, time

import numpy as np
import pandas as pd

#from sklearn.cross_validation import train_test_split


def get_history_price(path,begin,end,yinsu_type):
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




