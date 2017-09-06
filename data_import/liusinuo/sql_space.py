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
def space_sql(space_dict,sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect):
	print("\n 时间：",sql_date1,"-",sql_date2,"\n","钢种：",tradeNo_list,"\n","地点：",space_name,"\n","分析内容：",aspect_name,"\n")
	passOrNot = 0
	tradeNo_rtn_reason_print = []
	for sql_space in space_dict:
		if dateChoose == 1:  #订单时间
			#订单时间、总销量
			#sql_wgt = "select c.tradeNo,sum(c.orderWeight) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
			sql_wgt = "select a.tradeNo,sum(a.orderItemWeight) from data_sales2_new_orderno_orderItem a where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "'  group by a.tradeNo"
			#订单时间、总销售额
			#sql_amt = "select c.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.custNo = b.custNo and c.orderNo = a.orderNo group by c.tradeNo"
			sql_amt = "select a.tradeNo,sum(a.orderItemWeight * a.orderPrice) from data_sales2_new_orderno_orderItem a where a.orderDate >= " + sql_date1 + " and a.orderDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "'  group by a.tradeNo"
			#订单时间、总退货率、质量问题个数
			#sql_rtn = "select a.orderNo,a.custNo,a.tradeNo,sum(a.rtnWgt),a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + sql_space +  "  and a.custNo = b.custNo  group by a.tradeNo"
			#sql_rtn = "select a.tradeNo,sum(a.rtnWgt) from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + sql_space +  "  and a.custNo = b.custNo  group by a.tradeNo"
			#sql_rtn_reason = "select a.orderNo,a.custNo,a.tradeNo,a.rtnWgt,a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = " + sql_space +  "  and a.custNo = b.custNo"
		elif dateChoose == 2:  #发货时间 【===【以前的sql很慢，新的很快】===】 【很慢】，平均查询时间为10s左右，查询本身就很慢
			#发货时间、总销量
			#sql_wgt = "select d.tradeNo,sum(a.realDeliWgt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 >= " + sql_date1 + " and a.createDate1 <= " + sql_date2 + " and a.orderNo = b.orderNo and c." + sql_ctry_prov_cty + " = '" + sql_space + "' and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
			sql_wgt = "select a.tradeNo,sum(a.dispWeight) from data_sales_new_displistno a where a.dispDate >= " + sql_date1 + " and a.dispDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"
			#发货时间、总销售额
			#sql_amt = "select d.tradeNo,sum(a.prodAmt) from data_import_sales_displistno a,data_import_sales_orderno b,data_import_sales_custplace c,data_import_sales2_orderno_orderitem d where a.createDate1 >= " + sql_date1 + " and a.createDate1 <= " + sql_date2 + " and a.orderNo = b.orderNo and c." + sql_ctry_prov_cty + " = '" + sql_space + "' and b.custNo = c.custNo and d.orderNo = a.orderNo and d.orderItem = a.orderItem group by d.tradeNo"
			sql_amt = "select a.tradeNo,sum(a.dispAmt) from data_sales_new_displistno a where a.dispDate >= " + sql_date1 + " and a.dispDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"
		elif dateChoose == 3:  #派车履运时间(出货销账日期)
			#派车履运时间、总销量
			#sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.custNo = b.custNo group by a.tradeNo"
			sql_wgt = "select a.tradeNo,sum(a.loadWeight) from data_sales_new_loadno a where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "'  group by a.tradeNo"
			#派车履运时间、总销售额
			#sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.custNo = b.custNo group by a.tradeNo"
			sql_amt = "select a.tradeNo,sum(a.loadWeight * a.dispPrice) from data_sales_new_loadno a where a.shipDate >= " + sql_date1 + " and a.shipDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "'  group by a.tradeNo"
		elif dateChoose == 4:  #派车履运时间(结算时间)
			#派车履运时间、总销量
			#$sql_wgt = "select a.tradeNo,sum(a.realWgt) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.custNo = b.custNo group by a.tradeNo"
			sql_wgt = "select a.tradeNo,sum(a.loadWeight) from data_sales_new_loadno a where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "'  group by a.tradeNo"
			#派车履运时间、总销售额
			#sql_amt = "select a.tradeNo,sum(a.realWgt * a.unitPrice) from data_import_sales_loadno a,data_import_sales_custplace b where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.custNo = b.custNo group by a.tradeNo"
			sql_amt = "select a.tradeNo,sum(a.loadWeight * a.dispPrice) from data_sales_new_loadno a where a.settleDate >= " + sql_date1 + " and a.settleDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "'  group by a.tradeNo"
		elif dateChoose == 5:  #装船通知时间
			#装车通知时间、总销量
			#sql_wgt = "select c.tradeNo,sum(c.realWgt) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate >= " + sql_date1 + " and a.effectDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
			sql_wgt = "select a.tradeNo,sum(a.loadWeight) from data_sales_new_collectno a where a.collectDate >= " + sql_date1 + " and a.collectDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"
			#装车通知时间、总销售额
			#sql_amt = "select c.tradeNo,sum(c.realWgt * c.unitPrice) from data_import_sales_collectno a,data_import_sales_custplace b,data_import_sales_loadno c where a.effectDate >= " + sql_date1 + " and a.effectDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and c.custNo = b.custNo and a.collectNo = c.collectNo group by c.tradeNo"
			sql_amt = "select a.tradeNo,sum(a.loadWeight * a.dispPrice) from data_sales_new_collectno a where a.collectDate >= " + sql_date1 + " and a.collectDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"
		#不需要这个选项了
		elif dateChoose == 6:  #订单存货档建立时间   ######## 数据导的不全，需要重新导这个表
			#订单存货档建立时间、总销量
			sql_wgt = "select a.tradeNo,sum(a.labelWgt) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 >= " + sql_date1 + " and a.createDate121 <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
			#订单存货档建立时间、总销售额
			sql_amt = "select a.tradeNo,sum(a.labelWgt * c.basePrice) from data_import_sales_labelno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.createDate121 >= " + sql_date1 + " and a.createDate121 <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.orderNo = c.orderNo and a.orderItem = c.orderItem and a.customerNo = b.custNo group by a.tradeNo"
		elif dateChoose == 7:  #质保书时间
			#质保书时间、总销量
			#sql_wgt = "select a.tradeNo,sum(c.orderWeight) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate >= " + sql_date1 + " and a.reviseDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
			sql_wgt = "select a.tradeNo,sum(a.millsheetWeight) from data_sales_new_millsheetno a  where a.millsheetDate >= " + sql_date1 + " and a.millsheetDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"
			#质保书时间、总销售额
			#sql_amt = "select a.tradeNo,sum(c.orderWeight * c.basePrice) from data_import_sales_millsheetno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.reviseDate >= " + sql_date1 + " and a.reviseDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and a.customerNo = b.custNo and c.orderNo = a.orderNo and a.item = c.orderItem group by a.tradeNo"
			sql_amt = "select a.tradeNo,sum(a.millsheetWeight  * a.dispPrice) from data_sales_new_millsheetno a  where a.millsheetDate >= " + sql_date1 + " and a.millsheetDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"
		else: #外库接收时间    #########  搞清楚 外库接收 与 派车履运 的关系，他们是互斥关系，现在需要重新导loadno表，以使得此时间可以得出结果
			#外库接收时间、总销量
			#sql_wgt = "select c.tradeNo,sum(a.receiveWgt) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate >= " + sql_date1 + " and a.updateDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"
			sql_wgt = "select a.tradeNo,sum(a.receiveWeight) from data_sales_new_receiveno a where a.receiveDate >= " + sql_date1 + " and a.receiveDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"
			#外库接收时间、总销售额
			#sql_amt = "select c.tradeNo,sum(a.receiveWgt * c.unitPrice) from data_import_sales_receiveno a,data_import_sales_custplace b,data_import_sales_loadno c where a.updateDate >= " + sql_date1 + " and a.updateDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space + "' and c.custNo = b.custNo and a.loadNo = c.loadNo group by c.tradeNo"
			sql_amt = "select a.tradeNo,sum(a.receiveWeight * a.dispPrice) from data_sales_new_receiveno a where a.receiveDate >= " + sql_date1 + " and a.receiveDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space + "' group by a.tradeNo"

		#总退货率、质量问题个数   不分时间
		#sql_rtn = "select a.tradeNo,sum(a.rtnWgt) from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space +  "'  and a.custNo = b.custNo  group by a.tradeNo"
		sql_rtn = "select a.tradeNo,sum(a.rtnWeight) from data_sales_new_rtnno a where a.rtnDate >= " + sql_date1 + " and a.rtnDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space +  "' group by a.tradeNo"
		#sql_rtn_reason = "select a.rtnNo,a.orderNo,a.custNo,a.tradeNo,a.rtnWgt,a.unitPrice,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space +  "'  and a.custNo = b.custNo"
		sql_rtn_reason = "select a.rtnNo,a.orderNo,a.custNo,a.tradeNo,a.rtnWeight,a.rtnPrice,a.rtnReason from data_sales_new_rtnno  a where a.rtnDate >= " + sql_date1 + " and a.rtnDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space +  "' "
		#sql_rtn_reason_count = "select a.tradeNo,a.orderNo,a.orderItem,a.rtnReason from data_import_sales_rtnno a,data_import_sales_custplace b where a.createDate >= " + sql_date1 + " and a.createDate <= " + sql_date2 + " and b." + sql_ctry_prov_cty + " = '" + sql_space +  "'  and a.custNo = b.custNo group by a.orderNo,a.orderItem,a.rtnReason"
		sql_rtn_reason_count = "select a.tradeNo,a.orderNo,a.orderItem,a.rtnReason from data_sales_new_rtnno a where a.rtnDate >= " + sql_date1 + " and a.rtnDate <= " + sql_date2 + " and a." + sql_ctry_prov_cty + " = '" + sql_space +  "'   group by a.orderNo,a.orderItem,a.rtnReason"

		#=====================【 求 和 存 入 字 典 】==================================

		if aspect == 1 :
			tradeNo_wgt_list = conn_mysql.select(sql_wgt)
			print (type(tradeNo_wgt_list))
			weight_sum = 0
			for tradeNo in tradeNo_list:  #所选钢种
				for tradeNo_wgt in tradeNo_wgt_list:
					if tradeNo_wgt[0] == tradeNo: #如果订单中有这个钢种
						print(weight_sum,"\n",tradeNo_wgt[1],"\n")
						weight_sum += tradeNo_wgt[1] #重量求和
					else:
						pass
			print ("总销量：\t",sql_space,weight_sum)
			#print ("\n")

			space_dict[sql_space] = weight_sum
		elif aspect == 2:
			tradeNo_amt_list = conn_mysql.select(sql_amt)
			amount_sum = 0
			for tradeNo in tradeNo_list:  #所选钢种
				for tradeNo_amt in tradeNo_amt_list:
					if tradeNo_amt[0] == tradeNo: #如果订单中有这个钢种
						amount_sum += tradeNo_amt[1] #重量求和
					else:
						pass
			print ("总销售额：\t",sql_space,amount_sum)
			#print ("\n")
			space_dict[sql_space] = amount_sum
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
				print ("总退货率： %s%.5f" % (sql_space,rtn_rate),"%")
			else:
				print ("总退货率：",sql_space,"总销量为0，无法计算退货率！")
				rtn_rate = "总销量为0，无法计算退货率！"
				#rtn_rate = -2
			#tradeNo_rtn_rsn_list = conn_mysql.select(sql_rtn_reason)
			#print ("退货原因：\t",tradeNo_rtn_rsn_list)
			#print ("\n")
			space_dict[sql_space] = rtn_rate
		else:
			count = 0
			tradeNo_rtn_reason_count_list = conn_mysql.select(sql_rtn_reason_count)
			for tradeNo in tradeNo_list:
				for tradeNo_rtn_count_reason in tradeNo_rtn_reason_count_list:
					if tradeNo == tradeNo_rtn_count_reason[0]:
						count = count + 1
			print ("质量问题个数：",sql_space,count)
			space_dict[sql_space] = count


		if aspect == 3 or aspect == 4:
			tradeNo_rtn_reason_list = conn_mysql.select(sql_rtn_reason)
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
	return space_dict,passOrNot,tradeNo_rtn_reason_print
	#return sql_wgt,sql_amt,sql_rtn,sql_rtn_reason,sql_rtn_reason_count
