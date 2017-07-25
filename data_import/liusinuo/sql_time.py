'''

2016-10-21

对应 space.py 代码

控制 空间分析 的 sql 语句

'''
from . import mysql
from data_import import models
conn_mysql = models.BaseManage()
import datetime

#=====================【 SQL 语 句 查 询 】==================================

def time_sql(sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect):
	print("\n 时间：",sql_date1,"-",sql_date2,"\n","钢种：",tradeNo_list,"\n","地点：",space_name,"\n","分析内容：",aspect_name,"\n")

	sql_date1 = datetime.datetime.strptime(sql_date1, '%Y%m%d')
	sql_date2 = datetime.datetime.strptime(sql_date2, '%Y%m%d')
	xDay = (sql_date2 - sql_date1).days
	#print (xDay)
	aDay = datetime.timedelta(days=1)
	#print (aDay)
	i = 0

	time_dict = {}
	# time_dict_day = {}
	# time_dict_allDay = {}
	rtn_sum_dict = {}
	weight_sum_dict ={}
	passOrNot = 0
	tradeNo_rtn_reason_print = []

	while i <= xDay:

		#每次将日期更新为后一天
		if i == 0:
			sql_date = sql_date1.strftime('%Y%m%d')
			#print (sql_date1.strftime('%Y%m%d'))
			i += 1
		else:
			sql_date = datetime.datetime.strptime(sql_date, '%Y%m%d') + aDay
			#print (sql_date.strftime('%Y%m%d'))
			sql_date = sql_date.strftime('%Y%m%d') #格式转换
			i += 1

		if dateChoose == 1:  #订单时间
			#订单时间、总销量
			sql_wgt = "select c.tradeNo,sum(c.orderWeight) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
			#print (sql_wgt)
			#订单时间、总销售额
			sql_amt = "select c.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
			#订单时间、总退货率、质量问题个数
		elif dateChoose == 2:  #发货时间 【很慢】，平均查询时间为10s左右，查询本身就很慢
			#发货时间、总销量
			sql_wgt = "select d.tradeNo,sum(a.realDeliWgt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 = " + sql_date + " and a.orderNo = b.orderNo and c." + sql_ctry_prov_cty + " = '" + space_name + "' and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
			#发货时间、总销售额
			sql_amt = "select d.tradeNo,sum(a.prodAmt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 = " + sql_date + " and a.orderNo = b.orderNo and c." + sql_ctry_prov_cty + " = '" + space_name + "' and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
		elif dateChoose == 3:  #派车履运时间(出货销账日期)
			#派车履运时间、总销量
			sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
			#派车履运时间、总销售额
			sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
		elif dateChoose == 4:  #派车履运时间(结算时间)
			#派车履运时间、总销量
			sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
			#派车履运时间、总销售额
			sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
		elif dateChoose == 5:  #装车通知时间
			#装车通知时间、总销量
			sql_wgt = "select c.tradeNo,sum(c.realWgt) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
			#装车通知时间、总销售额
			sql_amt = "select c.tradeNo,sum(c.realWgt * c.unitPrice) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
		elif dateChoose == 6:  #订单存货档建立时间   ######## 数据导的不全，需要重新导这个表
			#订单存货档建立时间、总销量
			sql_wgt = "select a.tradeNo,sum(a.labelWgt) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
			#订单存货档建立时间、总销售额
			sql_amt = "select a.tradeNo,sum(a.labelWgt * c.basePrice) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
		elif dateChoose == 7:  #质保书时间
			#质保书时间、总销量
			sql_wgt = "select a.tradeNo,sum(c.orderWeight) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
			#质保书时间、总销售额
			sql_amt = "select a.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
		else: #外库接收时间    #########  搞清楚 外库接收 与 派车履运 的关系，他们是互斥关系，现在需要重新导labelno表，以使得此时间可以得出结果
			#外库接收时间、总销量
			sql_wgt = "select c.tradeNo,sum(a.receiveWgt) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"
			#外库接收时间、总销售额
			sql_amt = "select c.tradeNo,sum(a.receiveWgt * c.unitPrice) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"

		#总退货率、质量问题个数   不分时间
		sql_rtn = "select a.tradeNo,sum(a.rtnWgt) from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name +  "'  and a.custNo = b.custNo  group by a.tradeNo"
		sql_rtn_reason = "select a.rtnNo,a.orderNo,a.custNo,a.tradeNo,a.rtnWgt,a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name +  "'  and a.custNo = b.custNo"
		sql_rtn_reason_count = "select a.tradeNo,a.orderNo,a.orderItem,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate = " + sql_date + " and b." + sql_ctry_prov_cty + " = '" + space_name +  "'  and a.custNo = b.custNo group by a.orderNo,a.orderItem,a.rtnReason"

		#=====================【 求 和 存 入 字 典 】==================================

		if aspect == 1 :
			tradeNo_wgt_list = conn_mysql.select(sql_wgt)
			weight_sum = 0
			for tradeNo in tradeNo_list:  #所选钢种
				for tradeNo_wgt in tradeNo_wgt_list:
					if tradeNo_wgt[0] == tradeNo: #如果订单中有这个钢种
						weight_sum += tradeNo_wgt[1] #重量求和
					else:
						pass
			#print ("总销量：\t",sql_date,weight_sum)
			#print ("\n")

			time_dict[sql_date] = weight_sum
		elif aspect == 2:
			tradeNo_amt_list = conn_mysql.select(sql_amt)
			amount_sum = 0
			for tradeNo in tradeNo_list:  #所选钢种
				for tradeNo_amt in tradeNo_amt_list:
					if tradeNo_amt[0] == tradeNo: #如果订单中有这个钢种
						amount_sum += tradeNo_amt[1] #重量求和
					else:
						pass
			#print ("总销售额：\t",sql_date,amount_sum)
			#print ("\n")
			time_dict[sql_date] = amount_sum
		elif aspect == 3:
			#总销量
			tradeNo_wgt_list = conn_mysql.select(sql_wgt)
			weight_sum = 0
			for tradeNo in tradeNo_list:  #所选钢种
				for tradeNo_wgt in tradeNo_wgt_list:
					if tradeNo_wgt[0] == tradeNo: #如果订单中有这个钢种
						weight_sum += tradeNo_wgt[1] #重量求和
					else:
						pass
			#求总退货
			tradeNo_rtn_list = conn_mysql.select(sql_rtn)
			rtn_sum = 0
			rtn_rate = 0
			for tradeNo in tradeNo_list:  #所选钢种
				for tradeNo_rtn in tradeNo_rtn_list:
					if tradeNo_rtn[0] == tradeNo: #如果订单中有这个钢种
						rtn_sum += tradeNo_rtn[1] #重量求和
					else:
						pass
			if weight_sum != 0:
				rtn_rate = ( rtn_sum / weight_sum ) * 100
				rtn_rate = float(str(rtn_rate)[0:8])
			#	print ("总退货率：\t%s%.5f" % (sql_date,rtn_rate),"%")
			else:
			#	print ("总退货率：\t总销量为0，无法计算退货率！")
				rtn_rate = "总销量为0，无法计算退货率！"
			#tradeNo_rtn_rsn_list = conn_mysql.select(sql_rtn_reason)
			#print ("退货原因：\t",tradeNo_rtn_rsn_list)
			#print ("\n")
			time_dict[sql_date] = rtn_rate
			#每日的退货重量与总重量的结果存储起来
			rtn_sum_dict[sql_date] = rtn_sum  #每日退货重量
			weight_sum_dict[sql_date] = weight_sum  #每日总销量
			# #每日结果存储起来
			# time_dict_day['rtn_rate'] = rtn_rate
			# time_dict_day['rtn_sum'] = rtn_sum
			# time_dict_day['weight_sum'] = weight_sum
			# #将每日结果存到一个大字典中
			# time_dict_allDay[sql_date] = time_dict_day
		else:
			count = 0
			tradeNo_rtn_reason_count_list = conn_mysql.select(sql_rtn_reason_count)
			for tradeNo in tradeNo_list:
				for tradeNo_rtn_count_reason in tradeNo_rtn_reason_count_list:
					if tradeNo == tradeNo_rtn_count_reason[0]:
						count = count + 1
			#print ("质量问题个数：",sql_date,count)
			time_dict[sql_date] = count


		if aspect == 3 or aspect == 4:
			tradeNo_rtn_reason_list = conn_mysql.select(sql_rtn_reason)
			#print (tradeNo_rtn_reason_list)
			for tradeNo in tradeNo_list:  #所选钢种
				for tradeNo_rtn_reason in tradeNo_rtn_reason_list:
					if tradeNo_rtn_reason[3] == tradeNo:
						tradeNo_rtn_reason_print.append(tradeNo_rtn_reason)
			#print ("质量问题原因",tradeNo_rtn_reason_print)

		else:
			pass
	if len(tradeNo_rtn_reason_print) == 0:
		passOrNot = 1
	else:
		pass
	#print (tradeNo_rtn_reason_print)
	#print (passOrNot)

	#如果是退货率的话，需要存储每日的退货量与总销量，以保证后续计算结果正确
	if aspect == 3:
		time_dict_rtn = {} #将全部结果存储到同一个dictionary中
		time_dict_rtn['time_dict'] = time_dict #最原始得到的退货率
		time_dict_rtn['rtn_sum_dict'] = rtn_sum_dict #退货重量
		time_dict_rtn['weight_sum_dict'] = weight_sum_dict #总销量
		#print (time_dict_rtn)
		return time_dict_rtn,passOrNot,tradeNo_rtn_reason_print
	else:
		return time_dict,passOrNot,tradeNo_rtn_reason_print
	#return sql_wgt,sql_amt,sql_rtn,sql_rtn_reason,sql_rtn_reason_count
