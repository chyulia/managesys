from pandas import DataFrame
import pandas as pd
import numpy as np
import math
from . import models
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
import os
import json
import datetime
import csv
from decimal import *
from scipy.stats import norm
from . import batchprocess


#总体波动率分析(fluctuation.html)将cost和produce合并
import time
def fluc_qualityfields(request):
	# print("enter fluc_cost!")
	# fieldname=request.POST.get("fieldname").upper();#字段名
	SPECIFICATION=request.POST.get("SPECIFICATION");#钢种
	OPERATESHIFT=request.POST.get("OPERATESHIFT");#班次
	OPERATECREW=request.POST.get("OPERATECREW");#班别
	station=request.POST.get("station");#工位
	time1=request.POST.get("time1");
	time2=request.POST.get("time2");
	history_time1=request.POST.get("history_time1");
	history_time2=request.POST.get("history_time2");

	if SPECIFICATION !='blank':
		sentence_SPECIFICATION= " and SPECIFICATION='"+SPECIFICATION+"'"
	else:
		sentence_SPECIFICATION=''
	if OPERATESHIFT !='blank':
		sentence_OPERATESHIFT=" and OPERATESHIFT='"+OPERATESHIFT+"'"
	else:
		sentence_OPERATESHIFT=''
	if OPERATECREW !='blank':
		sentence_OPERATECREW=" and OPERATECREW='"+OPERATECREW+"'"
	else:
		sentence_OPERATECREW=''
	if station !='blank':
		sentence_station=" and station='"+station+"'"
	else:
		sentence_station=''
	#计算波动率的时间范围
	if time1 != '' and time2!='':
		sentence_time="and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')>='"+time1+"'and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')<='"+time2+"'"
	else:
		sentence_time=''
	#对比历史波动率的时间范围
	if history_time1 != '' and history_time2!='':
		sentence_historytime="and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')>='"+history_time1+"'and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')<='"+history_time2+"'"
	else:
		sentence_historytime=''

	#筛选条件：钢种+班次+班别+工位
	filters=sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station

	times={
		'time1':time1,
		'time2':time2,
		'history_time1':history_time1,
		'history_time2':history_time2
	}


	thistime=time.localtime(time.time())
	#当前时间
	# time_now=time.strftime('%Y-%m-%d',thistime)
	time_now=months(thistime,-3)
	#一个月前
	time_lastone=months(thistime,-4)
	#两个月前
	time_lasttwo=months(thistime,-5)
	#三个月前
	time_lastthree=months(thistime,-6)
	#四个月前
	time_lastfour=months(thistime,-7)


	#判断是否执行缓存
	ifcache=( filters=='' and time1==time_lastone and time2==time_now and history_time2==time_lastone and ( history_time1==time_lasttwo or history_time1==time_lastthree or history_time1==time_lastfour))
	print('是否执行缓存',ifcache)

	#判断执行哪项缓存,若不执行缓存则为0
	if ifcache:
		if history_time1==time_lasttwo:
			whichcache=1
		elif history_time1==time_lastthree:
			whichcache=2
		else:
			whichcache=3
	else:
		whichcache=0


	contentVO={
		'title':'测试',
		'state':'success',
		'time':times,
	}
	sentence_select=sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_time
	sentence_selecthistory=sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_historytime
		

	xasis_fieldname_ch=['C含量','SI含量','MN含量','P含量','S含量','重量','温度']
	xasis_fieldname=['C','SI','MN','P','S','STEELWGT','FINAL_TEMP_VALUE']
	

	#判断是否走缓存路线，对默认条件下的本月-上月；本月-上两月；本月-上三月走数据库缓存，其他走正常程序。
	#符合执行缓存的筛选条件
	if ifcache:
		fluc_ratio=[]#存储各相关性字段的在当前的波动率
		fluc_ratio_history=[]#存储各相关性字段的在当前的波动率
		sqlVO={}
		sqlVO["db_name"]="l2own"

		if history_time1==time_lasttwo:#历史区间为上一月：即从两月前到上月，走缓存
			for i in range (len(xasis_fieldname)):
				sqlVO["sql"]="SELECT VOLATILITY_THISMONTH,VOLATILITY_LASTMONTH FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+xasis_fieldname[i]+"\'"
				scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				# print(scrapy_records)
				current_volatility= scrapy_records[0].get('VOLATILITY_THISMONTH',None)
				history_volatility=scrapy_records[0].get('VOLATILITY_LASTMONTH',None)
				if current_volatility  != None and current_volatility != 'null':
					current_volatility=float(current_volatility)
				else:
					current_volatility='wrong'
				if history_volatility  != None and history_volatility != 'null':
					history_volatility=float(history_volatility)
				else:
					history_volatility='wrong'
				fluc_ratio.append(current_volatility)
				fluc_ratio_history.append(history_volatility)

		elif history_time1==time_lastthree:#历史区间为上两月：即从三月前到上月，走缓存
			for i in range (len(xasis_fieldname)):
				sqlVO["sql"]="SELECT VOLATILITY_THISMONTH,VOLATILITY_LAST2MONTH FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+xasis_fieldname[i]+"\'"
				scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				# print(scrapy_records)
				current_volatility= scrapy_records[0].get('VOLATILITY_THISMONTH',None)
				history_volatility=scrapy_records[0].get('VOLATILITY_LAST2MONTH',None)
				if current_volatility  != None and current_volatility != 'null':
					current_volatility=float(current_volatility)
				else:
					current_volatility='wrong'
				if history_volatility  != None and history_volatility != 'null':
					history_volatility=float(history_volatility)
				else:
					history_volatility='wrong'
				fluc_ratio.append(current_volatility)
				fluc_ratio_history.append(history_volatility)

		# elif history_time1==time_lastfour:#历史区间为上三月：即从四月前到上月，走缓存
		else:#历史区间为上三月：即从四月前到上月，走缓存
			for i in range (len(xasis_fieldname)):
				sqlVO["sql"]="SELECT VOLATILITY_THISMONTH,VOLATILITY_LAST3MONTH FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+xasis_fieldname[i]+"\'"
				scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				# print(scrapy_records)
				current_volatility= scrapy_records[0].get('VOLATILITY_THISMONTH',None)
				history_volatility=scrapy_records[0].get('VOLATILITY_LAST3MONTH',None)
				if current_volatility  != None and current_volatility != 'null':
					current_volatility=float(current_volatility)
				else:
					current_volatility='wrong'
				if history_volatility  != None and history_volatility != 'null':
					history_volatility=float(history_volatility)
				else:
					history_volatility='wrong'
				fluc_ratio.append(current_volatility)
				fluc_ratio_history.append(history_volatility)

		print("缓存--------------------------fluc_ratio_history",fluc_ratio_history)
		print("缓存--------------------------fluc_ratio_history",fluc_ratio_history)


	#普通时间区间，走正常程序
	else:
		#对任意个数字段进行字符串拼接
		field_sql=''
		for i in range(len(xasis_fieldname)):
			field_sql=field_sql+',nvl('+xasis_fieldname[i]+',0) as '+xasis_fieldname[i]

		#计算波动率的时间范围的sql
		sentence="SELECT HEAT_NO "+field_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_select
		# sentence="SELECT HEAT_NO,nvl(MIRON_WGT,0) as MIRON_WGT,nvl(SUM_BO_CSM,0) as SUM_BO_CSM ,nvl(COLDPIGWGT,0) as COLDPIGWGT,nvl(SCRAPWGT_COUNT,0) as SCRAPWGT_COUNT FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_select
		

		#对比历史波动率的时间范围的sql
		sentence_history="SELECT HEAT_NO "+field_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_selecthistory
		# sentence_history="SELECT HEAT_NO,nvl(MIRON_WGT,0) as MIRON_WGT,nvl(SUM_BO_CSM,0) as SUM_BO_CSM ,nvl(COLDPIGWGT,0) as COLDPIGWGT,nvl(SCRAPWGT_COUNT,0) as SCRAPWGT_COUNT FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_selecthistory

		# length_result1=len(xasis_fieldname)
		#计算当前时间区间的字段波动率-------------------------------------------------------------------------------------------------
		sqlVO={}
		sqlVO["db_name"]="l2own"
		sqlVO["sql"]=sentence
		# print(sqlVO["sql"])
		scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
		# print('len(scrapy_records)',len(scrapy_records))


		ana_describe=calaulate_describe(scrapy_records,xasis_fieldname)
		# if ana_describe['sign']==1:
		if len(scrapy_records)==0:
			contentVO['state']='failure_current'
			return HttpResponse(json.dumps(contentVO),content_type='application/json')

		# print('-----------------------ana_describe',ana_describe)

		fluc_ratio=[]#存储各相关性字段的在当前的波动率
		for i in range(len(xasis_fieldname)):
			if ana_describe['state'][xasis_fieldname[i]]=='wrong':#如果当前追溯字段无值，则设置wrong并在后面筛选除去该字段
				fluc_ratio.append('wrong')
				continue
			describe=[ele for ele in ana_describe[xasis_fieldname[i]]]
			#value接受计算完成的字段波动率值
			value=describe[2]/describe[1]
			fluc_ratio.append(value)
		print("-------------------------fluc_ratio",fluc_ratio)


		#计算历史时间区间的字段波动率-------------------------------------------------------------------------------------------------
		sqlVO_history={}
		sqlVO_history["db_name"]="l2own"
		sqlVO_history["sql"]=sentence_history
		# print(sqlVO_history["sql"])
		scrapy_records_history=models.BaseManage().direct_select_query_sqlVO(sqlVO_history)

		ana_describe_history=calaulate_describe(scrapy_records_history,xasis_fieldname)
		# if ana_describe_history['sign']==1:
		if len(scrapy_records_history)==0:
			contentVO['state']='failure_history'
			return HttpResponse(json.dumps(contentVO),content_type='application/json')
		# print('----------------------------ana_describe_history',ana_describe_history)

		fluc_ratio_history=[]#存储各相关性字段的在当前的波动率
		for i in range(len(xasis_fieldname)):
			if ana_describe_history['state'][xasis_fieldname[i]]=='wrong':#如果当前追溯字段无值，则设置wrong并在后面筛选除去该字段
				fluc_ratio_history.append('wrong')
				continue
			describe=[ele for ele in ana_describe_history[xasis_fieldname[i]]]
			#value接收计算完成的字段波动率值：标准差/期望
			value=describe[2]/describe[1]
			fluc_ratio_history.append(value)
		print("--------------------------fluc_ratio_history",fluc_ratio_history)


	#计算偏离程度
	offset_result=[]
	for i in range(len(xasis_fieldname)):
		if fluc_ratio[i]=='wrong' or fluc_ratio_history[i]=='wrong':#即当前字段无值时，在进行分析时（不是追溯时）,将当前字段的参数设为特殊值
			offset_result.append('wrong')
			continue
		try:
			#当fluc_ratio_history[i]=0时，计算公式将会报错，此时表明历史数据是没有波动率的，因此偏离程度相当于无穷
			temp=(fluc_ratio[i]-fluc_ratio_history[i])/fluc_ratio_history[i]
		except:
			temp=99999999
		offset_result.append(temp)

	#----------------------------------------------
	#进行筛选，在整体有数据的情况下，将正常字段与异常字段(无法计算偏离程度的字段)进行分开存储
	#（1）存储筛选后的字段
	xasis_fieldname_result=[]#字段英文名字数组
	xasis_fieldname_ch_result=[]#字段中文名字数组
	fluc_ratio_result=[]
	fluc_ratio_history_result=[]
	offset_result_final=[]#偏离程度值

	#（2）存储无法计算偏离程度的字段，当前数据或历史数据中有任意一方无法计算波动率时，就不能计算偏离程度
	xasis_fieldname_wrongresult=[]#字段英文名字数组
	xasis_fieldname_ch_wrongresult=[]#字段中文名字数组
	fluc_ratio_wrongresult=[]
	fluc_ratio_history_wrongresult=[]
	# offset_wrongresult_final=[]#偏离程度值

	for i in range(len(xasis_fieldname)):
		if offset_result[i]==None  or offset_result[i]=='wrong':#无法计算偏离程度的异常字段
			xasis_fieldname_wrongresult.append(xasis_fieldname[i])
			xasis_fieldname_ch_wrongresult.append(xasis_fieldname_ch[i])
			fluc_ratio_wrongresult.append(fluc_ratio[i])
			fluc_ratio_history_wrongresult.append(fluc_ratio_history[i])
			# offset_wrongresult_final.append(offset_result[i])

		else:#正常字段
			xasis_fieldname_result.append(xasis_fieldname[i])
			xasis_fieldname_ch_result.append(xasis_fieldname_ch[i])
			fluc_ratio_result.append(fluc_ratio[i])
			fluc_ratio_history_result.append(fluc_ratio_history[i])
			offset_result_final.append(offset_result[i])

	#------------------------------------------------------------

	offset_resultlist=["%.2f%%"%(n*100) for n in list(offset_result_final)]
	qualitative_offset_result_final=qualitative_offset(offset_result_final)#对偏离程度进行定性判断
	fluc_ratiolist=["%.3f"%(n) for n in list(fluc_ratio_result)]
	fluc_ratio_historylist=["%.3f"%(n) for n in list(fluc_ratio_history_result)]

	ana_result={}
	ana_result['time']=times
	ana_result['ifcache']=ifcache
	ana_result['whichcache']=whichcache
	ana_result['sentence_select']=sentence_select
	ana_result['sentence_selecthistory']=sentence_selecthistory		

	#正常字段
	ana_result['fieldname_ch']=xasis_fieldname_ch_result#中文名
	ana_result['fieldname_en']=xasis_fieldname_result#英文名
	ana_result['fluc_ratio']=fluc_ratiolist#标准偏差，即波动率
	ana_result['fluc_ratio_history']=fluc_ratio_historylist#标准偏差，即波动率
	ana_result['qualitative_offset_result']=qualitative_offset_result_final#偏离程度的定性判断
	ana_result['offset_result']=offset_result_final#偏离程度（小数）
	ana_result['offset_result_cent']=offset_resultlist#偏离程度(百分数)
	#异常字段
	ana_result['fieldname_ch_wrong']=xasis_fieldname_wrongresult
	ana_result['fieldname_en_wrong']=xasis_fieldname_ch_wrongresult
	ana_result['fluc_ratio_wrong']=fluc_ratio_wrongresult
	ana_result['fluc_ratio_history_wrong']=fluc_ratio_history_wrongresult

	#如果有数据，但是清洗后所有字段都无有效数据，则直接返回相关信息
	if len(xasis_fieldname_result)==0:
		ana_result['condition']='NoData'
	else:
		ana_result['condition']='Normal'


	contentVO['result']=ana_result
	return HttpResponse(json.dumps(contentVO),content_type='application/json')


#对分析字段偏离程度进行定性判断：
def qualitative_offset(offset_result):
	#偏离程度定性标准，例如-10%~10%为正常，10%~30%为偏高，30%以上为数据异常/极端数据
	qualitative_standard=[0.05,0.1]
	qualitative_offset_result=[]
	for i in range(len(offset_result)):
		if float(offset_result[i])<=0:
			qualitative_offset_result.append('变平稳')
		elif float(offset_result[i])<=qualitative_standard[0]:
			qualitative_offset_result.append('正常范围')
		elif float(offset_result[i])<=qualitative_standard[1]:
			qualitative_offset_result.append('偏高')
		else:
			qualitative_offset_result.append('高')		
	return  qualitative_offset_result

#追溯时对影响字段的定性判断
def qualitative_offset1(offset_result):
	#偏离程度定性标准，例如-10%~10%为正常，10%~30%为偏高，30%以上为数据异常/极端数据
	qualitative_standard=[0.01,0.05,0.1]
	qualitative_offset_result=[]
	for i in range(len(offset_result)):
		if float(offset_result[i])<=0:
			qualitative_offset_result.append('变平稳')
		elif float(offset_result[i])<=qualitative_standard[0]:
			qualitative_offset_result.append('正常范围')
		elif float(offset_result[i])<=qualitative_standard[1]:
			qualitative_offset_result.append('波动率偏高')
		else:
			qualitative_offset_result.append('波动率高')		
	return  qualitative_offset_result

#进行五数分析法
def Wushu(x):
    L=np.percentile(x,25)-1.5*(np.percentile(x,75)-np.percentile(x,25))
    U=np.percentile(x,75)+1.5*(np.percentile(x,75)-np.percentile(x,25))
    result=x[(x<U)&(x>L)]
    wushu_clean={}
    wushu_clean["minbook"]=L
    wushu_clean["maxbook"]=U
    wushu_clean["result"]=result
    return wushu_clean


#判断有效小数位数
def ivalue_num(num):
    a=str(num)
    if(a.isdigit()):
        ivalue_valid=0
    else:
        # print("%s,%s"%(a.split('.'),len(a.split('.'))))
        #数据库中存在如448.000的字段，执行a.split('.')的结果只有整数部分，因此取a.split('.')[1]会出现超出索引的情况
        if len(a.split('.'))==1:
            ivalue_valid=0
        else:
            ivalue_valid=len(a.split('.')[1])
    return  ivalue_valid   

#取有效位数
def vaild(lis,ivalue_valid,data):
    for i in range(len(lis)):
        shu=lis[i]
        if ivalue_valid==0:
            shua=int(float(shu))
            data.append(shua)
        else:    
            shua=float(shu)
            shub=round(shua,ivalue_valid)
            data.append(shub)
    return data 



#波动率影响因素追溯
from . import zhuanlu
def quality_fluc_influence(request):
	print("Enter fluc_influence")
	singlefield_en=request.POST.get("field");#字段英文名
	singlefield_offset=request.POST.get("offset_value");#一定时间范围波动率的偏离程度，
	sentence_select=request.POST.get("sentence_select");
	sentence_selecthistory=request.POST.get("sentence_selecthistory");
	ifcache=request.POST.get("ifcache");#是否执行缓存
	whichcache=request.POST.get("whichcache");#判断执行哪一项缓存，0为不执行缓存

	#中文名、偏离程度定性描述、带百分号的偏离程度绝对值、回归系数
	En_to_Ch_result_score,offset_result_nature,offset_value_single_cof,regression_coefficient_result=analy_cof(ifcache,whichcache,singlefield_en,singlefield_offset,sentence_select,sentence_selecthistory)
	contentVO={
		'title':'测试',
		'state':'success',
	}	
	# contentVO['xasis_fieldname']=xasis_fieldname_result#回归系数因素英文字段名
	contentVO['regression_coefficient']=regression_coefficient_result#字段回归系数值
	contentVO['offset_result_nature']=offset_result_nature#偏离程度定性描述
	contentVO['offset_result_cent']=offset_value_single_cof#带百分号的偏离程度绝对值
	contentVO['En_to_Ch_result']=En_to_Ch_result_score#回归系数最大因素中文字段名字
		
	return HttpResponse(json.dumps(contentVO),content_type='application/json')	


#仅进行数据清洗，并计算describe参数（可以是任意个字段），不计算概率分布和正态分布
def calaulate_describe(scrapy_records,fieldname):
	# print(scrapy_records[1:5])
	ana_describe={}
	ana_describe['shuxing']=['count','mean','std','min','25%','50%','75%','max']
	parameters=['NUMERICAL_LOWER_BOUND','NUMERICAL_UPPER_BOUND','IF_FIVENUMBERSUMMARY']
	state={}#存储各个字段的状态
	# sign=0#标志位，表示是否出现无数据状态
	print('fieldname',fieldname)
	for bookno in fieldname:
		print('计算字段：',bookno)
		state[bookno]='normal'#初始为正常
		ivalue_i=[]
		# print('len(scrapy_records)',len(scrapy_records))
		for n in range(len(scrapy_records)):
			ivalue = scrapy_records[n].get(bookno,None)
			if ivalue !=None and ivalue !=0:
				 ivalue=ivalue
				 ivalue_b=str(ivalue)
				 ivalue_valid=ivalue_num(ivalue_b)#小数位数
				 ivalue_i.append(ivalue_valid)
				 ivalue_i.sort(reverse=True)
		if ivalue_i==[]:#若字段为空，表示该字段没有数据
			state[bookno]='wrong'#若出现问题，将状态改为wrong
			# sign=1
			continue
		ivalue_valid=ivalue_i[0]#取所有有效位数的最大个数
		# print(ivalue_valid)		
		#将所有数据转为float格式
		for i in range(len(scrapy_records)):
			value = scrapy_records[i].get(bookno,None)
			if value != None :
				scrapy_records[i][bookno] = float(value)			
		frame=DataFrame(scrapy_records)	
		df=frame[bookno]

		#查询字段上下限
		sqlVO={}
		sqlVO["db_name"]="l2own"
		sqlVO["sql"]="SELECT NUMERICAL_LOWER_BOUND,NUMERICAL_UPPER_BOUND,IF_FIVENUMBERSUMMARY FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+bookno+"\'"
		print(sqlVO["sql"])
		bookno_parameter=models.BaseManage().direct_select_query_sqlVO(sqlVO)

		for j in range (len(parameters)):
			value = bookno_parameter[0].get(parameters[j],None)
			if value != None and value != 'null':
				bookno_parameter[0][parameters[j]] = float(value)


		# print('df_single',df_single)
		# df=df_single.sort_values(by=bookno)
		# print(df)
		#切片，对字段数据进行上下限筛选
		dfr=df[df>=bookno_parameter[0]['NUMERICAL_LOWER_BOUND']]
		dfr=dfr[df<=bookno_parameter[0]['NUMERICAL_UPPER_BOUND']]
		if len(dfr)<50:#如果数据个数小于50，则跳过这个字段的计算
			state[bookno]='wrong'#若出现问题，将状态改为wrong
			# sign=1
			continue

		#进行五数清洗
		if bookno_parameter[0]['IF_FIVENUMBERSUMMARY']==1:
			clean=Wushu(dfr)['result']
		else:
			clean=dfr		

		if len(clean)<50:#如果数据个数小于50，则跳过这个字段的计算
			state[bookno]='wrong'#若出现问题，将状态改为wrong
			# sign=1
			continue


		describe=clean.describe()

		# print(describe)

		# desx=[ele for ele in describe.index]
		desy=[ele for ele in describe]

		d4_data=[]
		desy1=vaild(desy,ivalue_valid,d4_data)

		#desy1内容依次为count、mean、std、min、25%、50%、75%、max
		#计算波动率：标准差/期望

		# ana_describe['scopeb']=desx
		ana_describe[bookno]=desy1
	ana_describe['state']=state#用于详细表示各个字段的数据情况，筛选条件下的无数据表示为wrong，正常情况表示为normal
	# ana_describe['sign']=sign#用于表征是否出现了字段的无数据现象
	# print('state',state)
	return ana_describe



#计算时间的向前或向后数月的时间
def months(dt,months):#这里的months 参数传入的是正数表示往后 ，负数表示往前
    month = dt.tm_mon - 1 + months
    year = dt.tm_year + month // 12#python3特性：//表示整数除，/除法会自动转为浮点数
    month = month % 12 + 1
    day = dt.tm_mday#对于参数更新而言，出现20170230并不会产生影响
    pretime=str(year)+'-'+str(month)+'-'+str(day)#可能是2017-7-5格式
    #将2017-7-5格式转化为2017-07-05格式
    t = time.strptime(pretime, "%Y-%m-%d")
    resulttime=time.strftime('%Y-%m-%d',t)
    return resulttime



#波动率影响因素追溯
from . import zhuanlu
def quality_multifurnace_regression_analyse(request):
	print("Enter multifurnace_regression_analyse")
	result = json.loads(request.POST.get("result"));
	str_cause=multifurnace_regression_analyse_to(result)

	contentVO={
		'title':'测试',
		'state':'success',
		'str_cause':str_cause
	}				
	return HttpResponse(json.dumps(contentVO),content_type='application/json')	


def multifurnace_regression_analyse_to(result):
	ifcache=result['ifcache']
	whichcache=result['whichcache']#判断执行哪一项缓存，0为不执行缓存
	sentence_select=result['sentence_select']#当前筛选条件
	sentence_selecthistory=result['sentence_selecthistory']#历史筛选条件

	str_cause=''#存放追溯结果
	n=0#n用来指示当前问题字段的个数
	print(ifcache)
	print(whichcache)

	#(1)对异常数据进行描述
	fieldname_en_wrong=result['fieldname_en_wrong']#读取各类中的字段
	for i in range(len(fieldname_en_wrong)):#对类中的每个字段进行处理
		#当前波动率
		corrent_wrong_fluc_ratio=result['fluc_ratio_wrong'][i]
		#历史波动率
		history_wrong_fluc_ratio=result['fluc_ratio_history_wrong'][i]
		#反馈信息
		str_cause=str_cause+'【'+str(n+1)+'】'+str(fieldname_en_wrong[i])+'当前波动率为'+str(corrent_wrong_fluc_ratio)[:5]+',历史波动率为'+str(history_wrong_fluc_ratio)[:5]+',无法计算偏离程度！\n' 
		n=n+1

	#(2)对正常字段进行分析或追溯
	fieldname_en=result['fieldname_en']#读取各类中的字段

	for i in range(len(fieldname_en)):#对类中的每个字段进行处理
		singlefield_en=fieldname_en[i]#单字段英文名
		singlefield_ch=result['fieldname_ch'][i]#单字段中文名
		singlefield_current_fluc_ratio=result['fluc_ratio'][i]#当前波动率
		singlefield_history_fluc_ratio=result['fluc_ratio_history'][i]#历史波动率
		singlefield_offset=result['offset_result'][i]#偏离程度
		offset_value_abs="%.2f%%"%(abs(float(singlefield_offset))*100)
		qualitative_offset_result_single=result['qualitative_offset_result'][i]#偏离程度

		if singlefield_offset <0:#当前字段波动率偏小，不需要进行追溯
			# str_cause=str_cause+'【'+str(n+1)+'】'+singlefield_ch+'波动率降低，数值趋于稳定。\n'
			# n=n+1
			continue
		elif singlefield_offset <=0.05:#偏离程度小于0.05，属于正常状态
			# str_cause=str_cause+'【'+str(n+1)+'】'+singlefield_ch+'波动率正常。\n'
			# n=n+1
			continue
		else:#正常追溯
			#中文名、偏离程度定性描述、带百分号的偏离程度绝对值、回归系数
			En_to_Ch_result_score,offset_result_nature,offset_value_single_cof,regression_coefficient_result = analy_cof(ifcache,whichcache,singlefield_en,singlefield_offset,sentence_select,sentence_selecthistory)
			if 	En_to_Ch_result_score==None:
				# str_des='本炉次'+prime_cost+'的'+singlefield_ch+qualitative_offset_result_single+',实际值为'+str(single_value)+danwei[i]+'，但进行回归分析时相关字段无数据！'

				continue
			else:
				# str_des='本炉次'+prime_cost+'的'+singlefield_ch+qualitative_offset_result_single+',实际值为'+str(single_value)+danwei[i]+',偏离度为'+offset_value+'。通过数据相关性分析发现，导致该问题的原因是:\n'      
				str_cause= str_cause+'【'+str(n+1)+'】'+singlefield_ch+qualitative_offset_result_single+offset_value_abs+'：'      
				n=n+1
				for i in range(len(En_to_Ch_result_score)):
					str_cause=str_cause+'[原因'+str(i+1)+']'+En_to_Ch_result_score[i]+offset_result_nature[i]+offset_value_single_cof[i]+'；'
				str_cause=str_cause+'\n'

	if n==0:
		str_cause='当前数据条件均符合要求，无需追溯。\n'

	return str_cause	


def analy_cof(ifcache,whichcache,singlefield_en,singlefield_offset,sentence_select,sentence_selecthistory):
	
	#从数据库读取相关性系数文件
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT * FROM PRO_BOF_HIS_RELATION_COF where OUTPUTFIELD='"+singlefield_en +"'  order by abs(COF) desc"
	print(sqlVO["sql"])
	scrapy_records_relation=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	#print(scrapy_records)
	length_result1=len(scrapy_records_relation)
	if length_result1==0:#即无相关性字段
		return None,None,None,None

	xasis_fieldname=[]#字段英文名字数组
	correlation_coefficient=[]#字段相关系数值数组
	str_sql=''
	for i in range(length_result1):
		xasis_fieldname.append(scrapy_records_relation[i].get('MIDDLEFIELD', None))
		correlation_coefficient.append(scrapy_records_relation[i].get('COF', None))
		str_sql=str_sql+','+scrapy_records_relation[i].get('MIDDLEFIELD', None)

	#判断是否走缓存路线，对默认条件下的本月-上月；本月-上两月；本月-上三月走数据库缓存，其他走正常程序。
	#执行缓存
	if bool(ifcache):
		fluc_ratio=[]#存储各相关性字段的在当前的波动率
		fluc_ratio_history=[]#存储各相关性字段的在当前的波动率
		sqlVO={}
		sqlVO["db_name"]="l2own"

		if whichcache=='1':#历史区间为上一月：即从两月前到上月，走缓存
			for i in range (len(xasis_fieldname)):
				sqlVO["sql"]="SELECT VOLATILITY_THISMONTH,VOLATILITY_LASTMONTH FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+xasis_fieldname[i]+"\'"
				scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				# print(scrapy_records)
				current_volatility= scrapy_records[0].get('VOLATILITY_THISMONTH',None)
				history_volatility=scrapy_records[0].get('VOLATILITY_LASTMONTH',None)
				if current_volatility  != None and current_volatility != 'null':
					current_volatility=float(current_volatility)
				else:
					current_volatility='wrong'
				if history_volatility  != None and history_volatility != 'null':
					history_volatility=float(history_volatility)
				else:
					history_volatility='wrong'
				fluc_ratio.append(current_volatility)
				fluc_ratio_history.append(history_volatility)

		elif whichcache=='2':#历史区间为上两月：即从三月前到上月，走缓存
			for i in range (len(xasis_fieldname)):
				sqlVO["sql"]="SELECT VOLATILITY_THISMONTH,VOLATILITY_LAST2MONTH FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+xasis_fieldname[i]+"\'"
				scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				# print(scrapy_records)
				current_volatility= scrapy_records[0].get('VOLATILITY_THISMONTH',None)
				history_volatility=scrapy_records[0].get('VOLATILITY_LAST2MONTH',None)
				if current_volatility  != None and current_volatility != 'null':
					current_volatility=float(current_volatility)
				else:
					current_volatility='wrong'
				if history_volatility  != None and history_volatility != 'null':
					history_volatility=float(history_volatility)
				else:
					history_volatility='wrong'
				fluc_ratio.append(current_volatility)
				fluc_ratio_history.append(history_volatility)

		# elif whichcache==3:#历史区间为上三月：即从四月前到上月，走缓存
		else:#历史区间为上三月：即从四月前到上月，走缓存
			for i in range (len(xasis_fieldname)):
				sqlVO["sql"]="SELECT VOLATILITY_THISMONTH,VOLATILITY_LAST3MONTH FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+xasis_fieldname[i]+"\'"
				scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				# print(scrapy_records)
				current_volatility= scrapy_records[0].get('VOLATILITY_THISMONTH',None)
				history_volatility=scrapy_records[0].get('VOLATILITY_LAST3MONTH',None)
				if current_volatility  != None and current_volatility != 'null':
					current_volatility=float(current_volatility)
				else:
					current_volatility='wrong'
				if history_volatility  != None and history_volatility != 'null':
					history_volatility=float(history_volatility)
				else:
					history_volatility='wrong'
				fluc_ratio.append(current_volatility)
				fluc_ratio_history.append(history_volatility)

		print("缓存--------------------------fluc_ratio_history",fluc_ratio_history)
		print("缓存--------------------------fluc_ratio_history",fluc_ratio_history)


	#普通筛选条件，走正常程序
	else:

		#计算当前时间区间的字段波动率-------------------------------------------------------------------------------------------------
		sqlVO={}
		sqlVO["db_name"]="l2own"
		sqlVO["sql"]="SELECT HEAT_NO" +str_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no>'150000'"+sentence_select
		print(sqlVO["sql"])
		scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
		print('len(scrapy_records)',len(scrapy_records))

		# try:#对于查询结果无数据的情况
		ana_describe=calaulate_describe(scrapy_records,xasis_fieldname)
		# except:
		# 	contentVO['state']='failure_current'
			# return HttpResponse(json.dumps(contentVO),content_type='application/json')

		# print('-----------------------ana_describe',ana_describe)

		fluc_ratio=[]#存储各相关性字段的在当前的波动率
		for i in range(length_result1):
			if ana_describe['state'][xasis_fieldname[i]]=='wrong':#如果当前追溯字段无值，则设置wrong并在后面筛选除去该字段
				fluc_ratio.append('wrong')
				continue
			describe=[ele for ele in ana_describe[xasis_fieldname[i]]]
			#value接受计算完成的字段波动率值
			value=describe[2]/describe[1]
			fluc_ratio.append(value)
		print("-------------------------fluc_ratio",fluc_ratio)


		#计算历史时间区间的字段波动率-------------------------------------------------------------------------------------------------
		sqlVO_history={}
		sqlVO_history["db_name"]="l2own"
		sqlVO_history["sql"]="SELECT HEAT_NO" +str_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no>'150000' "+sentence_selecthistory
		print(sqlVO_history["sql"])
		scrapy_records_history=models.BaseManage().direct_select_query_sqlVO(sqlVO_history)

		# try:
		ana_describe_history=calaulate_describe(scrapy_records_history,xasis_fieldname)
		# except:
		# 	contentVO['state']='failure_history'
			# return HttpResponse(json.dumps(contentVO),content_type='application/json')

		# print('----------------------------ana_describe_history',ana_describe_history)

		fluc_ratio_history=[]#存储各相关性字段的在当前的波动率
		for i in range(length_result1):
			if ana_describe_history['state'][xasis_fieldname[i]]=='wrong':
				fluc_ratio_history.append('wrong')
				continue
			describe=[ele for ele in ana_describe_history[xasis_fieldname[i]]]
			#value接收计算完成的字段波动率值：标准差/期望
			value=describe[2]/describe[1]
			fluc_ratio_history.append(value)
		print("--------------------------fluc_ratio_history",fluc_ratio_history)


	#计算偏离程度
	offset_degree=[]
	for i in range(length_result1):
		if fluc_ratio[i]=='wrong' or fluc_ratio_history[i]=='wrong':
			offset_degree.append('wrong')
			continue
		try:
			#当历史波动率fluc_ratio_history[i]=0时，计算公式将会报错，此时表明历史数据是没有波动率的，因此偏离程度相当于无穷
			temp=(fluc_ratio[i]-fluc_ratio_history[i])/fluc_ratio_history[i]
		except:
			temp=99999999
		offset_degree.append(temp)

	print(xasis_fieldname)
	print("偏离程度")
	print(offset_degree)

	xasis_fieldname_result=[]#字段英文名字数组
	correlation_coefficient_result=[]#字段回归系数值数组
	offset_degree_result=[]#偏离程度值

	#字段筛选，波动率只与字段的相关性的绝对值大小相关，与正负性无关。
	#只对波动率变大的字段进行追溯，追溯到的也应该是波动率变大（即不稳定）的字段
	j=0#标志位，表示当前筛选后的有效字段个数
	for i in range(length_result1):
		if j>=8:#取筛选后相关性最大的八个因素字段
			break
		if offset_degree[i]==None  or offset_degree[i]=='wrong' or offset_degree[i]<=0.01:#由于数据清洗的问题，暂且将NB字段如此处理，因为NB字段的所有数据均相同，导致数据清洗时将所有数据都清除了
			continue
		else:#offset_degree[i]>0.05
			j+=1
			xasis_fieldname_result.append(xasis_fieldname[i])
			correlation_coefficient_result.append(correlation_coefficient[i])
			offset_degree_result.append(offset_degree[i])


	if len(xasis_fieldname_result) == 0:
		return None,None,None,None

	#计算回归系数:regression_coefficient[0]表示各回归值，regression_coefficient[1]表示截距;1表示在regression中进行标准化，0表示不进行标准化
	regression_coefficient=batchprocess.regression(singlefield_en,xasis_fieldname_result,1)
	if regression_coefficient== False:
		return None,None,None,None

	#查询转炉工序字段名中英文对照
	ana_result={}
	ana_result=zhuanlu.PRO_BOF_HIS_ALLFIELDS
	En_to_Ch_result=[]
	for i in range(len(xasis_fieldname_result)):
		En_to_Ch_result.append(ana_result[xasis_fieldname_result[i]])



	#zip压缩:中文名、英文名、偏离程度、回归系数;注：python3之后zip函数返回的是迭代值，需要list强转
	L_zip=list(zip(En_to_Ch_result,xasis_fieldname_result,offset_degree_result,regression_coefficient[0],correlation_coefficient_result))
	print('L_zip:',list(L_zip))
	#按照回归系数进行排序(从大到小)
	L_zip.sort(key=lambda x:x[3],reverse=True)
	print('按照回归系数排序后的字段：',L_zip)
	#取回归系数前二的字段
	L_zip=L_zip[0:2]#表示取0和1
	print('取前二个字段时的实际字段个数：',len(L_zip))
	#解压缩
	L_unzip=list(zip(*L_zip))
	En_to_Ch_result_max=L_unzip[0]#中文名
	xasis_fieldname_result_max=L_unzip[1]#英文名
	offset_degree_result_max=L_unzip[2]#偏离程度
	regression_coefficient_max=L_unzip[3]#回归系数（权重）

	# '''
	#判断字段的顺序（对筛选后的三个字段再根据字段再表结构中的顺序进行排序）
	ana_result_score={}
	ana_result_score=zhuanlu.PRO_BOF_HIS_ALLFIELDS_SCORE
	En_to_Ch_result_score=[]
	for i in range(len(xasis_fieldname_result_max)):
		En_to_Ch_result_score.append(ana_result_score[xasis_fieldname_result_max[i]][1])
	# print('表结构中字段的顺序',En_to_Ch_result_score)

	#zip压缩：中文名、英文名、偏离程度、字段顺序编号
	L_zip = list(zip(En_to_Ch_result_max,xasis_fieldname_result_max,offset_degree_result_max,En_to_Ch_result_score,regression_coefficient_max))
	#按照字段顺序进行排序（从小到大）
	L_zip.sort(key=lambda x:x[3])
	print('追溯结果的三个字段',L_zip)
	#解压缩
	L_unzip=list(zip(*L_zip))

	En_to_Ch_result_max=L_unzip[0]#中文名
	xasis_fieldname_result_max=L_unzip[1]#英文名
	offset_degree_result_max=L_unzip[2]#偏离程度
	En_to_Ch_result_score_max=L_unzip[3]#字段序号
	regression_coefficient_max=L_unzip[4]#回归系数（权重）
	# '''

	offset_degree_result_max_final=["%.2f%%"%(abs(float(n))*100) for n in list(offset_degree_result_max)]#将偏离程度值转化为保留两位小数的百分数
	#定性判断偏离程度（偏高、偏低）
	pos_float=[ float(n) for n in list(offset_degree_result_max)]
	offset_result_nature=qualitative_offset1(pos_float)


	return En_to_Ch_result_max,offset_result_nature,offset_degree_result_max_final,regression_coefficient_max

