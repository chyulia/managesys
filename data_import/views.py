# -*- coding: utf-8 -*-
import os
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import F

from . import models
from data_import.forms import UploadFileForm
from . import util
from . import const
from pandas import DataFrame
import pandas as pd
import numpy as np
import math

from collections import defaultdict
from math import ceil
from os.path import join

from QinggangManageSys.settings import MAIN_OUTFIT_BASE
from .models import ContentPost

import logging
import logging.config
from data_import.structure import int_information

from .models import ContentPost

# logging.config.dictConfig(LOGGING)
logger = logging.getLogger('django')


exclude_posts = ("shares","abstract")

def home(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	contentVO={
	'title':'主页',
	'state':None
	}
	infost = int_information()
	print(len(infost))

	contentVO['infost'] = infost

	# the_abstract = get_object_or_404(ContentPost, title="abstract")
	# contentVO["abstract"] = the_abstract
	# contentVO["state"] = "success"
	print(contentVO)
	logger.debug(MAIN_OUTFIT_BASE)
	return render(request, MAIN_OUTFIT_BASE + 'index.html',contentVO)


#用户登录
def user_login(request):
	print('用户登录')
	contentVO={
		'title':'用户登录',
		'state':None
	}
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	print("username:{0},password:{1}".format(username,password))
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		print(user.__dict__)
		print(user.is_active)
		# Correct password, and the user is marked "active"
		auth.login(request, user)
		# Redirect to a success page.
		contentVO['state']='success'
		return HttpResponseRedirect("/index")
	print(contentVO['state'])
	return render(request, MAIN_OUTFIT_BASE + 'login.html',contentVO)
def module_nav(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	contentVO={
	'title':'模块导航',
	'state':None
	}
	infost = int_information()
	contentVO['infost'] = infost
	module_type = request.GET.get('module_type', '')
	if module_type =='':
		return render(request, MAIN_OUTFIT_BASE + 'index.html',contentVO)
	elif module_type=='1':
		return render(request, MAIN_OUTFIT_BASE + 'nav1.html',contentVO)
	else:
		return render(request, MAIN_OUTFIT_BASE + 'nav2.html',contentVO)
#用户注册
def user_register(request):
	print("进行注册处理")
	contentVO={
		'title':'用户注册',
		'state':None
	}
	if request.method == 'POST':
		password = request.POST.get('password', '')
		repeat_password = request.POST.get('repeat_password', '')
		if password == '' or repeat_password == '':
			contentVO['state'] = 'empty'
		elif password != repeat_password:
			contentVO['state'] = 'repeat_error'
		else:
			username = request.POST.get('username', '')
			if User.objects.filter(username=username):
				contentVO['state'] = 'user_exist'
			else:
				new_user = User.objects.create_user(username=username, password=password,email=request.POST.get('email', ''))
				new_user.save()
				contentVO['state'] = 'success'
				return HttpResponseRedirect('/login')
	print(contentVO['state'])
	return render(request, MAIN_OUTFIT_BASE + 'register.html',contentVO)

#用户登出
def user_logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login')

#修改密码
@login_required()
def modify_password(request):
	print("修改密码")
	contentVO={
		'title':'修改密码',
		'state':None
	}
	user=request.user
	print('用户名：{0}'.format(user.username))
	oldpassword = request.POST.get('oldpassword','')
	if user.check_password(oldpassword):
		newpassword = request.POST.get('newpassword', '')
		repeat_newpassword = request.POST.get('repeat_newpassword', '')
		if newpassword == '' or repeat_newpassword == '':
			contentVO['state']='empty'
		elif newpassword != repeat_newpassword:
			contentVO['state'] = 'repeat_error'
		else:
			user.set_password(newpassword)
			user.save()
			contentVO['state'] = 'success'
	print(contentVO['state'])
	return render(request, MAIN_OUTFIT_BASE + 'modify_password.html',contentVO)


#重置密码
def reset_password(request):
	return HttpResponseRedirect("/index")

'''
项目进度控制，包括3个部分
总结
任务
建议
CATEGORY_CHOICES = (
        ('c', 'Common'),
        ('s', 'summary'),
        ('t', 'task'),
        ('a', 'advice'),
        ('nc', 'No Category'),
    )
'''
def contentpost(request,slug, post_id):
	args = {'contentpost': get_object_or_404(ContentPost, pk=post_id)}
	return render(request, 'data_import/control/content.html', args)


def summary(request):
	args = dict()
	contentposts = ContentPost.objects.exclude(title__in=exclude_posts)

	def get_sorted_posts(category):
	    posts_by_year = defaultdict(list)
	    posts_of_a_category = contentposts.filter(category=category)  # already sorted by pub_date
	    for post in posts_of_a_category:
	        year = post.pub_date.year
	        posts_by_year[year].append(post)  # {'2013':post_list, '2014':post_list}
	    posts_by_year = sorted(posts_by_year.items(), reverse=True)  # [('2014',post_list), ('2013',post_list)]
	    return posts_by_year

	args['data'] = [
	    ('s', get_sorted_posts(category="s")),
	]
	return render(request, 'data_import/control/summary-tasks-advices.html', args)

def tasks(request):
	args = dict()
	contentposts = ContentPost.objects.exclude(title__in=exclude_posts)

	def get_sorted_posts(category):
	    posts_by_year = defaultdict(list)
	    posts_of_a_category = contentposts.filter(category=category)  # already sorted by pub_date
	    for post in posts_of_a_category:
	        year = post.pub_date.year
	        posts_by_year[year].append(post)  # {'2013':post_list, '2014':post_list}
	    posts_by_year = sorted(posts_by_year.items(), reverse=True)  # [('2014',post_list), ('2013',post_list)]
	    return posts_by_year

	args['data'] = [
	    ('t', get_sorted_posts(category="t")),
	]
	return render(request, 'data_import/control/summary-tasks-advices.html', args)

def advices(request):
	args = dict()
	contentposts = ContentPost.objects.exclude(title__in=exclude_posts)

	def get_sorted_posts(category):
	    posts_by_year = defaultdict(list)
	    posts_of_a_category = contentposts.filter(category=category)  # already sorted by pub_date
	    for post in posts_of_a_category:
	        year = post.pub_date.year
	        posts_by_year[year].append(post)  # {'2013':post_list, '2014':post_list}
	    posts_by_year = sorted(posts_by_year.items(), reverse=True)  # [('2014',post_list), ('2013',post_list)]
	    return posts_by_year

	args['data'] = [
	    ('a', get_sorted_posts(category="a")),
	]
	return render(request, 'data_import/control/summary-tasks-advices.html', args)

def shares(request):
	args = {'shares': get_object_or_404(ContentPost, title="shares")}
	return render(request, 'data_import/control/shares.html', args)

'''
数据迁移
'''
def transfer():
	tr = models.TransRelation.objects.all()
	for each  in tr:
		db_name = each.from_system
		sql_select= 'SELECT {0} FROM TABLE {1} WHERE uid={2}'.format(each.from_col,each.from_table,each.uid)
		util.BaseManage.generic_query(sql_select)
		#先通过uid获取元素
		sql_insert= 'INSERT INTO {0} (own_col) values({1})'.format(each.own_table,each.own_col)


from QinggangManageSys.settings import BASE_DIR


def load_procedure_name(request):
	sqlVO={}
	sqlVO["sql"]="SELECT * FROM `procedure`"
	# sqlVO["vars"]=["procedure"]
	option_value={}
	procedure_names=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	#print(procedure_names)
	for name in procedure_names:
		option_value[name["procedurename"]]=name["remark"]
	contentVO={
		'title':'ajaxtest请求结果',
		'state':'success',
		'procedure_names':option_value,
		'filepath':"\\QinggangManageSys\\data_import\\media\\upload\\空间分布7-21.xlsx"
	}
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

def upload_file(request):
	filepath=None
	if request.method == 'POST':
		print(request.POST)
		procedurename=request.POST['procedure']
		if request.FILES['file']!=None:
			filepath=handle_uploaded_file(request.FILES['file'])
	if filepath!=None:
		print(filepath)
		if 	procedurename.startswith("SALES2"):
			util.import_multikey_file(filepath,models.TransRelationMultikey,procedurename)
		else:
			util.batch_import_data(filepath,models.TransRelation,procedurename)
	return render(request, MAIN_OUTFIT_BASE + 'form.html')

def handle_uploaded_file(f):
	filename=f._name
	filetype=filename.split('.')[-1]
	print(filetype)
	filepath=BASE_DIR +"\\data_import\\media\\upload\\"+filename
	with open(filepath, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return filepath


def delete_records(request):
	if request.method == 'POST':
		procedurename=request.POST['procedure']
	if 	procedurename.startswith("SALES2"):
		records_sqlVO=util.create_delete_records_sqlVO(procedurename,models.TransRelationMultikey._meta.db_table)
	else:
		records_sqlVO=util.create_delete_records_sqlVO(procedurename,models.TransRelation._meta.db_table)
	result=models.BaseManage().direct_execute_query_sqlVO(records_sqlVO)
	return render(request, MAIN_OUTFIT_BASE + 'form.html')

def ana_data_lack(request):
	if request.method == 'POST':
		procedurename=request.POST['procedure']
	records_sqlVO=util.create_get_records_sqlVO(procedurename,models.TransRelation._meta.db_table)
	records=models.BaseManage().direct_select_query_sqlVO(records_sqlVO)
	table_model_name=class_name = records[0]['own_table']
	model = getattr(models,class_name)
	table_name=model._meta.db_table
	sum_sqlVO=util.create_sum_sqlVO(table_name)
	rs=models.BaseManage().direct_select_query_sqlVO(sum_sqlVO)
	for key in rs[0]:
		total_num=rs[0][key]
	print(total_num)
	ana_list=[]
	col_ele={}
	for record in records:
		print("************************{0}".format(record['own_col']))
		sql='SELECT %s FROM '+table_name+' WHERE '+record['own_col']+' IS NULL'
		varlist=[record['own_col']]
		sqlVO=util.create_sqlVO(sql,varlist)

		data=models.BaseManage().direct_select_query_sqlVO(sqlVO)
		lack_num=len(data)
		lack_rate=lack_num/int(total_num)
		col_ele['real_meaning']=record['real_meaning']
		col_ele['col_name']=record['own_col']
		col_ele['lack_num']=lack_num
		col_ele['lack_rate']=lack_rate
		ana_list.append(col_ele)
		col_ele={}

	filepath=util.write_2_excel(ana_list,procedurename)

	contentVO={
		'title':'数据缺失度分析结果',
		'state':'success',
		'filepath':filepath
	}
	return HttpResponse(json.dumps(contentVO), content_type='application/json')
	# return render(request,'data_import/index.html',contentVO)



def success(request):
	return render(request, MAIN_OUTFIT_BASE + 'success.html')

def ajaxtest(request):
	filepath=BASE_DIR +"\\data_import\\static\\libs\\echarts\\map\\"
	print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	contentVO={
		'title':'ajaxtest请求结果',
		'state':'success'
	}
	with open(filepath+'world.json','r')as f:
		chinaJson=json.load(f)
	contentVO['greet']=[55, 20, 76, 10, 10, 20]
	contentVO['china']=chinaJson
	print(type(chinaJson.get("features")))
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

def get_all_unique_table_records(records):
	unique_table_records=[]
	for record in records:
		tag=True
		for utr in unique_table_records:
			if utr['from_table']==record['from_table']:
				tag=False
				break;
		if tag:
			unique_table_records.append(record)
	return unique_table_records

def get_all_multikey_uid_data(records):
	unique_table_records=get_all_unique_table_records(records)
	print(unique_table_records)
	for record in unique_table_records:
		sqlVO=util.get_multikey_2uid_data(record)
		uids_single_record=models.BaseManage().direct_select_query_sqlVO(sqlVO)
		for uid in uids_single_record:
			insert_sqlVO=util.insert_2uid_sqlVO(uid,record)
			models.BaseManage().direct_execute_query_sqlVO(insert_sqlVO)
	all_uid_sqlVO=util.unique_uids_sqlVO()
	all_unique_uids=models.BaseManage().direct_select_query_sqlVO(all_uid_sqlVO)
	delete_sqlVO=util.delete_table('unique_col')
	models.BaseManage().direct_execute_query_sqlVO(delete_sqlVO)
	return all_unique_uids

def get_all_single_uid_data(records):
	unique_table_records=get_all_unique_table_records(records)
	print(unique_table_records)
	for record in unique_table_records:
		sqlVO=util.get_single_uid_data(record)
		uid_single_record=models.BaseManage().direct_select_query_sqlVO(sqlVO)
		for uid in uid_single_record:
			insert_sqlVO=util.insert_uid_sqlVO(uid,record)
			models.BaseManage().direct_execute_query_sqlVO(insert_sqlVO)
	all_uid_sqlVO=util.unique_single_uids_sqlVO()
	all_unique_uids=models.BaseManage().direct_select_query_sqlVO(all_uid_sqlVO)
	delete_sqlVO=util.delete_table('unique_col')
	models.BaseManage().direct_execute_query_sqlVO(delete_sqlVO)
	return all_unique_uids


def import_by_single(procedure):
	filepath = 'E:\\qinggang\\reference\\7-21\\需要迁移数据各工序模板\\转炉\\转炉迁移表1(1).xlsx'
	#util.batch_import_data(filepath,models.TransRelation)
	records_sqlVO=util.create_get_records_sqlVO(procedure,models.TransRelation._meta.db_table)
	records=models.BaseManage().direct_select_query_sqlVO(records_sqlVO)
	print("records:{records}".format(records=records))
	#records=None
	model=None
	#通过表名反射相应的对象
	class_name = records[0]['own_table']
	#print(class_name)
	model = getattr(models,class_name)
	table_name=model._meta.db_table
	if records !=None:
		uids_unique=get_all_single_uid_data(records)
		#将关联字段数据存入自己的表中
		print(uids_unique)
		for uid in uids_unique:
			attrdict={}
			if len(uid['relation_col1'])==0:
				continue
			attrdict[records[0]['own_uid']]=uid['relation_col1'].strip()
			real_model=model()
			real_model.set_attr(attrdict=attrdict)
			real_model.save()
		for record in records:
			print('start################################################{0}'.format(record))
			#取出所有的关联字段
			select_uid_sql = 'SELECT ' +record['own_uid'] +' FROM ' +table_name
			sqlVO={'sql':select_uid_sql}
			#print(sqlVO)
			own_uids=models.BaseManage().direct_select_query_sqlVO(sqlVO)
			#根据关联字段的值逐行匹配数据
			for uid in own_uids:
				own_uid_col=record['own_uid']
				own_id=uid[own_uid_col]
				sqlVO=util.get_value_by_uid_sqlVO(record,own_id)
				value=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				if(len(value)>0):
					insert_value=util.change_value_2_insert(value)
					dictVO={'record':record,'value':insert_value,'table_name':table_name,'own_id':own_id}
					sqlVO=util.create_update_by_uid_sqlVO(dictVO)

					models.BaseManage().direct_execute_query_sqlVO(sqlVO)
				#model.objects.filter(F(own_uid_col)=own_id).update(F(own_col)=insert_value)
			print('end################################################{0}'.format(record))


def import_by_multikey(procedure):
	print('迁移复合关联字段表数据')
	#filepath = 'E:\\qinggang\\reference\\7-21\\需要迁移数据各工序模板\\销售\\空间分布7-21.xlsx'
	#util.import_multikey_file(filepath,models.TransRelationMultikey)
	records_sqlVO=util.create_get_records_sqlVO(procedure,models.TransRelationMultikey._meta.db_table)
	records=models.BaseManage().direct_select_query_sqlVO(records_sqlVO)
	print("records:{records}".format(records=records))
	#records=None
	model=None
	#通过表名反射相应的对象，获取表名
	class_name = records[0]['own_table']
	#print(class_name)
	model = getattr(models,class_name)
	#print(model)
	table_name=model._meta.db_table
	#print(table_name)
	if records !=None:
		uids_unique=get_all_multikey_uid_data(records)
		print(uids_unique)
		for uid in uids_unique:
			attrdict={}
			if len(uid['relation_col1'])==0 or len(uid['relation_col2'])==0:
				continue
			attrdict[records[0]['own_uid1']]=uid['relation_col1'].strip()
			attrdict[records[0]['own_uid2']]=uid['relation_col2'].strip()
			real_model=model()
			real_model.set_attr(attrdict=attrdict)
			real_model.save()
		select_uid_sql = 'SELECT ' +records[0]['own_uid1'] +','+ records[0]['own_uid2'] +' FROM ' +table_name
		sqlVO={'sql':select_uid_sql}
		#print(sqlVO)
		own_uids=models.BaseManage().direct_select_query_sqlVO(sqlVO)
		for record in records:
			print('start################################################{0}'.format(record))
			#sql = 'SELECT '+record['FROM_COL']+' FROM '+record['FROM_TABLE']+' WHERE '+record['FROM_UID']
			#取出所有的关联字段
			for uid in own_uids:
				own_uid_col1=record['own_uid1']
				own_uid_col2=record['own_uid2']
				own_uid1=uid[own_uid_col1]
				own_uid2=uid[own_uid_col2]
				sqlVO=util.get_value_by_2uid_sqlVO(record,own_uid1,own_uid2)
				print(sqlVO)
				value=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				print('***************************{0}'.format(value))
				if(len(value)>0):
					insert_value=util.change_value_2_insert(value)
					dictVO={'record':record,'value':insert_value,'table_name':table_name,'own_uid1':own_uid1,'own_uid2':own_uid2}
					sqlVO=util.create_update_by_2uid_sqlVO(dictVO)
					print(sqlVO)
					models.BaseManage().direct_execute_query_sqlVO(sqlVO)
			print(sqlVO)

				#model.objects.filter(F(own_uid_col)=own_id).update(F(own_col)=insert_value)
				#print(sqlVO)
			print('end################################################{0}'.format(record))

def data_import(request):
	if request.method == 'POST':
		procedurename=request.POST['procedure']
		if procedurename.startswith("SALES2"):
			import_by_multikey(procedurename)
		else:
			import_by_single(procedurename)
	return render(request, MAIN_OUTFIT_BASE + 'import.html',{'title':"导入结果"})

'''
{'FROM_TABLE': 'db.tboj202', 'OWN_UID': 'heat_no', 'FROM_UID': 'heat_no', 'FRES', 'REAL_MEANING': '出钢量(t)',
'FROM_COL': 'steelWgt', 'FROM_DEPT': '炼钢转炉', 'OWN_TABLE': 'CONVERTER
'OWN_COL': 'steelWgt', 'CLASSIFICATION': '出钢量', 'REMARKS': '0', 'FROM_SYSTEM': 'MES',}
'''



def functionDemo(request):
	basepath='\\data_import\\media\\upload\\QG_USER.PRO_LF_HIS_CHRGDGEN.txt'
	filepath=BASE_DIR+basepath
	tables_info={}
	db_name='l2'
	#此处将有表名的循环
	tbList=[]
	with open(filepath,'r')as f:
		tb=f.readline()
		while tb:
			tbname=tb.strip()
			if(len(tbname)>0):
				tbList.append(tbname)
			tb=f.readline()
	print(tbList)

	for table_name in tbList:
		table_info={}
		column_sqlVO=util.create_get_columns_sqlVO(table_name,db_name)
		print(column_sqlVO)
		columns=models.BaseManage().direct_get_description(column_sqlVO)
		print(columns)
		table_info['columns']=columns
		sum_sqlVO=util.create_get_sum_sqlVO(columns[0][0],table_name,db_name)
		print(sum_sqlVO)
		rs=models.BaseManage().direct_select_query_sqlVO(sum_sqlVO)
		for key in rs[0]:
			total_num=rs[0][key]
		table_info['total_num']=total_num
		if total_num==0:
			tables_info[table_name]=table_info
			continue;
		for column in columns[0][1:]:
			column_info={}
			sql='SELECT '+column+' FROM '+table_name+' WHERE '+column+' IS NULL'
			null_num_sqlVO=util.create_sqlVO_by_dbname(sql,None,db_name)
			print(null_num_sqlVO)
			rs=models.BaseManage().direct_select_query_sqlVO(null_num_sqlVO)
			null_num=len(rs)
			column_info['null_num']=null_num
			print(null_num)
			null_rate=null_num/total_num
			column_info['null_rate']=null_rate
			#对“number”类型统计0出现的概率
			if(columns[1].get(column)=="DATETIME"):
				table_info[column]=column_info
				continue;
			elif(columns[1].get(column)=="NUMBER"):
				sql='SELECT COUNT('+column+') FROM '+table_name+' WHERE '+column+'=0'
			elif(columns[1].get(column)=="STRING"):
				sql="SELECT COUNT("+column+") FROM "+table_name+" WHERE "+column+"='0'"
			zero_num_sqlVO=util.create_sqlVO_by_dbname(sql,None,db_name)
			print(zero_num_sqlVO)
			rs=models.BaseManage().direct_select_query_sqlVO(zero_num_sqlVO)
			print(type(rs))
			if(len(rs)>0):
				for key in rs[0]:
					zero_num=rs[0][key]
					column_info['zero_num']=zero_num
				zero_rate=zero_num/total_num
				column_info['zero_rate']=zero_rate
			table_info[column]=column_info

		#还有缩进
		tables_info[table_name]=table_info

	#print(tables_info)
	util.write_ana_2_file(tbList,tables_info)

	contentVO={
		'title':'数据缺失度分析结果',
		'state':'success'
	}
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

def download_file(request):
	if request.method == 'GET':
		filepath=request.GET['filepath']
	def file_iterator(file_name, chunk_size=512):
		with open(file_name) as f:
		    while True:
		        c = f.read(chunk_size).decode('gbk','ignore').encode('utf-8','ignore') #以gbk编码读取
		        if c:
		            yield c
		        else:
		            break
	response = StreamingHttpResponse(file_iterator(filepath))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filepath)
	return response


def echarts(request):
	print('echarts示例')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request, MAIN_OUTFIT_BASE + 'echarts_demo.html',{'title':"青特钢大数据项目组——echarts示例"})


from data_import.liusinuo.main import main
from data_import.liusinuo.sql_market_share import sql_market_share
#from data_import.liusinuo.sql_stockControl import sql_stockControl
from data_import.sql_stockControl import sql_stockControl
def space(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == "GET":
		#print("执行了space的view")
		return render(request,'data_import/space.html',{'title':"青特钢大数据项目组数据管理"})
	elif request.method == "POST":
		print(request.POST)
		try:
			dictionary, conclusion, module_name, aspect_name, unite, maxValue = main(int(request.POST.get("module")),
										  								int(request.POST.get('aspect')),
										  								int(request.POST.get('dateChoose')),
										 						 		request.POST.get('sql_date1'),
										 						 		request.POST.get('sql_date2'),
										  								request.POST.get('sql_cust'),
										  								request.POST.get('tradeNo'),
										  								int(request.POST.get('space')),
										  								request.POST.get('space_detail'),
										  								request.POST.get('module_unit_key')
										  								)
			rst = []
			for key in dictionary.keys():
				rst.append({'name': key, 'value': dictionary.get(key)})
			return HttpResponse(json.dumps({'describe': conclusion,
				                            'result': rst,
				                            'module_name': module_name,
				                            'aspect_name': aspect_name,
				                            'unite': unite,
				                            'maxValue': maxValue}), content_type='text/json/text/text/text/text/')
		except Exception as ex:
			print(ex)


def time(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == "GET":
		return render(request,'data_import/time.html',{'title':"青特钢大数据项目组数据管理"})
	elif request.method == "POST":
		print(request.POST)
		try:
			dictionary, conclusion, module_name, aspect_name, unite, maxValue = main(int(request.POST.get("module")),
										  								int(request.POST.get('aspect')),
										  								int(request.POST.get('dateChoose')),
										 						 		request.POST.get('sql_date1'),
										 						 		request.POST.get('sql_date2'),
										  								request.POST.get('sql_cust'),
										  								request.POST.get('tradeNo'),
										  								int(request.POST.get('space')),
										  								request.POST.get('space_detail'),
										  								request.POST.get('module_unit_key')
										  								)
			rst = []
			for key in dictionary.keys():
				rst.append({'name': key, 'value': dictionary.get(key)})
			return HttpResponse(json.dumps({'describe': conclusion,
				                            'result': rst,
				                            'module_name': module_name,
				                            'aspect_name': aspect_name,
				                            'unite': unite,
				                            'maxValue': maxValue}), content_type='text/json/text/text/text/text/')
		except Exception as ex:
			print(ex)


def trade(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == "GET":
		return render(request,'data_import/trade.html',{'title':"青特钢大数据项目组数据管理"})
	elif request.method == "POST":
		print(request.POST)
		try:
			dictionary, conclusion, module_name, aspect_name, unite, maxValue = main(int(request.POST.get("module")),
										  								int(request.POST.get('aspect')),
										  								int(request.POST.get('dateChoose')),
										 						 		request.POST.get('sql_date1'),
										 						 		request.POST.get('sql_date2'),
										  								request.POST.get('sql_cust'),
										  								request.POST.get('tradeNo'),
										  								int(request.POST.get('space')),
										  								request.POST.get('space_detail'),
										  								request.POST.get('module_unit_key')
										  								)
			rst = []
			for key in dictionary.keys():
				rst.append({'name': key, 'value': dictionary.get(key)})
			return HttpResponse(json.dumps({'describe': conclusion,
				                            'result': rst,
				                            'module_name': module_name,
				                            'aspect_name': aspect_name,
				                            'unite': unite,
				                            'maxValue': maxValue}), content_type='text/json/text/text/text/text/')
		except Exception as ex:
			print(ex)


def cust_time(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == "GET":
		return render(request,'data_import/cust_time.html',{'title':"青特钢大数据项目组数据管理"})
	elif request.method == "POST":
		print(request.POST)
		try:

			dictionary, conclusion, module_name, aspect_name, unite, maxValue = main(int(request.POST.get("module")),
										  								int(request.POST.get('aspect')),
										  								int(request.POST.get('dateChoose')),
										 						 		request.POST.get('sql_date1'),
										 						 		request.POST.get('sql_date2'),
										  								request.POST.get('sql_cust'),
										  								request.POST.get('tradeNo'),
										  								request.POST.get('space'), #这里去掉了int()
										  								request.POST.get('space_detail'),
										  								request.POST.get('module_unit_key')
										  								)
			rst = []
			for key in dictionary.keys():
				rst.append({'name': key, 'value': dictionary.get(key)})

			return HttpResponse(json.dumps({'describe': conclusion,
				                            'result': rst,
				                            'module_name': module_name,
				                            'aspect_name': aspect_name,
				                            'unite': unite,
				                            'maxValue': maxValue}), content_type='text/json/text/text/text/text/')
		except Exception as ex:
			print(ex)


def cust_trade(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == "GET":
		return render(request,'data_import/cust_trade.html',{'title':"青特钢大数据项目组数据管理"})
	elif request.method == "POST":
		print(request.POST)
		try:
			print("+++++++++++++++++")
			dictionary, conclusion, module_name,aspect_name,unite,maxValue = main(int(request.POST.get("module")),
										  								int(request.POST.get('aspect')),
										  								int(request.POST.get('dateChoose')),
										 						 		request.POST.get('sql_date1'),
										 						 		request.POST.get('sql_date2'),
										  								request.POST.get('sql_cust'),
										  								request.POST.get('tradeNo'),
										  								request.POST.get('space'), #这里去掉了int()
										  								request.POST.get('space_detail'),
										  								request.POST.get('module_unit_key')
										  								)
			rst = []
			for key in dictionary.keys():
				rst.append({'name': key, 'value': dictionary.get(key)})
			print("********")
			return HttpResponse(json.dumps({'describe': conclusion,
				                            'result': rst,
				                            'module_name': module_name,
				                            'aspect_name': aspect_name,
				                            'unite': unite,
				                            'maxValue': maxValue}), content_type='text/json/text/text/text/text/')
		except Exception as ex:
			print(ex)


def stockControl(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == "GET":
		return render(request,'data_import/stockControl.html',{'title':"青特钢大数据项目组数据管理"})
	elif request.method == "POST":
		print(request.POST)
		print("正在执行 view.py 中的 库存管理 函数")
		try:
			dictionary, conclusion, module_name = sql_stockControl(int(request.POST.get("module")),
												request.POST.get('tradeNo'),
										  		request.POST.get('module_unit_key')
										  		)
			rst = []
			for key in dictionary.keys():
				rst.append({'name': key, 'value': dictionary.get(key)})
				print (type(dictionary.get(key)))
			print("geshi zhuanhuan wanbi")

			return HttpResponse(json.dumps({'describe': conclusion,
				                            'result': rst,
				                            'module_name': module_name
				                           }), content_type='text/json/text')
		except Exception as ex:
			print(ex)


def market_share(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == "GET":
		return render(request,'data_import/market_share.html',{'title':"青特钢大数据项目组数据管理"})
	elif request.method == "POST":
		print("====================================")
		print(request.POST)
		print("====================================")
		#print (" >>> 开始执行 view.py 中的 market_share 函数")
		try:
			ratio_dictionary, conclusion,all_dictionary = sql_market_share(request.POST.get("startYear"),
													request.POST.get('startMonth'),
													request.POST.get('endYear'),
											 		request.POST.get('endMonth')
														)


			ratio_rst = []
			for key in ratio_dictionary.keys():
				ratio_rst.append({'name': key, 'value': ratio_dictionary.get(key)})
			all_rst = []
			for key in all_dictionary.keys():
				all_rst.append({'name': key, 'value': all_dictionary.get(key)})
			#print (" >>>  view.py 中的 market_share 函数 执行到这里")
			#print (all_rst)
			return HttpResponse(json.dumps({'describe': conclusion,
				                            'result': ratio_rst,
				                            'all_dictionary':all_rst}), content_type='text/json/json/')
		except Exception as ex:
			print(ex)



#import data_import.liusinuo.update_mysql_space
from data_import.liusinuo.update_mysql_space import update_mysql_space_orderNo
from data_import.liusinuo.update_mysql_space import update_data_new_sales2_orderno_orderItem
from data_import.liusinuo.update_mysql_space import update_data_new_sales_displistno
from data_import.liusinuo.update_mysql_space import update_data_new_sales_loadno
from data_import.liusinuo.update_mysql_space import update_data_sales_new_loadno_collectno_receiveno
from data_import.liusinuo.update_mysql_space import update_data_sales_new_collectno
from data_import.liusinuo.update_mysql_space import update_data_sales_new_receiveno
from data_import.liusinuo.update_mysql_space import update_data_sales_new_rtnno
from data_import.liusinuo.update_mysql_space import update_data_sales_new_millsheetno
from data_import.liusinuo.update_mysql_space import update_data_sales_new_space_comparsion
from data_import.liusinuo.update_mysql_space import update_data_sales_new_marketshare
#更新数据仓库：销售部分——空间分析
def update_mysql_space(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_mysql_space可以执行")
	update_mysql_space_orderNo();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_orderno_orderItem(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_orderno_orderItem 可以执行")
	update_data_new_sales2_orderno_orderItem();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_displistno(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_displistno 可以执行")
	update_data_new_sales_displistno()
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_loadno(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_loadno 可以执行")
	update_data_new_sales_loadno();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_collectno(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_collectno 可以执行")
	update_data_sales_new_collectno();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_receiveno(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_receiveno 可以执行")
	update_data_sales_new_receiveno();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_rtnno(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_rtnno 可以执行")
	update_data_sales_new_rtnno();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_millsheetno(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_millsheetno 可以执行")
	update_data_sales_new_millsheetno();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def update_space_comparsion(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_millsheetno 可以执行")
	update_data_sales_new_space_comparsion();
	return HttpResponse(json.dumps(contentVO),content_type='application/json')



def update_space_marketshare(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	print("更新数据仓库 view.update_space_marketshare 可以执行")
	print(request.POST)
	print("===========================\n")

	update_data_sales_new_marketshare(request.POST.get("province"),
									request.POST.get('orderDate'),
									request.POST.get('salesWeight'),
									request.POST.get('month_value'),
									request.POST.get('year_value'))
	
	return HttpResponse(json.dumps(contentVO),content_type='application/json')






#从数据库动态加载钢种
from data_import import models
def getAllTradeNo_time(request):
	conn_mysql = models.BaseManage()
	sql_getAllTradeNo = "select c.tradeNo from data_import_sales_orderno a,data_import_sales2_orderno_orderitem c where c.orderNo = a.orderNo group by c.tradeNo"
	allTradeNo = conn_mysql.select(sql_getAllTradeNo)
	print (allTradeNo)
	#print (type(allTradeNo))

	# sqlVO={}
	# sqlVO["db_name"]="l2own"
	# sqlVO["sql"]="select distinct gk_no from qg_user.PRO_BOF_HIS_ALLFIELDS order by gk_no";
	# print(sqlVO["sql"])
	# scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)    #查询数据库
	# frame=DataFrame(scrapy_records)
	#print(frame['GK_NO'])

	# contentVO={
	# 	'title':'测试',
	# 	'state':'success'
	# }
	# # grape=[ele for ele in frame['GK_NO']]
	# #print(grape)
	# contentVO['result']=allTradeNo
	# return HttpResponse(json.dumps(contentVO),content_type='application/json')
	return HttpResponse(json.dumps({'result':allTradeNo}),content_type='json')


def lond_to_B(request):
	contentVO={
		'title':'测试',
		'state':'success'
	}
	ana_result={}
	ana_result=zhuanlu.PRO_BOF_HIS_ALLFIELDS_B
	contentVO['procedure_names']=ana_result
	#print(contentVO)
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

def bof_dataanalysis(request):
	print('转炉数据清洗')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/bof_dataanalysis.html',{'title':"青特钢大数据项目组数据管理"})


#请求成本单炉次bof_singlecost.html页面
def bof_singlecost(request):
	#print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/bof_singlecost.html',{'title':"青特钢大数据项目组数据管理"})


#跳转成本多炉次波动率页面
def bof_fluccost(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/bof_fluccost.html')

#跳转到质量单炉次
def bof_singlequality(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/bof_singlequality.html',{'title':"青特钢大数据项目组数据管理"})

#跳转到质量多炉次波动率页面
def bof_flucquality(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/bof_flucquality.html')



#跳转到分析工具analysis_tool.html页面
def analysis_tool(request):
	#print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/analysis_tool.html',{'title':"青特钢大数据项目组数据管理"})

#跳转到分析工具analysis_tool.html页面
def update_data_sales(request):
	#print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/update_data_sales.html',{'title':"青特钢大数据项目组数据管理"})
