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
def trade_sql(sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect):
	print("\n 时间：",sql_date1,"-",sql_date2,"\n","钢种：",tradeNo_list,"\n","地点：",space_name,"\n","分析内容：",aspect_name,"\n")
	passOrNot = 0
	tradeNo_rtn_reason_print = []
	trade_dict = {}
	chooseTrade_sum = 0
	allTrade_sum = 0
	weight_sum_all = 0
	weight_sum = 0
	rtn_sum_all = 0
	rtn_sum = 0
	tradeNo_weight = 0
	rtn_rate = 0

	if dateChoose == 1:  #订单时间
		#订单时间、总销量
		#sql_wgt = "select c.tradeNo,sum(c.orderWeight) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
		sql_wgt = "select a.tradeNo,sum(a.orderItemWeight) from data_sales2_new_orderno_orderItem a where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "'  group by a.tradeNo"
		#订单时间、总销售额
		#sql_amt = "select c.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
		sql_amt = "select a.tradeNo,sum(a.orderItemWeight * a.orderPrice) from data_sales2_new_orderno_orderItem a where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "'  group by a.tradeNo"
		#订单时间、总退货率、质量问题个数
		#sql_rtn = "select a.orderNo,a.custNo,a.tradeNo,sum(a.rtnWgt),a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + space_name +  "  and a.custNo = b.custNo  group by a.tradeNo"
		#sql_rtn = "select a.tradeNo,sum(a.rtnWgt) froam data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + space_name +  "  and a.custNo = b.custNo  group by a.tradeNo"
		#sql_rtn_reason = "select a.orderNo,a.custNo,a.tradeNo,a.rtnWgt,a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + space_name +  "  and a.custNo = b.custNo"
	elif dateChoose == 2:  #发货时间 【很慢】，平均查询时间为10s左右，查询本身就很慢
		#发货时间、总销量
		#sql_wgt = "select d.tradeNo,sum(a.realDeliWgt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 >= " + sql_date1 + " and a.createDate1 <= " + sql_date2 + " and a.orderNo = b.orderNo and c." + sql_ctry_prov_cty + " = '" + space_name + "' and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
		sql_wgt = "select a.tradeNo,sum(a.dispWeight) from data_sales_new_displistno a where a.dispDate >= " + sql_date1 + " and a.dispDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"
		#发货时间、总销售额
		#sql_amt = "select d.tradeNo,sum(a.prodAmt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 >= " + sql_date1 + " and a.createDate1 <= " + sql_date2 + " and a.orderNo = b.orderNo and c." + sql_ctry_prov_cty + " = '" + space_name + "' and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
		sql_amt = "select a.tradeNo,sum(a.dispAmt) from data_sales_new_displistno a where a.dispDate >= " + sql_date1 + " and a.dispDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"
	elif dateChoose == 3:  #派车履运时间(出货销账日期)
		#派车履运时间、总销量
		#sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
		sql_wgt = "select a.tradeNo,sum(a.loadWeight) from data_sales_new_loadno a where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "'  group by a.tradeNo"
		#派车履运时间、总销售额
		#sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
		sql_amt = "select a.tradeNo,sum(a.loadWeight * a.dispPrice) from data_sales_new_loadno a where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "'  group by a.tradeNo"
	elif dateChoose == 4:  #派车履运时间(结算时间)
		#派车履运时间、总销量
		#sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
		sql_wgt = "select a.tradeNo,sum(a.loadWeight) from data_sales_new_loadno a where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "'  group by a.tradeNo"
		#派车履运时间、总销售额
		#sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.custNo = b.custNo group by a.tradeNo"
		sql_amt = "select a.tradeNo,sum(a.loadWeight * a.dispPrice) from data_sales_new_loadno a where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "'  group by a.tradeNo"
	elif dateChoose == 5:  #装车通知时间
		#装车通知时间、总销量
		#sql_wgt = "select c.tradeNo,sum(c.realWgt) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate >= " + sql_date1 + " and a.effectDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
		sql_wgt = "select a.tradeNo,sum(a.loadWeight) from data_sales_new_collectno a where a.collectDate >= " + sql_date1 + " and a.collectDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"
		#装车通知时间、总销售额
		#sql_amt = "select c.tradeNo,sum(c.realWgt * c.unitPrice) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate >= " + sql_date1 + " and a.effectDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
		sql_amt = "select a.tradeNo,sum(a.loadWeight * a.dispPrice) from data_sales_new_collectno a where a.collectDate >= " + sql_date1 + " and a.collectDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"
	# elif dateChoose == 6:  #订单存货档建立时间   ######## 数据导的不全，需要重新导这个表
	# 	#订单存货档建立时间、总销量
	# 	sql_wgt = "select a.tradeNo,sum(a.labelWgt) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 >= " + sql_date1 + " and a.createDate121 <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
	# 	#订单存货档建立时间、总销售额
	# 	sql_amt = "select a.tradeNo,sum(a.labelWgt * c.basePrice) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 >= " + sql_date1 + " and a.createDate121 <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
	elif dateChoose == 7:  #质保书时间
		#质保书时间、总销量
		#sql_wgt = "select a.tradeNo,sum(c.orderWeight) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate >= " + sql_date1 + " and a.reviseDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
		sql_wgt = "select a.tradeNo,sum(a.millsheetWeight) from data_sales_new_millsheetno a  where a.millsheetDate >= " + sql_date1 + " and a.millsheetDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"
		#质保书时间、总销售额
		#sql_amt = "select a.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate >= " + sql_date1 + " and a.reviseDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
		sql_amt = "select a.tradeNo,sum(a.millsheetWeight  * a.dispPrice) from data_sales_new_millsheetno a  where a.millsheetDate >= " + sql_date1 + " and a.millsheetDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"
	else: #外库接收时间    #########  搞清楚 外库接收 与 派车履运 的关系，他们是互斥关系，现在需要重新导labelno表，以使得此时间可以得出结果
		#外库接收时间、总销量
		#sql_wgt = "select c.tradeNo,sum(a.receiveWgt) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate >= " + sql_date1 + " and a.updateDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"
		sql_wgt = "select a.tradeNo,sum(a.receiveWeight) from data_sales_new_receiveno a where a.receiveDate >= " + sql_date1 + " and a.receiveDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"
		#外库接收时间、总销售额
		#sql_amt = "select c.tradeNo,sum(a.receiveWgt * c.unitPrice) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate >= " + sql_date1 + " and a.updateDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name + "' and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"
		sql_amt = "select a.tradeNo,sum(a.receiveWeight * a.dispPrice) from data_sales_new_receiveno a where a.receiveDate >= " + sql_date1 + " and a.receiveDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name + "' group by a.tradeNo"

	#总退货率、质量问题个数   不分时间
	sql_rtn = "select a.tradeNo,sum(a.rtnWeight) from data_sales_new_rtnno a where a.rtnDate >= " + sql_date1 + " and a.rtnDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name +  "' group by a.tradeNo"
	#sql_rtn = "select a.tradeNo,sum(a.rtnWgt) from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name +  "'  and a.custNo = b.custNo  group by a.tradeNo"
	sql_rtn_reason = "select a.rtnNo,a.orderNo,a.custNo,a.tradeNo,a.rtnWeight,a.rtnPrice,a.rtnReason from data_sales_new_rtnno  a where a.rtnDate >= " + sql_date1 + " and a.rtnDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name +  "' "
	#sql_rtn_reason = "select a.rtnNo,a.orderNo,a.custNo,a.tradeNo,a.rtnWgt,a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name +  "'  and a.custNo = b.custNo"
	sql_rtn_reason_count = "select a.tradeNo,a.orderNo,a.orderItem,a.rtnReason from data_sales_new_rtnno a where a.rtnDate >= " + sql_date1 + " and a.rtnDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + space_name +  "'   group by a.orderNo,a.orderItem,a.rtnReason"
	#sql_rtn_reason_count = "select a.tradeNo,a.orderNo,a.orderItem,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + space_name +  "'  and a.custNo = b.custNo group by a.orderNo,a.orderItem,a.rtnReason"


	#=====================【 求 和 存 入 字 典 】==================================
	i = 0
	for tradeNo in tradeNo_list:
		i = i + 1
		if aspect == 1:
			tradeNo_wgt_list = conn_mysql.select(sql_wgt)
			for tradeNo_wgt in tradeNo_wgt_list:
				if i == 1:
					allTrade_sum += tradeNo_wgt[1] #全部钢种重量求和
				else:
					pass

				if tradeNo_wgt[0] == tradeNo: #如果订单中有这个钢种
					trade_dict[tradeNo] = tradeNo_wgt[1]  #所选钢种每个钢种的重量 添加到dict中
					print ("单个钢种总销量：\t",tradeNo,tradeNo_wgt[1])
					chooseTrade_sum += tradeNo_wgt[1] #所选钢种 重量求和
				else:
					pass

		elif aspect == 2:
			tradeNo_amt_list = conn_mysql.select(sql_amt)
			for tradeNo_amt in tradeNo_amt_list:
				if i == 1:
					allTrade_sum += tradeNo_amt[1] #全部钢种重量求和
				else:
					pass

				if tradeNo_amt[0] == tradeNo: #如果订单中有这个钢种
					trade_dict[tradeNo] = tradeNo_amt[1]  #所选钢种每个钢种的重量 添加到dict中
					print ("单个钢种总销售额：\t",tradeNo,tradeNo_amt[1])
					chooseTrade_sum += tradeNo_amt[1] #重量求和
				else:
					pass

		elif aspect == 3:
			tradeNo_wgt_list = conn_mysql.select(sql_wgt)
			for tradeNo_wgt in tradeNo_wgt_list: #在订单中
				if i == 1:
					weight_sum_all += tradeNo_wgt[1] #全部钢种重量求和
				else:
					pass

				if tradeNo_wgt[0] == tradeNo: #订单与退货是同一钢种
					tradeNo_weight = tradeNo_wgt[1]  #求所选钢种每个钢种的重量
					weight_sum += tradeNo_wgt[1] #所选钢种 重量求和
				else:
					pass
			#print (tradeNo,"\n本钢种销量",tradeNo_weight)

			tradeNo_rtn_list = conn_mysql.select(sql_rtn)
			tradeNo_rtn_weight = 0

			for tradeNo_rtn in tradeNo_rtn_list:#在退货单中
				if i == 1:
					rtn_sum_all += tradeNo_rtn[1] #全部钢种重量求和
					#print ("每一个的退货",tradeNo_rtn)
				else:
					pass
				#print ("总退货",rtn_sum_all)
				if tradeNo_rtn[0] == tradeNo: #如果退货单中有这个钢种
					tradeNo_rtn_weight = tradeNo_rtn[1] #求退货重量
					rtn_sum += tradeNo_rtn[1]
					#print ("所选的退货",tradeNo,tradeNo_rtn[0],tradeNo_rtn)
				else:
					pass
			#print (tradeNo,"\n本钢种退货量",tradeNo_rtn_weight)


			#单个钢种退货率计算
			if tradeNo_weight != 0:
				rtn_rate = ( tradeNo_rtn_weight / tradeNo_weight ) * 100
				rtn_rate = float(str(rtn_rate)[0:8])
				print ("钢种退货率：\t%s %.5f" % (tradeNo,rtn_rate),"%")

			else:
				print ("钢种退货率：\t总销量为0，无法计算退货率！")
				rtn_rate = "总销量为0，无法计算退货率！"

			trade_dict[tradeNo] = rtn_rate

		else:
			count = 0
			tradeNo_rtn_reason_count_list = conn_mysql.select(sql_rtn_reason_count)
			for tradeNo_rtn_count_reason in tradeNo_rtn_reason_count_list:
				allTrade_sum += 1
				if tradeNo == tradeNo_rtn_count_reason[0]:
					count = count + 1
					trade_dict[tradeNo]  = count
					chooseTrade_sum += 1
			print ("质量问题个数：",tradeNo,count)


		if aspect == 3 or aspect == 4:
			tradeNo_rtn_reason_list = conn_mysql.select(sql_rtn_reason)
			for tradeNo_rtn_reason in tradeNo_rtn_reason_list:
				if tradeNo_rtn_reason[3] == tradeNo:
					tradeNo_rtn_reason_print.append(tradeNo_rtn_reason)
			#print ("质量问题原因",tradeNo_rtn_reason_print)
		else:
			pass

	#退货部分总和
	if aspect == 3:
		rtn_rate = 0
		#所选钢种总退货率计算
		if weight_sum != 0:
			rtn_rate = ( rtn_sum / weight_sum ) * 100
			rtn_rate = float(str(rtn_rate)[0:8])
			print ("所选总退货率：\t%.5f" % (rtn_rate),"%")

		else:
			print ("所选总退货率：\t总销量为0，无法计算退货率！")
			rtn_rate = "总销量为0，无法计算退货率！"
		chooseTrade_sum = rtn_rate

		rtn_rate = 0
		#全部钢种总退货率计算
		if weight_sum_all != 0:
			rtn_rate = ( rtn_sum_all / weight_sum_all ) * 100
			rtn_rate = float(str(rtn_rate)[0:8])
			print ("总退货率：\t%.5f" % (rtn_rate),"%")

		else:
			print ("总退货率：\t总销量为0，无法计算退货率！")
			rtn_rate = "总销量为0，无法计算退货率！"
		allTrade_sum = rtn_rate
	else:
		pass


	if len(tradeNo_rtn_reason_print) == 0:
		passOrNot = 1
	else:
		pass
	#print ("全体钢种总销量",weight_sum_all,"所选销量",weight_sum)
	#print ("全体钢种退货量",rtn_sum_all,"所选钢种退货量",rtn_sum)
	print ("\n所选钢种：\t",chooseTrade_sum)
	print ("\n全部钢种\t",allTrade_sum)
	return trade_dict,passOrNot,tradeNo_rtn_reason_print,chooseTrade_sum,allTrade_sum
	#return sql_wgt,sql_amt,sql_rtn,sql_rtn_reason,sql_rtn_reason_count
