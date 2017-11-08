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
    INFO, WARNING, model_classname, iron_type, stone_predict_method, yinsu_type, choose_col_meaning, all_select, search_advice
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
    all_select = dc.get_all_steeltype()
    print(all_select)
    # choose_col = ('tradeno', 'delivery', 'specification', 'region', 'factory')
    choose_col = ('tradeno', 'region', 'factory', 'delivery', 'specification', )
    predict_all_select = all_select.copy()
    # predict_all_select.pop('region')
    # for col in choose_col:
    #     contentVO[col] = all_select[col]
    # model_selcet_eles = ['steeltype', 'tradeno', 'delivery','specification']
    all_select_pridict = dc.get_all_history_select("弹簧钢")
    contentVO['all_select'] = all_select
    contentVO['predict_all_select'] = predict_all_select
    contentVO['choose_col'] = choose_col
    contentVO['choose_col_meaning'] = choose_col_meaning
    contentVO["predict_method"] = predict_method
    contentVO['time_scale'] = time_scale
    contentVO['info'] = INFO
    contentVO['steel_type'] = steel_type
    contentVO['all_select_pridict'] = all_select_pridict


    contentVO['warning'] = WARNING
    return render(request, 'data_import/steelprice.html', contentVO)

def load_his_option(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    dc = data_preparetion.DataCleaning()
    contentVO = {
        'title': 'history options',
    }
    if request.method == 'POST':
        steel_type = request.POST.get('steeltype', '')
    all_select = dc.get_all_history_select(steel_type)
    print(all_select)
    contentVO['all_select'] = all_select
    return HttpResponse(json.dumps(contentVO), content_type='application/json')


def price_history(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    contentVO = {
        'title': '钢材历史价格',
    }
    dc = data_preparetion.DataCleaning()
    if request.method == 'POST':
        pop_no_op = ['csrfmiddlewaretoken']
        print(dict(request.POST))
        params, history_begin, history_end = dc.first_ele(dict(request.POST), pop_no_op=pop_no_op)
        tradeno = request.POST.get("tradeno",'')
    print(params)
    rs = dc.format_data(params, history_begin, history_end)
    if not rs:
        his_warnning = "该筛选条件下无合适数据<br/>"
        if tradeno !='':
            print(tradeno)
            his_warnning = his_warnning + "检索建议：<br/>"
            print(search_advice)
            search_advices = search_advice.get(tradeno)
        his_warnning  = his_warnning + str(search_advices)
        contentVO["his_warnning"] = his_warnning

        contentVO['state'] = const.COMMON.INVALID_PARAM.get('code', None)
    else:
        dfs = rs[1]
        #
        if dfs is not None:
            print(len(dfs))
            timeline, price = dc.data_to_display(dfs)
            contentVO['timeline'] = timeline
            contentVO['price'] = price
            contentVO['state'] = const.OK.get('code', 0)  # 前端检测state状态，匹配message信息进行相应处理
        else:
            contentVO["his_warnning"] = "该筛选条件下无合适数据"
            contentVO['state'] = const.COMMON.INVALID_PARAM.get('code', None)

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
    contentVO = {
        'title': '钢材价格预测',
    }
    dc = data_preparetion.DataCleaning()

    if request.method == 'POST':
        pop_no_op = ['csrfmiddlewaretoken', 'timeScale', 'typestr']
        print(dict(request.POST))
        # TODO 如果前端js取值为空，js是不会把这个值打包进参数传递给后台的
        # if 'steel_type' not in dict(request.POST):
        #     pop_no_op.pop('steel_type')
        steel_type = request.POST.get('steelType', '')
        time_scale = request.POST.get('timeScale', '')
        typestr = request.POST.get('typestr', '')
        if typestr != "":
            types = typestr.split(',')
            print(types)
        params, history_begin, history_end = dc.first_ele(dict(request.POST), pop_no_op=pop_no_op)
    print(params)
    sqlVO, rs = dc.format_data(params)

    dp = data_preparetion.Data_Preparetion()
    model_prepared = dp.intergrate_data_from_db(sqlVO=sqlVO)
    model_prepared['time'] = model_prepared['time'].map(lambda x: str(x))
    timeline = list(model_prepared['time'])
    true_value = model_prepared['steelprice'].map(lambda x: float(x)) # 表名标示数据
    contentVO['timeline'] = timeline
    if time_scale == "day":
        pass
    elif time_scale == "month":

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

        model_data, model_label = dp.create_data_label(model_prepared)
        models = map(init_models, types)
        models = list(models)
        # TODO 得到每个模型的预测结果就好了

        for index in range(len(models)):
            for method, model in models[index].items():
                if model is not None:
                    single_result = {}
                    special_model = model()
                    # 目前在数据量不大的情况下还是均作保留模型的实时训练
                    # data_train, data_test, label_train, label_test = special_model.standard_split_train_test(model_data, model_label)
                    # model().update_model(data_train, data_test, label_train, label_test)
                    result = special_model.predict(model_data)
                    if result is not None:
                        result = list(result)
                    single_result['predict_value'] = result
                    models_result[method] =single_result
        # logger.debug(models_result)
        print(models_result.keys())
        for method in models_result:
            models_result[method]['timeline'] = timeline
            models_result[method]['true_value'] = list(true_value)
        contentVO['state'] = const.OK.get('code', 0)

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
    return render(request, 'data_import/ironstoneprice.html', contentVO)

# TODO 根据yinsu_type选取相应描述
def stone_price_history(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        history_begin = request.POST.get('history_begin', '')
        history_end = request.POST.get('history_end', '')
        yinsu_type = request.POST.get('yinsu_type', '')
    path = data_root + '/tkszs_yinsu.csv'
    # path = data_root + 'tegang.csv'
    prices = get_stone_history_price(path, history_begin, history_end, yinsu_type)

    # prices['timeline'] = []
    # prices['price'] = []
    # print(type(prices.get('price',None)[0]))

    contentVO = {
        'title': '铁矿石历史价格',
        'state': 'success'
    }
    contentVO['state'] = const.OK.get('code', 0)  # 前端检测state状态，匹配message信息进行相应处理
    contentVO['ele_info'] = ELE_INFOS.get(yinsu_type, "数据来源不详")
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
    path_iron = data_root + '/tkszs_yinsu.csv'
    path_iron_yue = data_root + '/qdg_time.csv'
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
                models_result["elm"] = result
            if types[i] == "logistic_regression":
                result = predict_day(path_iron, types[i])
                models_result["logistic_regression"] = result
            if types[i] == "svm":
                result = predict_day(path_iron, types[i])
                models_result["svm"] = result
            if types[i] == "random_forest":
                result = predict_day(path_iron, types[i])
                models_result["random_forest"] = result
    if timeScale == "month":
        for i in range(len(types)):
            # print(types[i])
            if types[i] == "elm":
                print(types[i])
                result = predict_yue(path_iron_yue, types[i])
                models_result["elm"] = result
            if types[i] == "logistic_regression":
                result = predict_yue(path_iron_yue, types[i])
                models_result["logistic_regression"] = result
            if types[i] == "svm":
                result = predict_yue(path_iron_yue, types[i])
                models_result["svm"] = result
            if types[i] == "random_forest":
                result = predict_yue(path_iron_yue, types[i])
                models_result["random_forest"] = result
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