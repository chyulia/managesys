'''

2016-10-21

对应 space.py 代码

控制 空间分析 的 sql 语句

'''
from data_import import models
conn_mysql = models.BaseManage()
#=====================【 SQL 语 句 查 询 】==================================
'''
时间：订单？发货？派车（出货销账）？派车（结算）？装车？存货？质保书？外库接收？
地点：世界（国家）？国（省）？省（市）？
内容：销量？销售额？退货？主要质量问题？

时间 地点 钢种 销量

'''
def cust_sql(sql_date1,sql_date2,aspect_name,dateChoose,aspect,sql_cust):
	print("\n 时间：",sql_date1,"-",sql_date2,"\n","客户：",sql_cust,"\n","分析内容：",aspect_name,"\n")
	passOrNot = 0
	tradeNo_rtn_reason_print = []
	cust_dict = {}

	if dateChoose == 1:  #订单时间
		#订单时间、总销量
		sql_wgt = "select c.tradeNo,sum(c.orderWeight) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
		#订单时间、总销售额
		sql_amt = "select c.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
		#订单时间、总退货率、质量问题个数
		#sql_rtn = "select a.orderNo,a.custNo,a.tradeNo,sum(a.rtnWgt),a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + sql_space +  "  and a.custNo = b.custNo  group by a.tradeNo"
		#sql_rtn = "select a.tradeNo,sum(a.rtnWgt) from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + sql_space +  "  and a.custNo = b.custNo  group by a.tradeNo"
		#sql_rtn_reason = "select a.orderNo,a.custNo,a.tradeNo,a.rtnWgt,a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + sql_space +  "  and a.custNo = b.custNo"
	elif dateChoose == 2:  #发货时间 【很慢】，平均查询时间为10s左右，查询本身就很慢
		#发货时间、总销量
		sql_wgt = "select d.tradeNo,sum(a.realDeliWgt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 >= " + sql_date1 + " and a.createDate1 <= " + sql_date2 + " and a.orderNo = b.orderNo and b.custNo = " + sql_cust + " and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
		#发货时间、总销售额
		sql_amt = "select d.tradeNo,sum(a.prodAmt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 >= " + sql_date1 + " and a.createDate1 <= " + sql_date2 + " and a.orderNo = b.orderNo and b.custNo = " + sql_cust + " and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
	elif dateChoose == 3:  #派车履运时间(出货销账日期)
		#派车履运时间、总销量
		sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo group by a.tradeNo"
		#派车履运时间、总销售额
		sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo group by a.tradeNo"
	elif dateChoose == 4:  #派车履运时间(结算时间)
		#派车履运时间、总销量
		sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo group by a.tradeNo"
		#派车履运时间、总销售额
		sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo group by a.tradeNo"
	elif dateChoose == 5:  #装车通知时间
		#装车通知时间、总销量
		sql_wgt = "select c.tradeNo,sum(c.realWgt) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate >= " + sql_date1 + " and a.effectDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
		#装车通知时间、总销售额
		sql_amt = "select c.tradeNo,sum(c.realWgt * c.unitPrice) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate >= " + sql_date1 + " and a.effectDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
	elif dateChoose == 6:  #订单存货档建立时间   ######## 数据导的不全，需要重新导这个表
		#订单存货档建立时间、总销量
		sql_wgt = "select a.tradeNo,sum(a.labelWgt) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 >= " + sql_date1 + " and a.createDate121 <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
		#订单存货档建立时间、总销售额
		sql_amt = "select a.tradeNo,sum(a.labelWgt * c.basePrice) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 >= " + sql_date1 + " and a.createDate121 <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
	elif dateChoose == 7:  #质保书时间
		#质保书时间、总销量
		sql_wgt = "select a.tradeNo,sum(c.orderWeight) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate >= " + sql_date1 + " and a.reviseDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
		#质保书时间、总销售额
		sql_amt = "select a.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate >= " + sql_date1 + " and a.reviseDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
	else: #外库接收时间    #########  搞清楚 外库接收 与 派车履运 的关系，他们是互斥关系，现在需要重新导labelno表，以使得此时间可以得出结果
		#外库接收时间、总销量
		sql_wgt = "select c.tradeNo,sum(a.receiveWgt) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate >= " + sql_date1 + " and a.updateDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"
		#外库接收时间、总销售额
		sql_amt = "select c.tradeNo,sum(a.receiveWgt * c.unitPrice) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate >= " + sql_date1 + " and a.updateDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"

	#总退货率、质量问题个数   不分时间
	sql_rtn = "select a.tradeNo,sum(a.rtnWgt) from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo  group by a.tradeNo"
	sql_rtn_reason = "select a.rtnNo,a.orderNo,a.custNo,a.tradeNo,a.rtnWgt,a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo"
	sql_rtn_reason_count = "select a.tradeNo,a.orderNo,a.orderItem,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b.custNo = " + sql_cust + " and a.custNo = b.custNo group by a.orderNo,a.orderItem,a.rtnReason"

	#=====================【 求 和 存 入 字 典 】==================================

	if aspect == 1 :
		tradeNo_wgt_list = conn_mysql.select(sql_wgt)
		for tradeNo_wgt in tradeNo_wgt_list:
			cust_dict[tradeNo_wgt[0]] = tradeNo_wgt[1]
			print ("总销量：\t",tradeNo_wgt[0], tradeNo_wgt[1])

	elif aspect == 2:
		tradeNo_amt_list = conn_mysql.select(sql_amt)
		for tradeNo_amt in tradeNo_amt_list:
			cust_dict[tradeNo_amt[0]] = tradeNo_amt[1]
			print ("总销售额：\t",tradeNo_amt[0],tradeNo_amt[1])

	elif aspect == 3:

		tradeNo_wgt_list = conn_mysql.select(sql_wgt)
		tradeNo_rtn_list = conn_mysql.select(sql_rtn)
		rtn_rate = 0
		weight_tradeNo = 0

		for tradeNo_rtn in tradeNo_rtn_list: #求总退货
			rtn_readeNo = tradeNo_rtn[1]
			print (rtn_readeNo)
			for tradeNo_wgt in tradeNo_wgt_list: #总销量
				if tradeNo_rtn[0] == tradeNo_wgt[0]:
					weight_tradeNo = tradeNo_wgt[1]
					print (weight_tradeNo)
				if weight_tradeNo != 0:
					rtn_rate = ( rtn_readeNo / weight_tradeNo ) * 100
					rtn_rate = float(str(rtn_rate)[0:8])
					print ("总退货率：\t%s%.5f" % (tradeNo_rtn[0],rtn_rate),"%")
				else:
					print ("总退货率：\t总销量为0，无法计算退货率！")
					rtn_rate = "总销量为0，无法计算退货率！"
		#tradeNo_rtn_rsn_list = conn_mysql.select(sql_rtn_reason)
		#print ("退货原因：\t",tradeNo_rtn_rsn_list)
		#print ("\n")
			cust_dict[tradeNo_rtn[0]] = rtn_rate
	else:
		count = 1
		cust_dict = {}
		tradeNo_rtn_reason_count_list = conn_mysql.select(sql_rtn_reason_count)
		for tradeNo_rtn_count_reason in tradeNo_rtn_reason_count_list:
			if tradeNo_rtn_count_reason[0] not in cust_dict:
				cust_dict[tradeNo_rtn_count_reason[0]] = 1
			else:
				cust_dict[tradeNo_rtn_count_reason[0]] += 1
		for tradeNo in cust_dict:
			print ("质量问题个数：",tradeNo,cust_dict[tradeNo])


	if aspect == 3 or aspect == 4:
		tradeNo_rtn_reason_list = conn_mysql.select(sql_rtn_reason)
		for tradeNo_rtn_reason in tradeNo_rtn_reason_list:
			tradeNo_rtn_reason_print.append(tradeNo_rtn_reason)
		#print ("质量问题原因",tradeNo_rtn_reason_print)
	else:
		pass

	if len(tradeNo_rtn_reason_print) == 0:
		passOrNot = 1
	else:
		pass
	#print (tradeNo_rtn_reason_print)
	return cust_dict,passOrNot,tradeNo_rtn_reason_print
	#return sql_wgt,sql_amt,sql_rtn,sql_rtn_reason,sql_rtn_reason_count
