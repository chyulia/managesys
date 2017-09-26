# -*- coding: utf-8 -*-
import json
import logging
import sys

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import pandas as pd

from data_import.PricePredict.data_cleaning import get_history_price,create_single_model,get_stone_history_price,get_all_history_select
import data_import.PricePredict.PredictModels as PredictModels
from data_import.PricePredict.predict_day import predict_day
from data_import.PricePredict.predict_yue import predict_yue
from data_import.PricePredict.pre_config import steel_type,predict_method,time_scale,\
	INFO,WARNING,model_classname,iron_type,stone_predict_method,yinsu_type
from data_import import models,util
'''
预测相关方法在SteelPricePredict文件夹中
'''
try:
    logger = logging.getLogger('django')
except:
    pass

media_root = settings.MEDIA_ROOT
data_root = media_root + '/files/data/'

def steelprice(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	logger.debug(media_root)

	logger.debug(steel_type)
	logger.debug(predict_method)
	contentVO={
		'title':'钢材价格预测',
		'state':'success'
	}
	sqlVO = dict()
	tname = 'steelprice'
	sql = 'SELECT * FROM {0}'.format(tname)
	sqlVO['sql'] = sql
	desc = models.BaseManage().direct_get_description_only(sqlVO)
	print(desc)
	rs = models.BaseManage().direct_select_query_sqlVO(sqlVO)
	## rs为tuple，每一行记录也是tuple
	if rs:
		print(rs[:5])
		df = pd.DataFrame(rs, columns=pd.Series(desc[0]))
	all_select,choose_col = get_all_history_select(df)
	# choose_col = ('steeltype', 'tradeno', 'delivery', 'specification', 'factory', 'region')
	print(all_select)
	for col in choose_col:
		contentVO[col] = all_select[col]

	contentVO["steel_type"] = steel_type
	contentVO["predict_method"] = predict_method
	contentVO['time_scale'] = time_scale
	contentVO['info'] = INFO
	contentVO['warning'] = WARNING
	return render(request,'data_import/steelprice.html',contentVO)



def price_history(request):
    if not request.user.is_authenticated():
    	return HttpResponseRedirect("/login")
    if request.method == 'POST':
    	history_begin =	request.POST.get('history_begin', '')
    	history_end =	request.POST.get('history_end', '')
    path = data_root + 'tegang.csv'
    prices = get_history_price(path,history_begin,history_end)
    attrs = util.get_model_attrs(models.steelprice)
    print(attrs)
    sqlVO =util.create_select_condition({'tradeno':'65Mn','factory':'济源钢铁'})
    rs = models.BaseManage().direct_select_query_orignal_sqlVO(sqlVO)
    print(rs)
    logger.debug(type(prices.get('price',None)[0]))

    contentVO={
    	'title':'钢材历史价格',
    	'state':'success'
    }
    contentVO['timeline'] = prices.get('timeline',None)
    contentVO['price'] = prices.get('price',None)
    return HttpResponse(json.dumps(contentVO), content_type='application/json')

def init_models(modelname):
	model = None
	class_name =None
	#通过类名反射相应的类，暂未实例化
	try:
		class_name = model_classname[modelname]
		print(class_name)
		try:
			model = getattr(PredictModels,class_name)
		except:
			print('init model ',class_name,' failed.')
			print(sys.exc_info()[0])
			return {modelname:model}
	except:
		print('no such key name',modelname)
	return {modelname:model}

def price_predict(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		'''
		获取对应参数
		'''
		steelType =	request.POST.get('steelType', '')
		timeScale =	request.POST.get('timeScale', '')
		typestr =	request.POST.get('typestr', '')
		if typestr != "":
			types = typestr.split(',')
	'''
	根据参数选择模型
	结果返回预测数据时间跨度，预测值，真实值，score值
	对应不同的模型，每个模型存放在一张字典表中
	外层是由模型名为key的字典表result={"ELM":{"timeline":xxx,"predict_value":xxxx,\
	"true_value":xxxx,"score":xxxx},"SVM":{},"linear_regression":{}}
	'''
	models_result = {}
	path = data_root + 'tegang.csv'
	PRE_DAYS = [5]
	models_data = create_single_model(path,PRE_DAYS)
	logger.debug(len(models_data))
	models = map(init_models,types)
	models = list(models)
	logger.debug(models)
	for index in range(len(models)):
		for method, model in models[index].items():
			if model is not None:
				result = model().predict(models_data[0],0.4)
				models_result[method] = result
	# logger.debug(models_result)

	contentVO={
		'title':'钢材价格预测',
		'state':'success'
	}
	contentVO["result"] = models_result
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

'''
预测相关方法在ironstonepriceTools文件夹中
'''


def ironstoneprice(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	print(media_root)
	'''
	加载铁矿石种类，及可选的预测方法
	'''
	print(iron_type)
	print(predict_method)
	contentVO={
		'title':'铁矿石价格预测',
		'state':'success'
	}
	contentVO["yinsu_type"] = yinsu_type
	contentVO["iron_type"] = iron_type
	contentVO["predict_method"] = stone_predict_method
	contentVO['time_scale'] = time_scale
	return render(request,'data_import/ironstoneprice.html',contentVO)



def stone_price_history(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		history_begin =	request.POST.get('history_begin', '')
		history_end =	request.POST.get('history_end', '')
		yinsu_type =	request.POST.get('yinsu_type', '')
	path = data_root + 'tkszs_yinsu.csv'
	# path = data_root + 'tegang.csv'
	prices = get_stone_history_price(path,history_begin,history_end,yinsu_type)
	# prices['timeline'] = []
	# prices['price'] = []
	# print(type(prices.get('price',None)[0]))

	contentVO={
		'title':'铁矿石历史价格',
		'state':'success'
	}
	contentVO['timeline'] = prices.get('timeline',None)
	contentVO['price'] = prices.get('price',None)
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

def stone_price_predict(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		'''
		获取对应参数
		'''
		steelType =	request.POST.get('steelType', '')
		# print(steelType)
		timeScale =	request.POST.get('timeScale', '')
		typestr =	request.POST.get('typestr', '')
		if typestr != "":
			types = typestr.split(',')
			print(types)
	if steelType=='tkszs':
		print('this is tkszs')
	'''
	根据参数选择模型
	结果返回预测数据时间跨度，预测值，真实值，score值
	对应不同的模型，每个模型存放在一张字典表中
	外层是由模型名为key的字典表result={"ELM":{"timeline":xxx,"predict_value":xxxx,\
	"true_value":xxxx,"score":xxxx},"SVM":{},"LR":{}}
	'''
	# path = data_root + 'tegang.csv'
	path_iron = data_root + 'tkszs_yinsu.csv'
	path_iron_yue = data_root + 'qdg_time.csv'
	# PRE_DAYS = [5]
	# models_data = create_single_model(path,PRE_DAYS)
	# print(len(models_data))
	models_result = {}
	if timeScale == "day":
		for i in range(len(types)):
			# print(types[i])
			if types[i] == "elm":
				print(types[i])
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result
			if types[i] == "logistic_regression":
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result
			if types[i] == "svm":
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result
			if types[i] == "random_forest":
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result
	if timeScale == "month":
		for i in range(len(types)):
			# print(types[i])
			if types[i] == "elm":
				print(types[i])
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result
			if types[i] == "logistic_regression":
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result
			if types[i] == "svm":
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result
			if types[i] == "random_forest":
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result
	contentVO={
		'title':'钢材价格预测',
		'state':'success'
	}
	contentVO["result"] = models_result
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

if __name__ == '__main__':
	types = []
	types.append('elm')

