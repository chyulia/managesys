'''

2016-10-21

对应 v4_statistics.py 代码

将此大程序拆分成几个小程序

'''

#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
#======================================================================

#========== 1. 所 选 某 钢 种 占 全 部 钢 种 的 比 例 ============

#========== 2. 结 论 输 出 =======================================

#======================================================================
#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

#from sys import argv 
#script, filename = argv 

# from . import input_
# from . import sql_space
# from . import sql_time
# from . import sql_trade
# from . import sql_customer
# from . import sql_customer2
# from . import max_min_average
# from . import conclusion
# from . import save_txt
import math
from functools import reduce
# import data_import.models as models
from . import models
	
def sql_stockControl(module,tradeNo,module_unit_key):
	#========================【 输 入 】===========================
	print("开始执行stockControl.py文件中的函数\n\n")
	#按钢种查询数据库
	# select all stock
	sqlVO={}
	sqlVO["db_name"]="sale"
	sqlVO["sql"]="select TRADENO,sum(WEIGHT) from DB.TBID102 where ISINSTOCK = 'Y'  and STATUS <= '41' and INVID <= 'B11605026005EL014' GROUP BY TRADENO";
	#sqlVO["sql"]="select TRADENO,sum(WEIGHT) from DB.TBID102 where ISINSTOCK = 'Y'  and STATUS <= '41' GROUP BY TRADENO";
	stock_All=models.BaseManage().direct_select_query_sqlVO(sqlVO)

	# select stock before  20170401
	sqlVO={}
	sqlVO["db_name"]="sale"
	sqlVO["sql"] = "select TRADENO,sum(WEIGHT) from DB.TBID102 where ISINSTOCK = 'Y'  and STATUS <= '41' and INVID <= 'B11605026005EL014' and INSTOCKDATE < '20160201' GROUP BY TRADENO";
	#sqlVO["sql"] = "select TRADENO,sum(WEIGHT) from DB.TBID102 where ISINSTOCK = 'Y'  and STATUS <= '41' and INSTOCKDATE < '20170401' GROUP BY TRADENO";
	stock_overstock=models.BaseManage().direct_select_query_sqlVO(sqlVO)

	# print ("sql执行完毕")
	print ("stock_All\n",stock_All)
	# print (len(stock_All))
	# print ("\n")
	print ("stock_overstock\n",stock_overstock)
	# print (len(stock_overstock))
	# print ("\n")

	# this is the format of sql
	# [{'TRADENO': '50CrVA', 'SUM(WEIGHT)': 7950}, 
	# {'TRADENO': '50CrMnVA', 'SUM(WEIGHT)': 7767}, 
	# {'TRADENO': 'B7', 'SUM(WEIGHT)': 74863}, 
	# {'TRADENO': 'SCM435', 'SUM(WEIGHT)': 18981}]

	# [{'TRADENO': '50CrVA', 'SUM(WEIGHT)': 7950}, 
	# {'TRADENO': '50CrMnVA', 'SUM(WEIGHT)': 7767}, 
	# {'TRADENO': 'B7', 'SUM(WEIGHT)': 74863}, 
	# {'TRADENO': 'SCM435', 'SUM(WEIGHT)': 18981}]

	# initializaton
	tradeNolist = []
	sumWeight = []
	overWeight = []
	percentList = []

	# dict in tuple  ==>  list   (all stock)
	for items in stock_All:
		if items['SUM(WEIGHT)'] != 0:
			tradeNolist.append(items['TRADENO'])
			sumWeight.append(items['SUM(WEIGHT)'])
	#print(len(sumWeight))

	# dict in tuple  ==>  list   (stock before  20170401)
	i = 0
	for items in stock_overstock:
		#print(tradeNolist[i],items['TRADENO'],i)

		# if tradeNo is the same as tradeNoList , store
		if tradeNolist[i] == items['TRADENO']:
			overWeight.append(items['SUM(WEIGHT)'])
			itemPercent = (items['SUM(WEIGHT)'] / sumWeight[i]) * 100
			percentList.append(itemPercent)
			i = i + 1

		# if tradeNo are different 
		else:
			# if tradeNo are different ,then search the next one in tradeNoList ,determine whether they are the same
			while tradeNolist[i] != items['TRADENO']:
				#print(tradeNolist[i],items['TRADENO'])
				overWeight.append(0)
				percentList.append(0)
				# while they are different, store o
				# and then, if the index id is not exceed, i + 1
				if i < len(tradeNolist) - 1:
					i = i + 1
					#print("==============+++++++++++++",i)
				# else break the while loop
				else:
					break

			# if break the while loop, determine why it break
			# if the reason is "find out the same tradeNo", then do as follow
			# if not ,that must be "index out of range", then donnot execute the following quotation(the judgment quotation)
			if tradeNolist[i] == items['TRADENO']:
				#print(tradeNolist[i],items['TRADENO'],i)
				overWeight.append(items['SUM(WEIGHT)'])
				itemPercent = (items['SUM(WEIGHT)'] / sumWeight[i]) * 100
				percentList.append(itemPercent)
				i = i + 1
				#print("+++++++++++++++++++++======================",i)

	dictionary = {'tradeNo': tradeNolist,'stock_All': overWeight,'stock_overstock': overWeight,'percent': percentList}
	# print ('tradeNo',tradeNolist)
	# print ("\n")
	# print ('stock_All', overWeight)
	# print ("\n")
	# print ('stock_overstock', overWeight)
	# print ("\n")
	# print ('percent', percentList)
	# print ("\n")
	print (dictionary)
	conclusionPrint = "这是结论"
	module_name = "这是模块名称，第二个参数"
	#print ("222222222222")
	return dictionary,conclusionPrint,module_name





if __name__ == '__main__':
	print ("11111")
	dictionary,conclusionPrint,module_name = sql_stockControl(module,tradeNo,module_unit_key)
	print("stockControl.py文件中的函数执行完毕\n\n")
	#print (module,tradeNo)








