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

from . import input_
from . import sql_space
from . import sql_time
from . import sql_trade
from . import sql_customer
from . import sql_customer2
from . import max_min_average
from . import conclusion
from . import save_txt
import math
from functools import reduce
from data_import import models
conn_mysql = models.BaseManage()


def sql_market_share(startYear,startMonth,endYear,endMonth):
    #========================【 输 入 】===========================
    #获取数据
    #print ("开始执行 market_share_sql 函数")
    startDate = str(startYear) + str(startMonth) + "00"
    endDate = str(endYear) + str(endMonth) + "40"
    sql_province = "select a.province,sum(a.salesWeight),sum(a.qdisSalesWeight),(sum(a.qdisSalesWeight)/sum(a.salesWeight))*100 from data_sales_new_space_comparsion a where a.orderDate >= " + startDate + " and a.year <= " + endDate + " group by a.province"
    province_salesWeight_list = conn_mysql.select(sql_province) #得到的是一个tuple
    #print (type(province_salesWeight_list))
    print (province_salesWeight_list)

    ratio_dictionary = {}
    salesWeight_dictionary = {}
    qdisSalesWeight_dictionary = {}
    all_list = []
    conclusion_province = ""
    conclusion = startYear + "年" + startMonth + "月至" + endYear + "年" + endMonth + "月内，全国各省份市场容量及占比如下：\n"
    for province_salesWeight in province_salesWeight_list:  #所选钢种
        if province_salesWeight[0] == "":
            continue
        if province_salesWeight[3] == None:
            salesWeight_3 = 0
        else:
            salesWeight_3  = province_salesWeight[3]
        if province_salesWeight[2] == None:
            salesWeight_2 = 0
        else:
            salesWeight_2  = province_salesWeight[2]
        if province_salesWeight[1] == None:
            salesWeight_1 = 0
        else:
            salesWeight_1  = province_salesWeight[1]
        ratio_dictionary[province_salesWeight[0]] = float(salesWeight_3)
        salesWeight_dictionary[province_salesWeight[0]] = float(salesWeight_1)
        qdisSalesWeight_dictionary[province_salesWeight[0]] = float(salesWeight_2)
        all_list.append([province_salesWeight[0],float(salesWeight_1),float(salesWeight_2),float(salesWeight_3)])
        conclusion_province = province_salesWeight[0] + " 的市场容量为：" + str(salesWeight_1) + "吨，我公司在该地区销量为：" + str(salesWeight_2) + "吨,占比：" + str(salesWeight_3) + " %。\n"
        conclusion = conclusion + conclusion_province
    print ("比例字典：\n",ratio_dictionary)
    print ("\n")
    print ("市场容量字典：\n",salesWeight_dictionary)
    print ("\n")
    print ("青钢销量字典：\n",qdisSalesWeight_dictionary)
    print ("\n")
    print ("全部信息列表：\n",all_list)
    print ("\n")

    all_dictionary = {'全部信息list': all_list,'比例字典': ratio_dictionary,'市场容量字典': salesWeight_dictionary,'青钢销量字典': qdisSalesWeight_dictionary}
    print (all_dictionary)
    print ("\n")
    print ("结论：\n",conclusion)
    print ("\n")

    return ratio_dictionary,conclusion,all_dictionary





if __name__ == '__market_share_sql__':

    ratio_dictionary,conclusion,all_dictionary = sql_market_share(startYear,startMonth,endYear,endMonth)
    #print("market_share_sql.py 执行完毕")
    #print (module,tradeNo)
