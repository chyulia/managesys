# -*- coding: utf-8 -*
import json
import numpy as np
import pandas as pd
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404

from data_import.qualitypredictionTools.data_cleaning import get_history_price
from data_import.qualitypredictionTools.predict_temp import predict_temp
from data_import.qualitypredictionTools.predict_lf_temp import predict_lf_temp
from data_import.qualitypredictionTools.pre_config import lf_type,predict_method,heatno,yinsu_type

'''
预测相关方法在qualitypredictionTools文件夹中
'''

media_root = settings.MEDIA_ROOT
data_root = media_root + '/files/data/quality/'
path_lf = data_root + 'LF_test3.csv'
path_kmeans = data_root + 'km.pkl'
path_k1 = data_root + 'rf1.pkl'
path_k2 = data_root + 'rf2.pkl'
path_k3 = data_root + 'rf3.pkl'
path_k = [path_k1,path_k2,path_k3]
path_origin = data_root + 'origin.csv'

def quality_prediction(request):
	if not request.user.is_authenticated():	
		return HttpResponseRedirect("/login")
	print(media_root)
	'''
	加载预测种类，及可选的预测方法
	'''
	# print(lf_type)
	# print(heatno)
	contentVO={
		'title':'炼钢质量预测',
		'state':'success'
	}
	contentVO["yinsu_type"] = yinsu_type
	contentVO["lf_type"] = lf_type
	contentVO["predict_method"] = predict_method
	contentVO['heatno'] = heatno
	return render(request,'data_import/qualityprediction.html',contentVO)



def lf_quality_history(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	
	if request.method == 'POST':
		data_lf = pd.DataFrame()
		ltype = request.POST.get('ltype', '')
		rcsj = request.POST.get('rcsj', '')
		ylzq = request.POST.get('ylzq', '')
		jzwd = request.POST.get('jzwd', '')
		dh = request.POST.get('dh', '')
		zsdsj = request.POST.get('zsdsj', '')
		alshl = request.POST.get('alshl', '')
		althl = request.POST.get('althl', '')
		chl = request.POST.get('chl', '')
		mnhl = request.POST.get('mnhl', '')
		shl = request.POST.get('shl', '')
		phl = request.POST.get('phl', '')
		wdc = request.POST.get('wdc', '')
		wdcs = request.POST.get('wdcs', '')
		tdcs = request.POST.get('tdcs', '')
		jlcs = request.POST.get('jlcs', '')
		hjwl = request.POST.get('hjwl', '')
		fjswl = request.POST.get('fjswl', '')
		data_lf['rcsj'] = [rcsj]
		data_lf['ylzq'] = [ylzq]
		data_lf['jzwd'] = [jzwd]
		data_lf['dh'] = [dh]
		data_lf['zsdsj'] = [zsdsj]
		data_lf['alshl'] = [alshl]
		data_lf['althl'] = [althl]
		data_lf['chl'] = [chl]
		data_lf['mnhl'] = [mnhl]
		data_lf['shl'] = [shl]
		data_lf['phl'] = [phl]
		data_lf['wdc'] = [wdc]
		data_lf['wdcs'] = [wdcs]
		data_lf['tdcs'] = [tdcs]
		data_lf['jlcs'] = [jlcs]
		data_lf['hjwl'] = [hjwl]
		data_lf['fjswl'] = [fjswl]
	print('111')
	print(ltype)
	print(data_lf['fjswl'])
	models_result = {}
	if ltype == "temp":	
		print('s!')
		result = predict_lf_temp(data_lf,path_kmeans,path_k,path_origin)
		models_result["zhi"] = result

	# path = data_root + 'tkszs_yinsu.csv'
	# path = data_root + 'tegang.csv'
	# prices = get_history_price(path,history_begin,history_end,yinsu_type)
	# prices['timeline'] = []
	# prices['price'] = []
	# print(type(prices.get('price',None)[0]))

	contentVO={
		'title':'lf价格预测',
		'state':'success'
	}
	contentVO["result"] = models_result
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

def lf_quality_predict(request):
	print('1111111111')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		'''
		获取对应参数
		'''
		lftype =	request.POST.get('lftype', '')
		# print(steelType)
		heatno =	request.POST.get('heatno', '')

	
	print(lftype,heatno)
	'''
	根据参数选择模型
	结果返回预测数据时间跨度，预测值，真实值，score值
	对应不同的模型，每个模型存放在一张字典表中
	外层是由模型名为key的字典表result={"ELM":{"timeline":xxx,"predict_value":xxxx,\
	"true_value":xxxx,"score":xxxx},"SVM":{},"LR":{}}
	'''
	# path = data_root + 'tegang.csv'
	# path_lf = data_root + 'LF_test3.csv'
	# path_kmeans = data_root + 'km.pkl'
	# path_k1 = data_root + 'rf1.pkl'
	# path_k2 = data_root + 'rf2.pkl'
	# path_k3 = data_root + 'rf3.pkl'
	# path_k = [path_k1,path_k2,path_k3]
	# path_origin = data_root + 'origin.csv'
	# path_iron_yue = data_root + 'qdg_time.csv'
	# PRE_DAYS = [5]
	# models_data = create_single_model(path,PRE_DAYS)
	# print(len(models_data))
	models_result = {}
	if lftype == "temp":	
		result = predict_temp(path_lf,heatno,path_kmeans,path_k,path_origin)
		models_result["zhi"] = result
				
			
	contentVO={
		'title':'测试',
		'state':'success',
	}
	contentVO["result"] = models_result
	print(contentVO)
	return HttpResponse(json.dumps(contentVO), content_type='application/json')