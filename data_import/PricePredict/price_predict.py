#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import sys


from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from data_import import const
from data_import.PricePredict.data_cleaning import create_single_model, get_stone_history_price
import data_import.PricePredict.PredictModels as PredictModels
from data_import.PricePredict.predict_day import predict_day
from data_import.PricePredict.predict_yue import predict_yue
from data_import.PricePredict.pre_config import ELE_INFOS, steel_type, predict_method, time_scale, \
    INFO, WARNING, model_classname, iron_type, stone_predict_method, yinsu_type, choose_col_meaning, all_select
from data_import import models, util
from data_import.PricePredict import data_preparetion

'''
预测相关方法在SteelPricePredict文件夹中
'''
try:
    logger = logging.getLogger('django')
except:
    pass

media_root = settings.MEDIA_ROOT
data_root = os.path.join(media_root, 'files', 'data')

def steelprice(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    logger.debug(media_root)

    logger.debug(steel_type)
    logger.debug(predict_method)
    dc = data_preparetion.DataCleaning()
    contentVO = {
        'title': '钢材价格预测',
        'state': 'success'
    }
    # df = dc.valid_steel_data_by_time()
    #  从数据库里读取,可以写到配置文件里，减少读取时间，增加缓存，减少参数初始化时间
    all_select,choose_col = dc.get_all_history_select()
    # choose_col = ('steeltype', 'tradeno', 'delivery', 'specification', 'region', 'factory')
    predict_all_select = all_select.copy()
    predict_all_select.pop('region')
    for col in choose_col:
        contentVO[col] = all_select[col]
    # model_selcet_eles = ['steeltype', 'tradeno', 'delivery','specification']
    contentVO['all_select'] = all_select
    contentVO['predict_all_select'] = predict_all_select
    contentVO["steel_type"] = steel_type
    contentVO['choose_col'] = choose_col
    contentVO['choose_col_meaning'] = choose_col_meaning
    contentVO["predict_method"] = predict_method
    contentVO['time_scale'] = time_scale
    contentVO['info'] = INFO


    contentVO['warning'] = WARNING
    return render(request, 'data_import/steelprice.html', contentVO)

def price_history(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    contentVO = {
        'title': '钢材历史价格',
    }
    dc = data_preparetion.DataCleaning()
    if request.method == 'POST':
        pop_no_op = ['csrfmiddlewaretoken', 'steel_type']
        print(dict(request.POST))
        params, history_begin, history_end = dc.first_ele(dict(request.POST), pop_no_op=pop_no_op)
    print(params)
    rs = dc.format_data(params, history_begin, history_end)
    #
    if rs is not None:
        print(len(rs))
        prices_ = dc.data_to_display(rs)
        contentVO['timeline'] = prices_[0]
        contentVO['price'] = prices_[1]
        contentVO['state'] = const.OK.get('code', 0)  # 前端检测state状态，匹配message信息进行相应处理
    else:
        contentVO["his_warnning"] = "该筛选条件下无合适数据"
        contentVO['state'] = const.COMMON.INVALID_PARAM.get('code', None)

    # contentVO['timeline'] = prices.get('timeline', None)
    # contentVO['price'] = prices.get('price', None)
    contentVO['ele_info'] = ELE_INFOS.get('steel')
    return HttpResponse(json.dumps(contentVO), content_type='application/json')


def init_models(modelname):
    model = None
    class_name = None
    # 通过类名反射相应的类，暂未实例化
    try:
        class_name = model_classname[modelname]
        print(class_name)
        try:
            model = getattr(PredictModels, class_name)
        except:
            print('init model ', class_name, ' failed.')
            print(sys.exc_info()[0])
            return {modelname: model}
    except:
        print('no such key name', modelname)
    return {modelname: model}


# FIXME
def price_predict(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    dc = data_preparetion.DataCleaning()

    if request.method == 'POST':
        pop_no_op = ['csrfmiddlewaretoken', 'steel_type', 'timeScale']
        print(dict(request.POST))
        steelType = request.POST.get('steelType', '')
        timeScale = request.POST.get('timeScale', '')
        params, history_begin, history_end = dc.first_ele(dict(request.POST), pop_no_op=pop_no_op)
    print(params)
    rs = dc.format_data(params)

    if request.method == 'POST':
        '''
        获取对应参数,增加钢厂，牌号参数
        '''
        steelType = request.POST.get('steelType', '')
        timeScale = request.POST.get('timeScale', '')
        typestr = request.POST.get('typestr', '')
        if typestr != "":
            types = typestr.split(',')
    # TODO 设定有限的缓存模型，比如钢种，地区，规格，钢厂，提前生成csv文件会不会是一个比较好的处理方式？
    # TODO 根据参数选择缓存的模型，获取系统时间检索数据，代入回归模型获得预测值
    # FIXME
    ''' 
    根据参数选择模型
    结果返回预测数据时间跨度，预测值，真实值，score值
    对应不同的模型，每个模型存放在一张字典表中
    外层是由模型名为key的字典表result={"ELM":{"timeline":xxx,"predict_value":xxxx,\
    "true_value":xxxx,"score":xxxx},"SVM":{},"linear_regression":{}}
    '''
    models_result = {}

    # TODO 根据日月的预测选择，生成输入预测模型的数据

    models_data = None
    logger.debug(len(models_data))
    models = map(init_models, types)
    models = list(models)
    # TODO 得到每个模型的预测结果就好了
    for index in range(len(models)):
        for method, model in models[index].items():
            if model is not None:
                result = model().predict(models_data)
                models_result[method] = result
    # logger.debug(models_result)
    print(models_result.keys())
    contentVO = {
        'title': '钢材价格预测',
        'state': 'success'
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
    contentVO = {
        'title': '铁矿石价格预测',
        'state': 'success'
    }
    contentVO["yinsu_type"] = yinsu_type
    contentVO["iron_type"] = iron_type
    contentVO["predict_method"] = stone_predict_method
    contentVO['time_scale'] = time_scale
    return render(request, 'data_import/steelprice_temp.html', contentVO)

# TODO 根据yinsu_type选取相应描述
def stone_price_history(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        history_begin = request.POST.get('history_begin', '')
        history_end = request.POST.get('history_end', '')
        yinsu_type = request.POST.get('yinsu_type', '')
    path = data_root + 'tkszs_yinsu.csv'
    # path = data_root + 'tegang.csv'
    prices = get_stone_history_price(path, history_begin, history_end, yinsu_type)
    # prices['timeline'] = []
    # prices['price'] = []
    # print(type(prices.get('price',None)[0]))

    contentVO = {
        'title': '铁矿石历史价格',
        'state': 'success'
    }
    contentVO['ele_info'] = ELE_INFOS.get(yinsu_type, None)
    contentVO['timeline'] = prices.get('timeline', None)
    contentVO['price'] = prices.get('price', None)
    return HttpResponse(json.dumps(contentVO), content_type='application/json')


def stone_price_predict(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        '''
        获取对应参数
        '''
        steelType = request.POST.get('steelType', '')
        # print(steelType)
        timeScale = request.POST.get('timeScale', '')
        typestr = request.POST.get('typestr', '')
        if typestr != "":
            types = typestr.split(',')
            print(types)
    if steelType == 'tkszs':
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
                result = predict_day(path_iron, types[i])
                models_result["zhi"] = result
            if types[i] == "logistic_regression":
                result = predict_day(path_iron, types[i])
                models_result["zhi"] = result
            if types[i] == "svm":
                result = predict_day(path_iron, types[i])
                models_result["zhi"] = result
            if types[i] == "random_forest":
                result = predict_day(path_iron, types[i])
                models_result["zhi"] = result
    if timeScale == "month":
        for i in range(len(types)):
            # print(types[i])
            if types[i] == "elm":
                print(types[i])
                result = predict_yue(path_iron_yue, types[i])
                models_result["zhi"] = result
            if types[i] == "logistic_regression":
                result = predict_yue(path_iron_yue, types[i])
                models_result["zhi"] = result
            if types[i] == "svm":
                result = predict_yue(path_iron_yue, types[i])
                models_result["zhi"] = result
            if types[i] == "random_forest":
                result = predict_yue(path_iron_yue, types[i])
                models_result["zhi"] = result
    contentVO = {
        'title': '钢材价格预测',
        'state': 'success'
    }
    contentVO["result"] = models_result
    return HttpResponse(json.dumps(contentVO), content_type='application/json')


if __name__ == '__main__':
    types = []
    types.append('elm')
# {'sql': 'SELECT * FROM steelprice where region=%s and tradeno=%s and factory=%s '
#         'and specification=%s and delivery=%s and steeltype=%s and updatetime >= %s and updatetime <= %s',
#  'vars': ['全国', '65Mn', '鞍钢', 'Φ6.5-25', '热轧', '弹簧钢', datetime.datetime(2010, 6, 3, 0, 0), datetime.datetime(2017, 9, 22, 0, 0)]}