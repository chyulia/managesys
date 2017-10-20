
# coding: utf-8

#!/usr/bin/python


#爬取之后的数据进行处理，把几张表合成一张
from data_import import models

import numpy as np
import pandas as pd


class ri_to_yue():
    def __init__(self):
        self.sql_conn = models.BaseManage()
        self.listed = list()

    def BDI(self):
        list_a = []
        list_price = []

        sql='truncate table yue_haiyun'
        date = self.sql_conn.execute(sql)
        sql='SELECT haiyun_date FROM haiyun'
        date = self.sql_conn.select(sql)
        # print(date)
        for each_day in date:
            ri = str(each_day[0])
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            list_a.append(yue)
        
        # print(list_a)
        sql='SELECT * FROM haiyun'
        data_1 = self.sql_conn.select(sql)
        data_1= list(data_1)
        se = list(set(list_a))
        se = sorted(se)

        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
                ri = str(each_day[1])
                each_ri = ri[0:7]
                if each_day[2] != '-':              
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)

        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price

        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            # print(i,j)
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_haiyun(haiyun_date,haiyun_BDI) values(%s,%s)'
            self.sql_conn.execute_params(sql,list_m)
            list_m.clear()


    def CRU(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []

        sql='truncate table yue_CRU'
        date = self.sql_conn.execute(sql)

        sql='SELECT CRU_date FROM CRU'
        date = sql_conn.select(sql)

        for each_day in date:
            ri = str(each_day[0])
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            list_a.append(yue)
            
        sql='SELECT * FROM CRU'
        data_1 = sql_conn.select(sql)

        data_1=list(data_1)

        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a

        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
        #         print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':
                
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
                    #     sum1 = sum1/k
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            # date_init = date_init[0:4] + date_init[5:7]
            se[i] = date_init

        tkszs_date = se
        tkszs_qdg = list_price
        list_n = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            print(i,j)
            list_n.append(i)
            list_n.append(j)
            sql='insert into yue_CRU(CRU_date,CRU_BDI) values(%s,%s)'
            sql_conn.execute_params(sql,list_n)
            list_n.clear()

    def PMI(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_PMI'
        date = self.sql_conn.execute(sql)
        sql='SELECT PMI_date FROM PMI'
        date = sql_conn.select(sql)
        for each_day in date:
            ri = str(each_day[0])
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            list_a.append(yue)
        sql='SELECT * FROM PMI'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
                ri = str(each_day[1])
                each_ri = ri[0:7]
                if each_day[2] != '-':        
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_PMI(PMI_date,PMI_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def PPI(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_PPI'
        date = self.sql_conn.execute(sql)
        sql='SELECT PPI_date FROM PPI'
        date = sql_conn.select(sql)

        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            # print(yue)
            list_a.append(yue)
        sql='SELECT * FROM PPI'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
                # print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':
                
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
                    #     sum1 = sum1/k
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            # date_init = date_init[0:4] + date_init[5:7]
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_PPI(PPI_date,PPI_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def WTI(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_WTI'
        date = self.sql_conn.execute(sql)
        sql='SELECT WTI_date FROM WTI'
        date = sql_conn.select(sql)
        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            # print(yue)
            list_a.append(yue)
        sql='SELECT * FROM WTI'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        type(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
        #         print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':               
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
                    #     sum1 = sum1/k
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_WTI(WTI_date,WTI_BDI) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def cugangyuedu(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_cugangyuedu'
        date = sql_conn.execute(sql)
        sql='SELECT cugangyuedu_date FROM cugangyuedu'
        date = sql_conn.select(sql)
        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            # print(yue)
            list_a.append(yue)
        sql='SELECT * FROM cugangyuedu'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        type(data_1)

        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
        #     print(each_yue)
            sum1 = 0
            k = 0
            for each_day in data_1:
                # print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':
                
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
                    #     sum1 = sum1/k
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            # print(i,j)
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_cugangyuedu(cugangyuedu_date,cugangyuedu_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def fdczs(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_fdczs'
        date = sql_conn.execute(sql)
        sql='SELECT fdczs_date FROM fdczs'
        date = sql_conn.select(sql)

        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            list_a.append(yue)
        sql='SELECT * FROM fdczs'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
        #     print(each_yue)
            sum1 = 0
            k = 0
            for each_day in data_1:
                # print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':
                
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
                    #     sum1 = sum1/k
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            # date_init = date_init[0:4] + date_init[5:7]
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            # print(i,j)
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_fdczs(fdczs_date,fdczs_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def gkkc(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_gkkc'
        date = sql_conn.execute(sql)
        sql='SELECT gkkc_date FROM gkkc'
        date = sql_conn.select(sql)
        for each_day in date:
            ri = str(each_day[0])
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            list_a.append(yue)
        sql='SELECT * FROM gkkc'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        type(data_1)

        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
        #     print(each_yue)
            sum1 = 0
            k = 0
            for each_day in data_1:
                # print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':              
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            # date_init = date_init[0:4] + date_init[5:7]
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        print(se,list_price)
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_gkkc(gkkc_date,gkkc_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def meiyuan(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_meiyuan'
        date = sql_conn.execute(sql)
        sql='SELECT meiyuan_date FROM meiyuan'
        date = sql_conn.select(sql)

        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            # print(yue)
            list_a.append(yue)
        sql='SELECT * FROM meiyuan'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
                ri = str(each_day[1])
                each_ri = ri[0:7]
                if each_day[2] != '-':
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
                    #     sum1 = sum1/k
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_meiyuan(meiyuan_date,meiyuan_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def tksjkl(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_tksjkl'
        date = sql_conn.execute(sql)
        sql='SELECT tksjkl_date FROM tksjkl'
        date = sql_conn.select(sql)
        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            # print(yue)
            list_a.append(yue)
        sql='SELECT * FROM tksjkl'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
        #     print(each_yue)
            sum1 = 0
            k = 0
            for each_day in data_1:
                # print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':
                
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
                    #     sum1 = sum1/k
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            # date_init = date_init[0:4] + date_init[5:7]
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_tksjkl(tksjkl_date,tksjkl_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def tksykcl(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table yue_tksykcl'
        date = sql_conn.execute(sql)
        sql='SELECT tksykcl_date FROM tksykcl'
        date = sql_conn.select(sql)
        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            # print(yue)
            list_a.append(yue)
        sql='SELECT * FROM tksykcl'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
                # print(each_day)
                ri = str(each_day[1])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[2] != '-':
                
                    each_price = float(each_day[2])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        print(se,list_price)
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into yue_tksykcl(tksykcl_date,tksykcl_zhi) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def tkszs_qdg(self):
        sql_conn = MySQL()
        list_a = []
        list_price = []
        sql='truncate table tkszs_qdg'
        date = sql_conn.execute(sql)
        sql='SELECT tkszs_date FROM tkszs'
        date = sql_conn.select(sql)
        for each_day in date:
            ri = str(each_day[0])
            # yue = ri[0:7]
            yue =  ri[0:4] + ri[5:7]
            yue = int(yue)
            # print(yue)
            list_a.append(yue)
        sql='SELECT * FROM tkszs'
        data_1 = sql_conn.select(sql)
        data_1=list(data_1)
        se = list(set(list_a))
        se = sorted(se)
        for i in range(len(se)):
            se[i]=str(se[i])
            a=se[i]
            a = a[0:4]+'-'+a[4:6]
            se[i] = a
        list_price = []
        for each_yue in se:
            sum1 = 0
            k = 0
            for each_day in data_1:
                # print(each_day)
                ri = str(each_day[0])
                each_ri = ri[0:7]
        #         print(each_ri)
                if each_day[4] != '-':
                
                    each_price = float(each_day[4])
                    if each_yue == each_ri:
                        k=k+1
                        sum1 = sum1 + each_price
            sum1 = sum1/k 
            sum1 = round(sum1,1)
            list_price.append(sum1)
        for i in range(len(se)):
            date_init = se[i]
            date_init = str(date_init)
            # date_init = date_init[0:4] + date_init[5:7]
            se[i] = date_init
        tkszs_date = se
        tkszs_qdg = list_price
        list_m = []
        for i,j in zip(tkszs_date,tkszs_qdg):
            list_m.append(i)
            list_m.append(j)
            sql='insert into tkszs_qdg(tkszs_date,tkszs_qdg) values(%s,%s)'
            sql_conn.execute_params(sql,list_m)
            list_m.clear()

    def integration(self):
        sql_conn = MySQL()

        sql='''UPDATE tkszs_qdg,yue_cugangyuedu
        SET tkszs_qdg.cugangyuedu = yue_cugangyuedu.cugangyuedu_zhi
        WHERE tkszs_qdg.tkszs_date = yue_cugangyuedu.cugangyuedu_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_haiyun
        SET tkszs_qdg.BDI = yue_haiyun.haiyun_BDI
        WHERE tkszs_qdg.tkszs_date = yue_haiyun.haiyun_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_meiyuan
        SET tkszs_qdg.meiyuan = yue_meiyuan.meiyuan_zhi
        WHERE tkszs_qdg.tkszs_date = yue_meiyuan.meiyuan_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_tksjkl
        SET tkszs_qdg.tksjkl = yue_tksjkl.tksjkl_zhi
        WHERE tkszs_qdg.tkszs_date = yue_tksjkl.tksjkl_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_tksykcl
        SET tkszs_qdg.tksykcl = yue_tksykcl.tksykcl_zhi
        WHERE tkszs_qdg.tkszs_date = yue_tksykcl.tksykcl_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_WTI
        SET tkszs_qdg.WTI = yue_WTI.WTI_BDI
        WHERE tkszs_qdg.tkszs_date = yue_WTI.WTI_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_PPI
        SET tkszs_qdg.PPI = yue_PPI.PPI_zhi
        WHERE tkszs_qdg.tkszs_date = yue_PPI.PPI_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_PMI
        SET tkszs_qdg.PMI = yue_PMI.PMI_zhi
        WHERE tkszs_qdg.tkszs_date = yue_PMI.PMI_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_fdczs
        SET tkszs_qdg.fdczs = yue_fdczs.fdczs_zhi
        WHERE tkszs_qdg.tkszs_date = yue_fdczs.fdczs_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_CRU
        SET tkszs_qdg.CRU = yue_CRU.CRU_BDI
        WHERE tkszs_qdg.tkszs_date = yue_CRU.CRU_date;
        '''
        sql_conn.execute(sql)

        sql='''UPDATE tkszs_qdg,yue_gkkc
        SET tkszs_qdg.gkkc = yue_gkkc.gkkc_zhi
        WHERE tkszs_qdg.tkszs_date = yue_gkkc.gkkc_date;
        '''
        sql_conn.execute(sql)





# if __name__ == '__main__':
#     ri_yue = ri_to_yue()
#     ri_yue.BDI()
#     ri_yue.CRU()
#     ri_yue.PMI()
#     ri_yue.PPI()
#     ri_yue.WTI()
#     ri_yue.cugangyuedu()
#     ri_yue.fdczs()
#     ri_yue.gkkc()
#     ri_yue.meiyuan()
#     ri_yue.tksjkl()
#     ri_yue.tksykcl()
#     ri_yue.tkszs_qdg()
#     ri_yue.integration()
#     print(OK!!!)




