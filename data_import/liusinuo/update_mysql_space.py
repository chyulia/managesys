'''

2016-10-21

对应 space.py 代码

控制 空间分析 的 sql 语句

'''
from data_import import models
conn_mysql = models.BaseManage()
from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine

#=====================【 SQL 语 句 查 询 】==================================
'''
时间：订单？发货？派车（出货销账）？派车（结算）？装车？存货？质保书？外库接收？
地点：世界（国家）？国（省）？省（市）？
内容：销量？销售额？退货？主要质量问题？

时间 地点 钢种 销量

'''
def tuple_to_dataframe (theTuple):
	theList = []
	# theBigList = list(theTuple)
	# for item in theBigList:  #遍历 tuple
	# 	theList.append(list(item))
	for i in range(len(theTuple)) :  #遍历 tuple
		theList.append(list(theTuple[i]))  #将 tuple 里面的 tuple 转化为 list
	print ("将查询得到的 tuple 转化为 list")
	theDataFrame = DataFrame(theList)
	print ("将 list 转化为 dataframe")
	return theDataFrame

def dataFrame_rename_space_orderNo (theDataFrame):
	theDataFrame.rename(columns = { 0: "tradeNo", 1: "orderWeight", 2: "orderPrice", 3: "orderDate",
		4: "province", 5: "country", 6: "city", 7: "custNo", 8: "orderNo", 9: "orderItem", 10: "crcy", 11: "taxType",
		12: "taxRate", 13: "orderAmount", 14: "compNo", 15: "status", 16: "transWayNo", 17: "salesType", 18: "salesMan",
		19: "salesDept", 20: "salesGroup", 21: "fwEdit", 22: "isGathered", 23: "updateEmpNoOrderNo", 24: "updateDateOrderNo",
		25: "updateTimeOrderNo", 26: "createEmpNoOrderNo", 27: "createDateOrderNo", 28: "createTimeOrderNo", 29: "compId",
		30: "orderVer", 31: "orderitemStatus", 32: "lineupStatus", 33: "contractTypeA", 34: "contractTypeB", 35: "contractTypeC",
		36: "prodClass", 37: "prodDetailClass", 38: "prodType", 39: "prodKind", 40: "psrNo", 41: "apnNo", 42: "standName",
		43: "mscNo", 44: "quality", 45: "priority", 46: "netWeightShipYN", 47: "countWgtMode", 48: "downPaymentYN", 49: "orderQty",
		50: "specialPriceFlag", 51: "basePrice", 52: "freightPrice", 53: "downPaymentRatio", 54: "downPayment", 55: "shipReqDateA",
		56: "shipReqDateB", 57: "slabType", 58: "cutType", 59: "orderDiameter", 60: "orderDiameterUnit", 61: "orderThick",
		62: "orderThickUnit", 63: "orderWidth", 64: "orderWidthUnit", 65: "orderLength", 66: "orderLengthUnit", 67: "orderDiameterMin",
		68: "orderDiameterMax", 69: "orderThickMin", 70: "orderThickMax", 71: "orderWidthMax", 72: "orderWidthMin", 73: "orderLengthMax",
		74: "orderLengthMin", 75: "shipTolMax", 76: "shipTolMin", 77: "minCoilWeight", 78: "maxCoilWeight", 79: "packCode",
		80: "minShortLength", 81: "maxShortLength", 82: "bundleType", 83: "specialReqCodeL", 84: "ultrasonicYN", 85: "eddyCurrentYN",
		86: "specMark", 87: "closeReason", 88: "closeEmpNo", 89: "closeDate", 90: "closeTime", 91: "unCloseEmpNo", 92: "unCloseDate",
		93: "unCloseTime", 94: "smEdit", 95: "enlace", 96: "deleteReason", 97: "deleteEmpNo", 98: "deleteDate", 99: "deleteTime",
		100: "dispWeight", 101: "dispQty", 102: "deliWeight", 103: "deliQty", 104: "chgWeight", 105: "chgQty", 106: "chgDeliWeight",
		107: "chgDeliQty", 108: "packWire", 109: "ironWire", 110: "pcsOfBdl", 111: "multipleLength", 112: "packMaterialWeight",
		113: "reWeigh", 114: "memo", 115: "updateEmpNoCustplace", 116: "updateDateCustplace", 117: "updateTimeCustplace",
		118: "createEmpNoCustplace", 119: "createDateCustplace", 120: "createTimeCustplace", 121: "confirmEmpNoOrderitem",
		122: "confirmDateOrderitem", 123: "confirmTimeOrderitem", 124: "cancelEmpNoOrderitem", 125: "cancelDateOrderitem",
		126: "cancelTimeOrderitem", 127: "createEmpNoOrderitem", 128: "createDateOrderitem", 129: "createTimeOrderitem",
		130: "updateEmpNoOrderitem", 131: "updateDateOrderitem", 132: "updateTimeOrderitem", 133: "orderItemNo", 134: "updateDate101",
		135: "updateTime101", 136: "updateEmpL101", 137: "updateDept101", 138: "lineUpCause", 139: "procRange", 140: "failureDate",
		141: "failureTime", 142: "sizeDesc", }, inplace=True)
	print ("修改 DataFrame 列名")
	return theDataFrame


def update_mysql_space_orderNo():
	print("更新数据仓库 data_new_sales_space.py 开始执行\n")

	#查询数据仓库表中的数据
	print("查询旧数据仓库表：")
	sql_data_ori = "select tradeNo, orderWeight, orderPrice, orderDate,province, country, city, custNo, orderNo, orderItem, crcy, taxType, taxRate, orderAmount, compNo, status, transWayNo, salesType, salesMan, salesDept, salesGroup, fwEdit, isGathered, updateEmpNoOrderNo, updateDateOrderNo, updateTimeOrderNo, createEmpNoOrderNo, createDateOrderNo, createTimeOrderNo, compId, orderVer, orderitemStatus, lineupStatus, contractTypeA, contractTypeB, contractTypeC, prodClass, prodDetailClass, prodType, prodKind, psrNo, apnNo, standName, mscNo, quality, priority, netWeightShipYN, countWgtMode, downPaymentYN, orderQty, specialPriceFlag, basePrice, freightPrice, downPaymentRatio, downPayment, shipReqDateA, shipReqDateB, slabType, cutType, orderDiameter, orderDiameterUnit, orderThick, orderThickUnit, orderWidth, orderWidthUnit, orderLength, orderLengthUnit, orderDiameterMin, orderDiameterMax, orderThickMin, orderThickMax, orderWidthMax, orderWidthMin, orderLengthMax, orderLengthMin, shipTolMax, shipTolMin, minCoilWeight, maxCoilWeight, packCode, minShortLength, maxShortLength, bundleType, specialReqCodeL, ultrasonicYN, eddyCurrentYN, specMark, closeReason, closeEmpNo, closeDate, closeTime, unCloseEmpNo, unCloseDate, unCloseTime, smEdit, enlace, deleteReason, deleteEmpNo, deleteDate, deleteTime, dispWeight, dispQty, deliWeight, deliQty, chgWeight, chgQty, chgDeliWeight, chgDeliQty, packWire, ironWire, pcsOfBdl, multipleLength, packMaterialWeight, reWeigh, memo, updateEmpNoCustplace, updateDateCustplace, updateTimeCustplace, createEmpNoCustplace, createDateCustplace, createTimeCustplace, confirmEmpNoOrderitem, confirmDateOrderitem, confirmTimeOrderitem, cancelEmpNoOrderitem, cancelDateOrderitem, cancelTimeOrderitem, createEmpNoOrderitem, createDateOrderitem, createTimeOrderitem, updateEmpNoOrderitem, updateDateOrderitem, updateTimeOrderitem, orderItemNo, updateDate101, updateTime101, updateEmpL101, updateDept101,lineUpCause, procRange, failureDate, failureTime, sizeDesc from data_new_sales_space_orderno"
	data_ori = conn_mysql.select(sql_data_ori)
	# 把上面那个查询数据库得来的 tuple 转化为 list
	dataFrame_data_ori = tuple_to_dataframe (data_ori)
	#修改列名
	dataFrame_data_ori = dataFrame_rename_space_orderNo (dataFrame_data_ori)
	print("查询旧数据仓库表 完毕\n")

	#查询数据库得到数据仓库表 sales space orderNo
	print("联合查询得到新数据：")
	sql_select_space_orderNo = "select c.tradeNo, c.orderWeight, c.basePrice, a.orderDate, b.country, b.province, b.city, a.custNo, a.orderNo, c.orderItem, a.crcy, a.taxType, a.taxRate, a.orderAmount, a.compNo, a.status, a.transWayNo, a.salesType, a.salesMan, a.salesDept, a.salesGroup, a.fwEdit, a.isGathered, a.createEmpNo, a.createDate, a.createTime, a.updateEmpNo, a.updateDate, a.updateTime, c.compId, c.orderVer, c.status, c.lineupStatus, c.contractTypeA, c.contractTypeB, c.contractTypeC, c.prodClass, c.prodDetailClass, c.prodType, c.prodKind, c.psrNo, c.apnNo, c.standName, c.mscNo, c.quality, c.priority, c.netWeightShipYN, c.countWgtMode, c.downPaymentYN, c.orderQty, c.specialPriceFlag, c.basePrice, c.freightPrice, c.downPaymentRatio, c.downPayment, c.shipReqDateA, c.shipReqDateB, c.slabType, c.cutType, c.orderDiameter, c.orderDiameterUnit, c.orderThick, c.orderThickUnit, c.orderWidth, c.orderWidthUnit, c.orderLength, c.orderLengthUnit, c.orderDiameterMin, c.orderDiameterMax, c.orderThickMin, c.orderThickMax, c.orderWidthMax, c.orderWidthMin, c.orderLengthMax, c.orderLengthMin, c.shipTolMax, c.shipTolMin, c.minCoilWeight, c.maxCoilWeight, c.packCode, c.minShortLength, c.maxShortLength, c.bundleType, c.specialReqCodeL, c.ultrasonicYN, c.eddyCurrentYN, c.specMark, c.closeReason, c.closeEmpNo, c.closeDate, c.closeTime, c.unCloseEmpNo, c.unCloseDate, c.unCloseTime, c.smEdit, c.enlace, c.deleteReason, c.deleteEmpNo, c.deleteDate, c.deleteTime, c.dispWeight, c.dispQty, c.deliWeight, c.deliQty, c.chgWeight, c.chgQty, c.chgDeliWeight, c.chgDeliQty, c.packWire, c.ironWire, c.pcsOfBdl, c.multipleLength, c.packMaterialWeight, c.reWeigh, c.memo, c.confirmEmpNo, c.confirmDate, c.confirmTime, c.cancelEmpNo, c.cancelDate, c.cancelTime, c.createEmpNo, c.createDate, c.createTime, c.updateEmpNo, c.updateDate, c.updateTime, c.orderItemNo, c.updateDate101, c.updateTime101, c.updateEmpL101, c.updateDept101, c.lineUpCause, c.procRange, c.failureDate, c.failureTime, c.sizeDesc from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.custNo = b.custNo and c.orderNo = a.orderNo"
	#sql_select_space_orderNo = "select c.tradeNo, c.orderWeight from data_import_sales_orderno a,data_import_sales_custplace b,data_import_sales2_orderno_orderitem c where a.custNo = b.custNo and c.orderNo = a.orderNo"
	data_space_orderNo = conn_mysql.select(sql_select_space_orderNo)
	# 把上面那个查询数据库得来的 tuple 转化为 list
	dataFrame_data_space_orderNo = tuple_to_dataframe (data_space_orderNo)
	#修改列名
	dataFrame_data_space_orderNo = dataFrame_rename_space_orderNo (dataFrame_data_space_orderNo)
	print("联合查询得到新数据 完毕\n")

	# #去除新数种与旧数据重复的部分
	# frames=[df1,df2,df3]
	# result=pd.concat(frames)

	#将两个 dataframe 的主键的列提取出来
	orderNo_list_ori = list(dataFrame_data_ori.orderNo)
	#print (orderNo_list_ori)
	orderItem_list_ori = list(dataFrame_data_ori.orderItem)
	#dataFrame_data_ori.loc[i,orderItem]
	orderNo_orderItem_list_ori = []
	for i,item in enumerate(orderNo_list_ori):
		orderNo_orderItem_list_ori.append(str(item) + str(orderItem_list_ori[i]))
	#print (orderNo_orderItem_list_ori)
	print(len(orderNo_orderItem_list_ori))
	print("旧数据仓库拼接  完毕\n")

	orderNo_list_new = list(dataFrame_data_space_orderNo.orderNo)
	orderItem_list_new = list(dataFrame_data_space_orderNo.orderItem)
	orderNo_orderItem_list_new = []
	for i,item in enumerate(orderNo_list_new):
		orderNo_orderItem_list_new.append(str(item) + str(orderItem_list_new[i]))
	print(len(orderNo_orderItem_list_new))
	print("新数据仓库拼接  完毕\n")

	index_list = list(range(0, len(orderNo_orderItem_list_new)))
	remove_list = []
	for j,jtems in enumerate(orderNo_orderItem_list_ori):
		for i,items  in enumerate(orderNo_orderItem_list_new):
			if items == jtems :
				#orderNo_orderItem_list_new.remove(orderNo_orderItem_list_new[i])
				#orderNo_list_new.remove(orderNo_list_new[i])
				#orderItem_list_new.remove(orderItem_list_new[i])
				remove_list.append(i)
				index_list.remove(i)
	print ("选中：",len(index_list))
	print ("删除：",len(remove_list))
	print ("清理重复索引  完毕\n")


	columns_list = ["tradeNo", "orderWeight", "orderPrice", "orderDate", "province", "country", "city", "custNo", 	"orderNo", "orderItem", "crcy", "taxType", "taxRate", "orderAmount", "compNo", "status","transWayNo", "salesType", "salesMan", "salesDept", "salesGroup", "fwEdit", "isGathered", "updateEmpNoOrderNo", "updateDateOrderNo", "updateTimeOrderNo", "createEmpNoOrderNo", "createDateOrderNo", "createTimeOrderNo", "compId", "orderVer", "orderitemStatus", "lineupStatus", "contractTypeA", "contractTypeB", "contractTypeC", "prodClass", "prodDetailClass", "prodType", "prodKind", "psrNo", "apnNo", "standName", "mscNo", "quality", "priority", "netWeightShipYN", "countWgtMode", "downPaymentYN", "orderQty", "specialPriceFlag", "basePrice", "freightPrice", "downPaymentRatio", "downPayment", "shipReqDateA", "shipReqDateB", "slabType", "cutType", "orderDiameter", "orderDiameterUnit", "orderThick", "orderThickUnit", "orderWidth", "orderWidthUnit", "orderLength", "orderLengthUnit", "orderDiameterMin", "orderDiameterMax", "orderThickMin", "orderThickMax", "orderWidthMax", "orderWidthMin", "orderLengthMax", "orderLengthMin", "shipTolMax", "shipTolMin", "minCoilWeight", "maxCoilWeight", "packCode", "minShortLength", "maxShortLength", "bundleType", "specialReqCodeL", "ultrasonicYN", "eddyCurrentYN", "specMark", "closeReason", "closeEmpNo", "closeDate", "closeTime", "unCloseEmpNo", "unCloseDate", "unCloseTime", "smEdit", "enlace", "deleteReason", "deleteEmpNo", "deleteDate", "deleteTime", "dispWeight", "dispQty", "deliWeight", "deliQty", "chgWeight", "chgQty", "chgDeliWeight", "chgDeliQty", "packWire", "ironWire", "pcsOfBdl", "multipleLength", "packMaterialWeight", "reWeigh", "memo", "updateEmpNoCustplace", "updateDateCustplace", "updateTimeCustplace", "createEmpNoCustplace", "createDateCustplace", "createTimeCustplace", "confirmEmpNoOrderitem", "confirmDateOrderitem", "confirmTimeOrderitem", "cancelEmpNoOrderitem", "cancelDateOrderitem", "cancelTimeOrderitem", "createEmpNoOrderitem", "createDateOrderitem", "createTimeOrderitem", "updateEmpNoOrderitem", "updateDateOrderitem", "updateTimeOrderitem", "orderItemNo", "updateDate101", "updateTime101", "updateEmpL101", "updateDept101", "lineUpCause", "procRange", "failureDate", "failureTime", "sizeDesc"]
	# 将不重复的筛选出来，成为新的 df
	dataframe_new = pd.DataFrame(dataFrame_data_space_orderNo,index = index_list,columns = columns_list)
	print ("不重复数据筛选  完毕\n")
	#print (dataframe_new)



	# 将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
	# 建立数据库连接
	yconnect = create_engine('mysql+mysqldb://root:123456@202.204.54.75:3306/qinggang?charset=utf8')
	print ("建立数据库连接")
	# 传入数据
	#pd.io.sql.to_sql(dataFrame_data_space_orderNo,'data_new_sales_space_orderno', yconnect, schema='qinggang', if_exists='append')
	dataframe_new.to_sql('data_new_sales_space_orderno', yconnect,  schema='qinggang', if_exists='append', index=False)
	print ("将数据写入数据表 ：data_new_sales_space_orderno")

	return

if __name__ == '__update_mysql_space__':

	update_mysql_space_orderNo()
