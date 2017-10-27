'''
更新BOF转炉数据

'''


import math
# from functools import reduce
# import data_import.models as models
from . import models

def updatebof(request):#全部数据重新执行
	batch_updatebof()


def batch_updatebof():
#========================【 输 入 】===========================
	print("开始执行updatebof")
	# 按钢种查询数据库
	# select all stock
	sqlVO={}
	sqlVO["db_name"]="l2query"
#表格单独处理----------------------------
	# --1.1.1.1.	炉次计划表（PRO_BOF_HIS_PLAN）
	# --删除重复项并选取时间最晚的记录
	sqlVO["sql"]='''create table pro_bof_his_plan_Result as
				select * from QG_USER.pro_bof_his_plan@dblink_to_l2 t1 where not exists
				(select * from QG_USER.pro_bof_his_plan@dblink_to_l2 t2 where heat_no = t1.heat_no
				and (t2.MSG_DATE > t1.MSG_DATE or (t2.MSG_DATE = t1.MSG_DATE and t2.rowid > t1.rowid)) )''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.2.	炉次兑铁信息表（PRO_BOF_HIS_MIRON）
	sqlVO["sql"]='''create table pro_bof_his_miron_Result as
	select * from QG_USER.pro_bof_his_miron@dblink_to_l2 t1 where not exists (select * from QG_USER.pro_bof_his_miron@dblink_to_l2 t2 where heat_no = t1.heat_no and (t2.MSG_DATE > t1.MSG_DATE or (t2.MSG_DATE = t1.MSG_DATE and t2.rowid > t1.rowid)) )''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.3.	炉次兑废钢信息表（PRO_BOF_HIS_SCRAP)
	# --步骤一：删除顺序号重复项
	sqlVO["sql"]='''create table pro_bof_his_scrap_result1 as
	select * from QG_USER.pro_bof_his_scrap@dblink_to_l2 t1 where not exists (select * from QG_USER.pro_bof_his_scrap@dblink_to_l2 t2 where t2.seq_no=t1.seq_no and t2.rowid>t1.rowid) ''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --步骤二：取最新值
	sqlVO["sql"]='''create table pro_bof_his_scrap_result2 as
	select * from pro_bof_his_scrap_result1 t1 where not exists (select * from pro_bof_his_scrap_result1 t2 where heat_no = t1.heat_no and t2.MSG_DATE > t1.MSG_DATE)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --行列转换（暂时不采取）
	# --sqlVO["sql"]='''create table pro_bof_his_scrap_result3 as
	# --select * from
	# --       (select HEAT_NO,SCRAP_NUM,SCRAP_CODE1,SCRAP_WGT1,SCRAP_CODE2,SCRAP_WGT2,SCRAP_CODE3,SCRAP_WGT3,SCRAP_CODE4,SCRAP_WGT4 from pro_bof_his_scrap_result2)
	# --pivot(
	# --      max(SCRAP_WGT1) for SCRAP_CODE1,max(SCRAP_WGT2) for SCRAP_CODE2 in (
	# --                '96053101' as scrap_96053101,
	# --                '96052200' as scrap_96052200,
	# --                '16010101' as scrap_16010101,
	# --                '16020101' as scrap_16020101,
	# --                '16030101' as scrap_16030101,
	# --                '16040101' as scrap_16040101,
	# --                '96052501' as scrap_96052501,
	# --)order by 1''';models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤三：直观表格转换
	sqlVO["sql"]='''create table pro_bof_his_scrap_result as
	select HEAT_NO,STATION,MSG_DATE,LDL_NO,SCRAP_NUM,SCRAP_WGT1 as scrap_96053101,SCRAP_WGT2 as scrap_96052200,SCRAP_WGT3 as scrap_16010101,SCRAP_WGT4 as scrap_16020101,SCRAP_WGT5 as scrap_16030101,SCRAP_WGT6 as scrap_16040101,SCRAP_WGT7 as scrap_96052501
	from pro_bof_his_scrap_result2''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --步骤四：删除中间过程表
	sqlVO["sql"]='''drop table pro_bof_his_scrap_result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''drop table pro_bof_his_scrap_result2''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)


	# --1.1.1.4.	炉次实绩表（PRO_BOF_HIS_POOL）
	sqlVO["sql"]='''create table pro_bof_his_pool_Result as
	select * from QG_USER.pro_bof_his_pool@dblink_to_l2 t1 where not exists (select * from QG_USER.pro_bof_his_pool@dblink_to_l2 t2 where heatno = t1.heatno and (t2.MSG_DATE > t1.MSG_DATE or (t2.MSG_DATE = t1.MSG_DATE and t2.rowid > t1.rowid)) )''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.5.	炉次事件表（PRO_BOF_HIS_EVENTS）
	# --步骤一：删除重复记录
	sqlVO["sql"]='''create table pro_bof_his_events_result1 as
	select * from QG_USER.pro_bof_his_events@dblink_to_l2 t1 where not exists (select * from QG_USER.pro_bof_his_events@dblink_to_l2 t2 where t2.seq_no=t1.seq_no and t2.rowid>t1.rowid) ''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤二：行列转换(由于在事件表中所有事件混合编号，所以很难判断该事件是第几次发送，因此对下列事件均只选取了最新的记录，即一次操作)
	# --3007测温时间节点在测温表中已处理，3009加料时间节点在加料表中已处理
	sqlVO["sql"]='''create table pro_bof_his_events_result as
	select * from
	       (select HEAT_NO,EVT_CODE,EVT_TIME from pro_bof_his_events_result1)
	pivot(
	       max(EVT_TIME) for (EVT_CODE) in (
	                        '3001' as Event_3001,
	                        '3002' as Event_3002,
	                        '3003' as Event_3003,
	                        '3004' as Event_3004,
	                        # --('1','3005') as E3005_1,('2','3005') as E3005_2,('3','3005') as E3005_3,# --吹氧开始，在吹氧记录表中已处理
	                        # --('1','3006') as E3006_1,('2','3006') as E3006_2,('3','3006') as E3006_3,# --吹氧结束，在吹氧记录表中已处理
	                        # --('1','3007') as E3007_1,('2','3007') as E3007_2,('3','3007') as E3007_3,('4','3007') as E3007_4# --测温时间，在测温表中已处理
	                        # --3008取样信息，在事件表中并未记录，在取样表中已做处理
	                        # --3009加料，在加料表中已处理
	                        '3010' as Event_3010,
	                        '3011' as Event_3011,
	                        '3012' as Event_3012,
	                        '3013' as Event_3013,
	                        '4003' as Event_4003,
	                        '4004' as Event_4004

	       )
	)order by 1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --步骤三：删除中间过程表
	sqlVO["sql"]='''drop table pro_bof_his_events_result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)


	# --1.1.1.6.	炉次吹氧记录表（PRO_BOF_HIS_BOCSM）
	# --步骤一：根据seq_no删除重复值
	sqlVO["sql"]='''create table PRO_BOF_HIS_BOCSM_RESULT1 as
	select * from QG_USER.PRO_BOF_HIS_BOCSM@DBLINK_TO_L2 t1 where not exists (select * from QG_USER.PRO_BOF_HIS_BOCSM@DBLINK_TO_L2 t2 where t2.seq_no=t1.seq_no and t2.rowid>t1.rowid) ''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤二：对吹氧量和吹氧时间进行加和
	sqlVO["sql"]='''create table PRO_BOF_HIS_BOCSM_RESULT2 as
	SELECT HEAT_NO,SUM(BO_CSM)as SUM_BO_CSM,SUM(BO_DUR)as SUM_BO_DUR FROM PRO_BOF_HIS_BOCSM_RESULT1 group by heat_no''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤三：其他字段的处理（吹氧开始时间。结束时间，吹氧时间等）（取6次）
	sqlVO["sql"]='''create table PRO_BOF_HIS_BOCSM_RESULT3 as
	select * from
	       (select HEAT_NO,STATION,BO_NO,BOSTRT_TIME,BOEND_TIME,BO_DUR,BO_CSM from PRO_BOF_HIS_BOCSM_RESULT1)
	pivot(
	       max(BOSTRT_TIME) as BOSTRT_TIME,max(BOEND_TIME) as BOEND_TIME,sum(BO_DUR)as BO_DUR,sum(BO_CSM)as BO_CSM for BO_NO in (
	                        '1' as d1,
	                        '2' as d2,
	                        '3' as d3,
	                        '4' as d4,
	                        '5' as d5,
	                        '6' as d6
	       )
	)order by 1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --步骤四：将时间和吹氧总量合并
	sqlVO["sql"]='''create table PRO_BOF_HIS_BOCSM_RESULT as
	Select t2.HEAT_NO,STATION,t2.SUM_BO_CSM,t2.SUM_BO_DUR,D1_BOSTRT_TIME,D1_BOEND_TIME,D1_BO_DUR,D1_BO_CSM,D2_BOSTRT_TIME,D2_BOEND_TIME,D2_BO_DUR,D2_BO_CSM,
	D3_BOSTRT_TIME,D3_BOEND_TIME,D3_BO_DUR,D3_BO_CSM,D4_BOSTRT_TIME,D4_BOEND_TIME,D4_BO_DUR,D4_BO_CSM,D5_BOSTRT_TIME,D5_BOEND_TIME,D5_BO_DUR,
	D5_BO_CSM,D6_BOSTRT_TIME,D6_BOEND_TIME,D6_BO_DUR,D6_BO_CSM
	from PRO_BOF_HIS_BOCSM_RESULT2 t2 JOIN PRO_BOF_HIS_BOCSM_RESULT3 t3 ON t2.heat_no=t3.heat_no''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --sqlVO["sql"]='''create table PRO_BOF_HIS_BOCSM_RESULT_test as
	# --select * from PRO_BOF_HIS_BOCSM_RESULT2 t2 JOIN PRO_BOF_HIS_BOCSM_RESULT3 t3 ON t2.heat_no=t3.heat_no
	# --步骤五：删除中间过程表（可不删）
	sqlVO["sql"]='''drop table PRO_BOF_HIS_BOCSM_Result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''drop table PRO_BOF_HIS_BOCSM_Result2''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''drop table PRO_BOF_HIS_BOCSM_Result3''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.7.	炉次测温表（PRO_BOF_HIS_TEMP）
	# --步骤一：根据seq_no删除重复值
	sqlVO["sql"]='''create table PRO_BOF_HIS_TEMP_Result1 as
	select * from QG_USER.PRO_BOF_HIS_TEMP@DBLINK_TO_L2 t1 where not exists (select * from QG_USER.PRO_BOF_HIS_TEMP@DBLINK_TO_L2 t2 where t2.seq_no=t1.seq_no and t2.rowid>t1.rowid) ''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤一：取最新值
	sqlVO["sql"]='''create table PRO_BOF_HIS_TEMP_Result2 as
	select * from PRO_BOF_HIS_TEMP_Result1 t1 where not exists (select * from PRO_BOF_HIS_TEMP_Result1 t2 where heat_no = t1.heat_no and (t2.TEMP_NO > t1.TEMP_NO or (t2.TEMP_NO = t1.TEMP_NO and t2.SEQ_NO > t1.SEQ_NO)) )''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤三：处理其他字段（每次测温时间等，取前四次测温）注：最新值并不一定是第四次测温值！！！
	sqlVO["sql"]='''create table PRO_BOF_HIS_TEMP_Result3 as
	select * from
	       (select HEAT_NO,TEMP_NO,TEMP_TIME,TEMP_VALUE,TEMP_TYPE,TEMP_ACQ from PRO_BOF_HIS_TEMP_Result1)
	pivot(
	       max(TEMP_TIME) as TEMP_TIME,max(TEMP_VALUE) as TEMP_VALUE,max(TEMP_TYPE)as TEMP_TYPE,max(TEMP_ACQ)as TEMP_ACQ for TEMP_NO in (
	                        '1' as d1,
	                        '2' as d2,
	                        '3' as d3,
	                        '4' as d4
	       )
	)order by 1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤四：将测温最新时间和前4次测温信息合并
	sqlVO["sql"]='''create table PRO_BOF_HIS_TEMP_Result as
	Select t2.HEAT_NO,t2.TEMP_NO as final_TEMP_NO,t2.TEMP_TIME as final_TEMP_TIME,t2.TEMP_VALUE as final_TEMP_VALUE,
	t2.TEMP_TYPE as final_TEMP_TYPE ,t2.TEMP_ACQ as final_TEMP_ACQ,
	D1_TEMP_TIME,D1_TEMP_VALUE,D1_TEMP_TYPE,D1_TEMP_ACQ,D2_TEMP_TIME,D2_TEMP_VALUE,D2_TEMP_TYPE,D2_TEMP_ACQ,D3_TEMP_TIME,
	D3_TEMP_VALUE,D3_TEMP_TYPE,D3_TEMP_ACQ,D4_TEMP_TIME,D4_TEMP_VALUE,D4_TEMP_TYPE,D4_TEMP_ACQ
	from PRO_BOF_HIS_TEMP_Result2 t2 JOIN PRO_BOF_HIS_TEMP_Result3 t3 ON t2.heat_no=t3.heat_no ''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤五：删除中间过程表（可不删）
	sqlVO["sql"]='''drop table PRO_BOF_HIS_TEMP_Result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''drop table PRO_BOF_HIS_TEMP_Result2''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''drop table PRO_BOF_HIS_TEMP_Result3''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)


	# --1.1.1.8.	炉次加料表A（PRO_BOF_HIS_CHRGDGEN）父表
	# --步骤一：根据seq_no删除重复值
	sqlVO["sql"]='''create table PRO_BOF_HIS_CHRGDGEN_Result1 as
	select * from QG_USER.PRO_BOF_HIS_CHRGDGEN@DBLINK_TO_L2 t1 where not exists (select * from QG_USER.PRO_BOF_HIS_CHRGDGEN@DBLINK_TO_L2 t2 where t2.seq_no=t1.seq_no and t2.rowid>t1.rowid) ''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤二：行列转换（各批次加料时间等）(取了前30批)
	sqlVO["sql"]='''create table PRO_BOF_HIS_CHRGDGEN_Result as
	select * from
	       (select HEAT_NO,STATION,CHRGD_BATCHNO,CHRGD_TIME,CHRGD_TYPE from PRO_BOF_HIS_CHRGDGEN_Result1)
	pivot(
	       max(CHRGD_TIME) as CHRGD_TIME,max(CHRGD_TYPE) as CHRGD_TYPE for CHRGD_BATCHNO in (
	                        '1' as d1,
	                        '2' as d2,
	                        '3' as d3,
	                        '4' as d4,
	                        '5' as d5,
	                        '6' as d6,
	                        '7' as d7,
	                        '8' as d8,
	                        '9' as d9,
	                        '10' as d10,
	                        '11' as d11,
	                        '12' as d12,
	                        '13' as d13,
	                        '14' as d14,
	                        '15' as d15,
	                        '16' as d16,
	                        '17' as d17,
	                        '18' as d18,
	                        '19' as d19,
	                        '20' as d20,
	                        '21' as d21,
	                        '22' as d22,
	                        '23' as d23,
	                        '24' as d24,
	                        '25' as d25,
	                        '26' as d26,
	                        '27' as d27,
	                        '28' as d28,
	                        '29' as d29,
	                        '30' as d30

	       )
	)order by 1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤三：删除中间过程表
	sqlVO["sql"]='''drop table PRO_BOF_HIS_CHRGDGEN_Result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)



	# --1.1.1.9.	炉次加料表B（PRO_BOF_HIS_CHRGDDAT）子表
	# --步骤一：根据seq_no删除重复值
	sqlVO["sql"]='''create table PRO_BOF_HIS_CHRGDDAT_Result1 as
	select * from QG_USER.PRO_BOF_HIS_CHRGDDAT@DBLINK_TO_L2 t1 where not exists (select * from QG_USER.PRO_BOF_HIS_CHRGDDAT@DBLINK_TO_L2 t2 where t2.seq_no=t1.seq_no and t2.rowid>t1.rowid) ''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤二：行列转换(物料代码及加和的物料重量)（加料表B表，即子表）
	sqlVO["sql"]='''create table PRO_BOF_HIS_CHRGDDAT_Result as
	select * from
	       (select HEAT_NO,STATION, MAT_CODE, MAT_WGT from PRO_BOF_HIS_CHRGDDAT_Result1)
	pivot(
	       sum(MAT_WGT) for MAT_CODE in (
	                '12010301' as L12010301,
	                '12010302' as L12010302,
	                '12010601' as L12010601,
	                '12010701' as L12010701,
	                '12020201' as L12020201,
	                '12020301' as L12020301,
	                '13010101' as L13010101,
	                '13010301' as L13010301,
	                '13020101' as L13020101,
	                '13020201' as L13020201,
	                '13020501' as L13020501,
	                '13040400' as L13040400,
	                '96020400' as L96020400,
	                '96040100' as L96040100,
	                '96040200' as L96040200,
	                '96053601' as L96053601,
	                '1602010074' as L1602010074
	       )
	)order by 1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --步骤三：删除中间过程表
	sqlVO["sql"]='''drop table PRO_BOF_HIS_CHRGDDAT_Result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.12.	取样信息记录（PRO_BOF_HIS_ANAGEN）
	# --步骤一：根据seq_no删除重复值
	sqlVO["sql"]='''create table PRO_BOF_HIS_ANAGEN_Result1 as
	select * from QG_USER.PRO_BOF_HIS_ANAGEN@DBLINK_TO_L2 t1 where not exists (select * from QG_USER.PRO_BOF_HIS_ANAGEN@DBLINK_TO_L2 t2 where t2.seq_no = t1.seq_no and t2.rowid > t1.rowid)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤二：取样信息记录表字段的处理（取样时间、取样类型等）（取前5次取样）一个炉次号可能对应多个站别，取消station
	sqlVO["sql"]='''create table PRO_BOF_HIS_ANAGEN_Result as
	select * from
	       (select HEAT_NO,SAMP_NO,SAMP_TIME,SAMP_TYPE from PRO_BOF_HIS_ANAGEN_Result1)
	pivot(
	       max(SAMP_TIME) as SAMP_TIME,max(SAMP_TYPE) as SAMP_TYPE for SAMP_NO in (
	                        '1' as d1,
	                        '2' as d2,
	                        '3' as d3,
	                        '4' as d4,
	                        '5' as d5
	       )
	)order by 1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤三：删除中间过程表格
	sqlVO["sql"]='''drop table PRO_BOF_HIS_ANAGEN_Result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)


	# --1.1.1.13.	成分信息记录（PRO_BOF_HIS_ANADAT）
	# # --步骤一：根据seq_no删除重复值
	# sqlVO["sql"]='''create table PRO_BOF_HIS_ANADAT_Result1 as
	# select * from QG_USER.PRO_BOF_HIS_ANADAT@DBLINK_TO_L2 t1 where not exists (select * from QG_USER.PRO_BOF_HIS_ANADAT@DBLINK_TO_L2 t2 where t2.seq_no=t1.seq_no and t2.rowid>t1.rowid) ''';
	# models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	
	# --步骤一：取样信息表中获取取样类型，添加到成分信息表中
	sqlVO["sql"]='''create table PRO_BOF_HIS_ANADAT_Result1 as
	select t2.*, t1.samp_type from PRO_BOF_HIS_ANAGEN t1 right join  PRO_BOF_HIS_ANADAT t2 on t1.samp_no = t2.samp_no and t1.heat_no =t2.heat_no''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤二：取最新成分数据(取样类型不能为3,3表示炉前数据)
	sqlVO["sql"]='''create table PRO_BOF_HIS_ANADAT_Result2 as
	select * from PRO_BOF_HIS_ANADAT_Result1 t1 where SAMP_TYPE !=3 AND not exists (select * from PRO_BOF_HIS_ANADAT_Result1 t2 where t2.heat_no = t1.heat_no and t2.ELMT_CODE=t1.ELMT_CODE and t2.SAMP_NO > t1.SAMP_NO )''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --步骤三：成分信息记录的行列转换（各成分参数）
	sqlVO["sql"]='''create table PRO_BOF_HIS_ANADAT_Result as# --删除了station字段，因为数据自身的问题，存在极个别情况出现一个炉次号对应多个站别的记录
	select * from
	       (select HEAT_NO,ELMT_CODE, ELMT_CONT from PRO_BOF_HIS_ANADAT_Result2)
	pivot(
	      max(ELMT_CONT) for ELMT_CODE in (
	                'C' as C,
	                'Si' as Si,
	                'Mn' as Mn,
	                'P' as P,
	                'S' as S,
	                'Al_T' as Al_T,
	                'Al_S' as Al_S,
	                'Ni' as Ni,
	                'Cr' as Cr,
	                'Cu' as Cu,
	                'Mo' as Mo,
	                'V' as V,
	                'Ti' as Ti,
	                'Nb' as Nb,
	                'W' as W,
	                'Pb' as Pb,
	                'Sn' as Sn,
	                'As' as "AS",
	                'Bi' as Bi,
	                'B' as B,
	                'Ca' as Ca,
	                'N' as N,
	                'Co' as Co,
	                'Zr' as Zr,
	                'Ce' as Ce,
	                'Fe' as Fe
	       )
	)order by 1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --步骤四：删除中间过程表格
	sqlVO["sql"]='''drop table PRO_BOF_HIS_ANADAT_Result1''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''drop table PRO_BOF_HIS_ANADAT_Result2''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)


#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#字段汇总-----------------------------------------
	# --删除表
	sqlVO["sql"]='''drop table IF EXISTS PRO_BOF_HIS_ALLFIELDS''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --新建空表
	sqlVO["sql"]='''create table PRO_BOF_HIS_ALLFIELDS (
	HEAT_NO VARCHAR2(20 BYTE) NULL ,
	STATION VARCHAR2(4 BYTE) NULL
	)
	ENABLE ROW MOVEMENT
	LOGGING
	NOCOMPRESS
	NOCACHE
	''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --添加字段
	# --1.1.1.1.	炉次计划表（PRO_BOF_HIS_PLAN）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	"MSG_DATE_PLAN" DATE NULL ,
	"WORK_SHOP_PLAN" VARCHAR2(1 BYTE) NULL ,
	"PLANT_DIFF" VARCHAR2(8 BYTE) NULL ,
	"HEAT_ORDER" VARCHAR2(20 BYTE) NULL ,
	"GE_NO" VARCHAR2(20 BYTE) NULL ,
	"GK_NO" VARCHAR2(20 BYTE) NULL ,
	"SPECIFICATION" VARCHAR2(20 BYTE) NULL ,
	"PROCESS_CODE1" VARCHAR2(2 BYTE) NULL ,
	"SAMPLE_CODE" VARCHAR2(4 BYTE) NULL ,
	"HEAT_WGT" NUMBER(6) NULL ,
	"PLAN_DATE" VARCHAR2(8 BYTE) NULL ,
	"HEAT_PATH" VARCHAR2(4 BYTE) NULL ,
	"CAST_NO" VARCHAR2(5 BYTE) NULL ,
	"CAST_SEQ" VARCHAR2(3 BYTE) NULL ,
	"PLAN_STATUS" VARCHAR2(1 BYTE) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.2.	炉次兑铁信息表（PRO_BOF_HIS_MIRON）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	"MSG_DATE_MIRON" DATE NULL ,
	"MIRON_NO_MIRON" VARCHAR2(20 BYTE) NULL ,
	"LDL_NO_MIRON" VARCHAR2(12 BYTE) NULL ,
	"MIRON_WGT" NUMBER(6) NULL ,
	"MIRON_TEMP" NUMBER(4) NULL ,
	"MIRON_C" NUMBER(7,4) NULL ,
	"MIRON_SI" NUMBER(7,4) NULL ,
	"MIRON_MN" NUMBER(7,4) NULL ,
	"MIRON_P" NUMBER(7,4) NULL ,
	"MIRON_S" NUMBER(7,4) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.3.	炉次兑废钢信息表（PRO_BOF_HIS_SCRAP)(暂时不做行列转换)
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	MSG_DATE_SCRAP DATE NULL ,
	LDL_NO_SCRAP VARCHAR2(12 BYTE) NULL ,
	SCRAP_NUM NUMBER(2) NULL ,
	scrap_96053101 NUMBER(6) NULL ,
	scrap_96052200 NUMBER(6) NULL ,
	scrap_16010101 NUMBER(6) NULL ,
	scrap_16020101 NUMBER(6) NULL ,
	scrap_16030101 NUMBER(6) NULL ,
	scrap_16040101 NUMBER(6) NULL ,
	scrap_96052501 NUMBER(6) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.4.	炉次实绩表（PRO_BOF_HIS_POOL）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	"MSG_DATE_POOL" DATE NULL ,
	"WORK_SHOP_POOL" VARCHAR2(1 BYTE) NULL ,
	"OPERATEDATE" VARCHAR2(8 BYTE) NULL ,
	"OPERATESHIFT" VARCHAR2(1 BYTE) NULL ,
	"OPERATECREW" VARCHAR2(1 BYTE) NULL ,
	"OPERATOR" VARCHAR2(10 BYTE) NULL ,
	"HEATORDER" VARCHAR2(20 BYTE) NULL ,
	"FURNACESEQ" NUMBER(5) NULL ,
	"SPRAYGUNLOC" VARCHAR2(1 BYTE) NULL ,
	"SPRAYGUNSEQ" NUMBER(5) NULL ,
	"GUNCHANGERES" VARCHAR2(200 BYTE) NULL ,
	"HOTMETALWGT" NUMBER(6) NULL ,
	"COLDPIGWGT" NUMBER(6) NULL ,
	"SCRAPWGT" NUMBER(6) NULL ,
	"SLAGWGT" NUMBER(6) NULL ,
	"RETURNSTEELWEIGHT" NUMBER(6) NULL ,
	"RETURNHEATNO" VARCHAR2(8 BYTE) NULL ,
	"RETURNMEMO" VARCHAR2(200 BYTE) NULL ,
	"DOWNFURNACETIMES" NUMBER(2) NULL ,
	"PUTSPRAYGUNTIME" VARCHAR2(6 BYTE) NULL ,
	"CARBONTEMPERATURE" NUMBER(6,2) NULL ,
	"FIRSTCATCHCARBONC" NUMBER(5,3) NULL ,
	"FIRSTCATCHCARBONP" NUMBER(5,3) NULL ,
	"SUBLANCE_AGE" NUMBER(3) NULL ,
	"SUBLANCE_INDEPTH" NUMBER(6,2) NULL ,
	"O_CONT" NUMBER(4) NULL ,
	"C_CONT" NUMBER(4) NULL ,
	"LEQHEIGH" NUMBER(6,3) NULL ,
	"STOVEHEATSNUM" NUMBER(3) NULL ,
	"PITPATCHINGKIND" VARCHAR2(2 BYTE) NULL ,
	"BOTTOMBLOWING" VARCHAR2(2 BYTE) NULL ,
	"FIRSTCATCHOXYGENCONSUME" NUMBER(6,2) NULL ,
	"TIMEOFOXYGEN" NUMBER(6) NULL ,
	"TOTALOXYGENCONSUME" NUMBER(6,2) NULL ,
	"TOTALTIMEOFOXYGEN" NUMBER(6) NULL ,
	"N2CONSUME" NUMBER(6,2) NULL ,
	"TIMEOFSLAGSPLISHING" NUMBER(6) NULL ,
	"BEFARTEMP" NUMBER(6,2) NULL ,
	"STEELWGT" NUMBER(6) NULL ,
	"PERIOD" NUMBER(7) NULL ,
	"IS_NO" VARCHAR2(20 BYTE) NULL ,
	"TLADLENO" VARCHAR2(12 BYTE) NULL ,
	"IS_TEMP" NUMBER(6,2) NULL ,
	"TAPPINGSTARTDATE" VARCHAR2(8 BYTE) NULL ,
	"TAPPINGSTARTTIME" VARCHAR2(8 BYTE) NULL ,
	"TAPPINGENDDATE" VARCHAR2(8 BYTE) NULL ,
	"TAPPINGENDTIME" VARCHAR2(8 BYTE) NULL ,
	"MEMO" VARCHAR2(200 BYTE) NULL ,
	"LADLENO" VARCHAR2(8 BYTE) NULL ,
	"LADLESTATUS" VARCHAR2(3 BYTE) NULL ,
	"LADLEAGE" VARCHAR2(3 BYTE) NULL ,
	"SLAGTHICK" NUMBER(3) NULL ,
	"SCRAPSTEEL" NUMBER(3) NULL ,
	"INSULATIONAGENT" NUMBER(2) NULL ,
	"OPERATETIME" NUMBER(4) NULL ,
	"ARRIVEDATE" VARCHAR2(8 BYTE) NULL ,
	"ARRIVETIME" VARCHAR2(6 BYTE) NULL ,
	"DEPARTUREDATE" VARCHAR2(8 BYTE) NULL ,
	"DEPARTURETIME" VARCHAR2(6 BYTE) NULL ,
	"TEMPOFARRIVE" NUMBER(6,2) NULL ,
	"TEMPOFDEPARTURE" NUMBER(6,2) NULL ,
	"OPERATORA" VARCHAR2(10 BYTE) NULL ,
	"OPERATORB" VARCHAR2(10 BYTE) NULL ,
	"OPERATORC" VARCHAR2(10 BYTE) NULL ,
	"OPERATORD" VARCHAR2(10 BYTE) NULL ,
	"OPERATORE" VARCHAR2(10 BYTE) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.5.	炉次事件表（PRO_BOF_HIS_EVENTS）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	Event_3001 DATE NULL,
	Event_3002 DATE NULL,
	Event_3003 DATE NULL,
	Event_3004 DATE NULL,
	Event_3010 DATE NULL,
	Event_3011 DATE NULL,
	Event_3012 DATE NULL,
	Event_3013 DATE NULL,
	Event_4003 DATE NULL,
	Event_4004 DATE NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)


	# --1.1.1.6.	炉次吹氧记录表（PRO_BOF_HIS_BOCSM）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	"SUM_BO_CSM" NUMBER(10,2) NULL ,
	"SUM_BO_DUR" NUMBER(10) NULL,
	"D1_BOSTRT_TIME" DATE NULL ,
	"D1_BOEND_TIME" DATE NULL ,
	"D1_BO_DUR" NUMBER(10) NULL ,
	"D1_BO_CSM" NUMBER(10,2) NULL ,
	"D2_BOSTRT_TIME" DATE NULL ,
	"D2_BOEND_TIME" DATE NULL ,
	"D2_BO_DUR" NUMBER(10) NULL ,
	"D2_BO_CSM" NUMBER(10,2) NULL ,
	"D3_BOSTRT_TIME" DATE NULL ,
	"D3_BOEND_TIME" DATE NULL ,
	"D3_BO_DUR" NUMBER(10) NULL ,
	"D3_BO_CSM" NUMBER(10,2) NULL ,
	"D4_BOSTRT_TIME" DATE NULL ,
	"D4_BOEND_TIME" DATE NULL ,
	"D4_BO_DUR" NUMBER(10) NULL ,
	"D4_BO_CSM" NUMBER(10,2) NULL ,
	"D5_BOSTRT_TIME" DATE NULL ,
	"D5_BOEND_TIME" DATE NULL ,
	"D5_BO_DUR" NUMBER(10) NULL ,
	"D5_BO_CSM" NUMBER(10,2) NULL ,
	"D6_BOSTRT_TIME" DATE NULL ,
	"D6_BOEND_TIME" DATE NULL ,
	"D6_BO_DUR" NUMBER(10) NULL ,
	"D6_BO_CSM" NUMBER(10,2) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.7.	炉次测温表（PRO_BOF_HIS_TEMP）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	final_TEMP_NO NUMBER(4) NULL ,
	final_TEMP_TIME DATE NULL ,
	final_TEMP_VALUE NUMBER(4) NULL ,
	final_TEMP_TYPE VARCHAR2(1 BYTE) NULL ,
	final_TEMP_ACQ VARCHAR2(1 BYTE) NULL ,
	D1_TEMP_TIME DATE NULL ,
	D1_TEMP_VALUE NUMBER(4) NULL ,
	D1_TEMP_TYPE VARCHAR2(1 BYTE) NULL ,
	D1_TEMP_ACQ VARCHAR2(1 BYTE) NULL ,
	D2_TEMP_TIME DATE NULL ,
	D2_TEMP_VALUE NUMBER(4) NULL ,
	D2_TEMP_TYPE VARCHAR2(1 BYTE) NULL ,
	D2_TEMP_ACQ VARCHAR2(1 BYTE) NULL ,
	D3_TEMP_TIME DATE NULL ,
	D3_TEMP_VALUE NUMBER(4) NULL ,
	D3_TEMP_TYPE VARCHAR2(1 BYTE) NULL ,
	D3_TEMP_ACQ VARCHAR2(1 BYTE) NULL ,
	D4_TEMP_TIME DATE NULL ,
	D4_TEMP_VALUE NUMBER(4) NULL ,
	D4_TEMP_TYPE VARCHAR2(1 BYTE) NULL ,
	D4_TEMP_ACQ VARCHAR2(1 BYTE) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.8.	炉次加料表A（PRO_BOF_HIS_CHRGDGEN）父表
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	 D1_CHRGD_TIME DATE NULL,D1_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D2_CHRGD_TIME DATE NULL,D2_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D3_CHRGD_TIME DATE NULL,D3_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D4_CHRGD_TIME DATE NULL,D4_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D5_CHRGD_TIME DATE NULL,D5_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D6_CHRGD_TIME DATE NULL,D6_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D7_CHRGD_TIME DATE NULL,D7_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D8_CHRGD_TIME DATE NULL,D8_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D9_CHRGD_TIME DATE NULL,D9_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D10_CHRGD_TIME DATE NULL,D10_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D11_CHRGD_TIME DATE NULL,D11_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D12_CHRGD_TIME DATE NULL,D12_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D13_CHRGD_TIME DATE NULL,D13_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D14_CHRGD_TIME DATE NULL,D14_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D15_CHRGD_TIME DATE NULL,D15_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D16_CHRGD_TIME DATE NULL,D16_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D17_CHRGD_TIME DATE NULL,D17_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D18_CHRGD_TIME DATE NULL,D18_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D19_CHRGD_TIME DATE NULL,D19_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D20_CHRGD_TIME DATE NULL,D20_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D21_CHRGD_TIME DATE NULL,D21_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D22_CHRGD_TIME DATE NULL,D22_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D23_CHRGD_TIME DATE NULL,D23_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D24_CHRGD_TIME DATE NULL,D24_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D25_CHRGD_TIME DATE NULL,D25_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D26_CHRGD_TIME DATE NULL,D26_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D27_CHRGD_TIME DATE NULL,D27_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D28_CHRGD_TIME DATE NULL,D28_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D29_CHRGD_TIME DATE NULL,D29_CHRGD_TYPE VARCHAR2(1 BYTE) NULL ,
	 D30_CHRGD_TIME DATE NULL,D30_CHRGD_TYPE VARCHAR2(1 BYTE) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.9.	炉次加料表B（PRO_BOF_HIS_CHRGDDAT）子表
	# --添加表格PRO_BOF_HIS_CHRGDDAT_Result的字段（炉次加料表B）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	L12010301 NUMBER(8,2) NULL,
	L12010302 NUMBER(8,2) NULL  ,
	L12010601 NUMBER(8,2) NULL  ,
	L12010701 NUMBER(8,2) NULL  ,
	L12020201 NUMBER(8,2) NULL  ,
	L12020301 NUMBER(8,2) NULL  ,
	L13010101 NUMBER(8,2) NULL  ,
	L13010301 NUMBER(8,2) NULL  ,
	L13020101 NUMBER(8,2) NULL  ,
	L13020201 NUMBER(8,2) NULL  ,
	L13020501 NUMBER(8,2) NULL  ,
	L13040400 NUMBER(8,2) NULL  ,
	L96020400 NUMBER(8,2) NULL  ,
	L96040100 NUMBER(8,2) NULL  ,
	L96040200 NUMBER(8,2) NULL  ,
	L96053601 NUMBER(8,2) NULL  ,
	L1602010074 NUMBER(8,2) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.10.	线上设备信息（PRO_BOF_HIS_EQPONLINE）(设备信息暂跳过)
	# --1.1.1.11.	设备维修记录表（PRO_BOF_HIS_EQPLOG）(设备信息暂跳过)

	# --1.1.1.12.	取样信息记录（PRO_BOF_HIS_ANAGEN）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	D1_SAMP_TIME DATE NULL,
	D1_SAMP_TYPE VARCHAR2(2 BYTE) NULL ,
	D2_SAMP_TIME DATE NULL,
	D2_SAMP_TYPE VARCHAR2(2 BYTE) NULL ,
	D3_SAMP_TIME DATE NULL,
	D3_SAMP_TYPE VARCHAR2(2 BYTE) NULL ,
	D4_SAMP_TIME DATE NULL,
	D4_SAMP_TYPE VARCHAR2(2 BYTE) NULL ,
	D5_SAMP_TIME DATE NULL,
	D5_SAMP_TYPE VARCHAR2(2 BYTE) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.13.	成分信息记录（PRO_BOF_HIS_ANADAT）
	sqlVO["sql"]='''alter table PRO_BOF_HIS_ALLFIELDS add(
	C NUMBER(7,4) NULL ,
	Si NUMBER(7,4) NULL ,
	Mn NUMBER(7,4) NULL ,
	P NUMBER(7,4) NULL ,
	S NUMBER(7,4) NULL ,
	Al_T NUMBER(7,4) NULL ,
	Al_S NUMBER(7,4) NULL ,
	Ni NUMBER(7,4) NULL ,
	Cr NUMBER(7,4) NULL ,
	Cu NUMBER(7,4) NULL ,
	Mo NUMBER(7,4) NULL ,
	V NUMBER(7,4) NULL ,
	Ti NUMBER(7,4) NULL ,
	Nb NUMBER(7,4) NULL ,
	W NUMBER(7,4) NULL ,
	Pb NUMBER(7,4) NULL ,
	Sn NUMBER(7,4) NULL ,
	"AS" NUMBER(7,4) NULL ,
	Bi NUMBER(7,4) NULL ,
	B NUMBER(7,4) NULL ,
	Ca NUMBER(7,4) NULL ,
	N NUMBER(7,4) NULL ,
	Co NUMBER(7,4) NULL ,
	Zr NUMBER(7,4) NULL ,
	Ce NUMBER(7,4) NULL ,
	Fe NUMBER(7,4) NULL
	)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.14.	实时数据记录（PRO_BOF_HIS_RDATA）(暂跳过)

	# --# --# --# --# --# --以上为字段添加# --# --# --# --# --# --# --# --# ---！分！界！线！# --# --# --# --# --# --# --# --以下为数据添加# --# --# --# --# --# --# --# --# --# --# --# --# --# --# --# --# ---
	# --添加数据 记得一定要commit!!!
	# --1.1.1.1.	炉次计划表（PRO_BOF_HIS_PLAN）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_PLAN_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	        SET a.MSG_DATE_PLAN =b.MSG_DATE ,
	        a.WORK_SHOP_PLAN =b.WORK_SHOP,
	        a.PLANT_DIFF=b.PLANT_DIFF ,
	        a.HEAT_ORDER=b.HEAT_ORDER ,
	        a.GE_NO=b.GE_NO,
	        a.GK_NO=b.GK_NO,
	        a.SPECIFICATION=b.SPECIFICATION,
	        a.PROCESS_CODE1=b.PROCESS_CODE1 ,
	        a.SAMPLE_CODE=b.SAMPLE_CODE ,
	        a.HEAT_WGT=b.HEAT_WGT,
	        a.PLAN_DATE=b.PLAN_DATE,
	        a.HEAT_PATH=b.HEAT_PATH,
	        a.CAST_NO=b.CAST_NO,
	        a.CAST_SEQ=b.CAST_SEQ,
	        a.PLAN_STATUS=b.PLAN_STATUS
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,MSG_DATE_PLAN ,WORK_SHOP_PLAN ,PLANT_DIFF,HEAT_ORDER,GE_NO,GK_NO,"SPECIFICATION",PROCESS_CODE1 ,SAMPLE_CODE ,
	HEAT_WGT,PLAN_DATE,HEAT_PATH,CAST_NO,CAST_SEQ,PLAN_STATUS )
	    VALUES (b.HEAT_NO,b.MSG_DATE, b.WORK_SHOP, b.PLANT_DIFF, b.HEAT_ORDER, b.GE_NO, b.GK_NO, b."SPECIFICATION", b.PROCESS_CODE1 , b.SAMPLE_CODE ,
	    b.HEAT_WGT, b.PLAN_DATE, b.HEAT_PATH, b.CAST_NO, b.CAST_SEQ, b.PLAN_STATUS);
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.2.	炉次兑铁信息表（PRO_BOF_HIS_MIRON）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_MIRON_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	        SET a.MSG_DATE_MIRON=b.MSG_DATE,
	        a.MIRON_NO_MIRON=b.MIRON_NO,
	        a.LDL_NO_MIRON=b.LDL_NO,
	        a.MIRON_WGT = b.MIRON_WGT,
	        a.MIRON_TEMP = b.MIRON_TEMP,
	        a.MIRON_C = b.MIRON_C,
	        a.MIRON_SI = b.MIRON_SI,
	        a.MIRON_MN = b.MIRON_MN,
	        a.MIRON_P = b.MIRON_P,
	        a.MIRON_S = b.MIRON_S
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,MSG_DATE_MIRON,MIRON_NO_MIRON, LDL_NO_MIRON,MIRON_WGT, MIRON_TEMP,MIRON_C,MIRON_SI,MIRON_MN,MIRON_P,MIRON_S)
	    VALUES (b.HEAT_NO,b.MSG_DATE,b.MIRON_NO, b.LDL_NO, b.MIRON_WGT, b.MIRON_TEMP,b.MIRON_C,b.MIRON_SI,b.MIRON_MN,b.MIRON_P,b.MIRON_S);
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.3.	炉次兑废钢信息表（PRO_BOF_HIS_SCRAP）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_SCRAP_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	    SET a.MSG_DATE_SCRAP=b.MSG_DATE,
	    a.LDL_NO_SCRAP= b.LDL_NO,
	    a.SCRAP_NUM= b.SCRAP_NUM,
	    a.scrap_96053101= b.scrap_96053101 ,
	    a.scrap_96052200= b.scrap_96052200 ,
	    a.scrap_16010101= b.scrap_16010101 ,
	    a.scrap_16020101= b.scrap_16020101 ,
	    a.scrap_16030101= b.scrap_16030101 ,
	    a.scrap_16040101= b.scrap_16040101 ,
	    a.scrap_96052501= b.scrap_96052501
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,MSG_DATE_SCRAP,LDL_NO_SCRAP, SCRAP_NUM,scrap_96053101, scrap_96052200,scrap_16010101,scrap_16020101,scrap_16030101,scrap_16040101,scrap_96052501)
	    VALUES (b.HEAT_NO,b.MSG_DATE,b.LDL_NO, b.SCRAP_NUM,b.scrap_96053101, b.scrap_96052200,b.scrap_16010101,b.scrap_16020101,b.scrap_16030101,b.scrap_16040101,b.scrap_96052501);
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.4.	炉次实绩表（PRO_BOF_HIS_POOL）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_POOL_RESULT) B
	ON (a.HEAT_NO = b.HEATNO)
	WHEN MATCHED THEN
	    UPDATE
	    SET a.MSG_DATE_POOL= b.MSG_DATE,
	    a.WORK_SHOP_POOL= b.WORK_SHOP ,
	    a.OPERATEDATE=b.OPERATEDATE,
	    a.OPERATESHIFT=b.OPERATESHIFT,
	    a.OPERATECREW=b.OPERATECREW,
	    a.OPERATOR=b.OPERATOR    ,
	    a.STATION=b.STATION,
	    a.HEATORDER=b.HEATORDER  ,
	    a.FURNACESEQ=b.FURNACESEQ  ,
	    a.SPRAYGUNLOC=b.SPRAYGUNLOC  ,
	    a.SPRAYGUNSEQ=b.SPRAYGUNSEQ  ,
	    a.GUNCHANGERES=b.GUNCHANGERES ,
	    a.HOTMETALWGT=b.HOTMETALWGT  ,
	    a.COLDPIGWGT=b.COLDPIGWGT   ,
	    a.SCRAPWGT=b.SCRAPWGT   ,
	    a.SLAGWGT=b.SLAGWGT   ,
	    a.RETURNSTEELWEIGHT=b.RETURNSTEELWEIGHT  ,
	    a.RETURNHEATNO=b.RETURNHEATNO   ,
	    a.RETURNMEMO=b.RETURNMEMO    ,
	    a.DOWNFURNACETIMES=b.DOWNFURNACETIMES   ,
	    a.PUTSPRAYGUNTIME=b.PUTSPRAYGUNTIME    ,
	    a.CARBONTEMPERATURE=b.CARBONTEMPERATURE ,
	    a.FIRSTCATCHCARBONC=b.FIRSTCATCHCARBONC  ,
	    a.FIRSTCATCHCARBONP=b.FIRSTCATCHCARBONP   ,
	    a.SUBLANCE_AGE=b.SUBLANCE_AGE   ,
	    a.SUBLANCE_INDEPTH=b.SUBLANCE_INDEPTH  ,
	    a.O_CONT=b.O_CONT   ,
	    a.C_CONT=b.C_CONT  ,
	    a.LEQHEIGH=b.LEQHEIGH   ,
	    a.STOVEHEATSNUM=b.STOVEHEATSNUM   ,
	    a.PITPATCHINGKIND=b.PITPATCHINGKIND,
	    a.BOTTOMBLOWING=b.BOTTOMBLOWING    ,
	    a.FIRSTCATCHOXYGENCONSUME=b.FIRSTCATCHOXYGENCONSUME  ,
	    a.TIMEOFOXYGEN=b.TIMEOFOXYGEN   ,
	    a.TOTALOXYGENCONSUME=b.TOTALOXYGENCONSUME   ,
	    a.TOTALTIMEOFOXYGEN=b.TOTALTIMEOFOXYGEN   ,
	    a.N2CONSUME=b.N2CONSUME   ,
	    a.TIMEOFSLAGSPLISHING=b.TIMEOFSLAGSPLISHING   ,
	    a.BEFARTEMP=b.BEFARTEMP   ,
	    a.STEELWGT=b.STEELWGT   ,
	    a.PERIOD=b.PERIOD   ,
	    a.IS_NO=b.IS_NO    ,
	    a.TLADLENO=b.TLADLENO    ,
	    a.IS_TEMP=b.IS_TEMP   ,
	    a.TAPPINGSTARTDATE=b.TAPPINGSTARTDATE    ,
	    a.TAPPINGSTARTTIME=b.TAPPINGSTARTTIME    ,
	    a.TAPPINGENDDATE=b.TAPPINGENDDATE    ,
	    a.TAPPINGENDTIME=b.TAPPINGENDTIME    ,
	    a.MEMO=b.MEMO    ,
	    a.LADLENO=b.LADLENO    ,
	    a.LADLESTATUS=b.LADLESTATUS    ,
	    a.LADLEAGE=b.LADLEAGE    ,
	    a.SLAGTHICK=b.SLAGTHICK   ,
	    a.SCRAPSTEEL=b.SCRAPSTEEL  ,
	    a.INSULATIONAGENT=b.INSULATIONAGENT   ,
	    a.OPERATETIME=b.OPERATETIME   ,
	    a.ARRIVEDATE=b.ARRIVEDATE    ,
	    a.ARRIVETIME=b.ARRIVETIME    ,
	    a.DEPARTUREDATE=b.DEPARTUREDATE    ,
	    a.DEPARTURETIME=b.DEPARTURETIME    ,
	    a.TEMPOFARRIVE=b.TEMPOFARRIVE  ,
	    a.TEMPOFDEPARTURE=b.TEMPOFDEPARTURE  ,
	    a.OPERATORA=b.OPERATORA    ,
	    a.OPERATORB=b.OPERATORB    ,
	    a.OPERATORC=b.OPERATORC    ,
	    a.OPERATORD=b.OPERATORD    ,
	    a.OPERATORE=b.OPERATORE
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,MSG_DATE_POOL ,WORK_SHOP_POOL,OPERATEDATE ,OPERATESHIFT,OPERATECREW ,"OPERATOR" ,HEATORDER ,FURNACESEQ ,SPRAYGUNLOC ,
	SPRAYGUNSEQ ,GUNCHANGERES ,HOTMETALWGT ,COLDPIGWGT ,SCRAPWGT ,SLAGWGT ,RETURNSTEELWEIGHT ,RETURNHEATNO ,RETURNMEMO ,
	DOWNFURNACETIMES ,PUTSPRAYGUNTIME ,CARBONTEMPERATURE ,FIRSTCATCHCARBONC ,FIRSTCATCHCARBONP,SUBLANCE_AGE,SUBLANCE_INDEPTH ,O_CONT ,
	C_CONT,LEQHEIGH ,STOVEHEATSNUM ,PITPATCHINGKIND ,BOTTOMBLOWING ,FIRSTCATCHOXYGENCONSUME ,TIMEOFOXYGEN ,TOTALOXYGENCONSUME ,
	TOTALTIMEOFOXYGEN,N2CONSUME ,TIMEOFSLAGSPLISHING ,BEFARTEMP ,STEELWGT ,PERIOD ,IS_NO ,TLADLENO ,IS_TEMP ,TAPPINGSTARTDATE ,
	TAPPINGSTARTTIME ,TAPPINGENDDATE ,TAPPINGENDTIME ,MEMO ,LADLENO ,LADLESTATUS ,LADLEAGE ,SLAGTHICK ,SCRAPSTEEL ,INSULATIONAGENT ,
	OPERATETIME,ARRIVEDATE,ARRIVETIME ,DEPARTUREDATE,DEPARTURETIME,TEMPOFARRIVE ,TEMPOFDEPARTURE,OPERATORA ,OPERATORB,OPERATORC,OPERATORD,OPERATORE
	)
	    VALUES (b.HEATNO,b.MSG_DATE ,b.WORK_SHOP,b.OPERATEDATE ,b.OPERATESHIFT,b.OPERATECREW ,b."OPERATOR",b.HEATORDER ,b.FURNACESEQ ,b.SPRAYGUNLOC ,b.
	SPRAYGUNSEQ ,b.GUNCHANGERES ,b.HOTMETALWGT ,b.COLDPIGWGT ,b.SCRAPWGT ,b.SLAGWGT ,b.RETURNSTEELWEIGHT ,b.RETURNHEATNO ,b.RETURNMEMO ,b.
	DOWNFURNACETIMES ,b.PUTSPRAYGUNTIME ,b.CARBONTEMPERATURE ,b.FIRSTCATCHCARBONC ,b.FIRSTCATCHCARBONP,b.SUBLANCE_AGE,b.SUBLANCE_INDEPTH ,b.O_CONT ,b.
	C_CONT,b.LEQHEIGH ,b.STOVEHEATSNUM ,b.PITPATCHINGKIND ,b.BOTTOMBLOWING ,b.FIRSTCATCHOXYGENCONSUME ,b.TIMEOFOXYGEN ,b.TOTALOXYGENCONSUME ,b.
	TOTALTIMEOFOXYGEN,b.N2CONSUME ,b.TIMEOFSLAGSPLISHING ,b.BEFARTEMP ,b.STEELWGT ,b.PERIOD ,b.IS_NO ,b.TLADLENO ,b.IS_TEMP ,b.TAPPINGSTARTDATE ,b.
	TAPPINGSTARTTIME ,b.TAPPINGENDDATE ,b.TAPPINGENDTIME ,b.MEMO ,b.LADLENO ,b.LADLESTATUS ,b.LADLEAGE ,b.SLAGTHICK ,b.SCRAPSTEEL ,b.INSULATIONAGENT ,b.
	OPERATETIME,b.ARRIVEDATE,b.ARRIVETIME ,b.DEPARTUREDATE,b.DEPARTURETIME,b.TEMPOFARRIVE ,b.TEMPOFDEPARTURE,b.OPERATORA ,b.OPERATORB,b.OPERATORC,b.OPERATORD,b.OPERATORE
	);
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.5.	炉次事件表（PRO_BOF_HIS_EVENTS）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_EVENTS_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	    SET a.Event_3001 =b.Event_3001 ,
	    a.Event_3002 =b.Event_3002 ,
	    a.Event_3003 =b.Event_3003 ,
	    a.Event_3004 =b.Event_3004 ,
	    a.Event_3010 =b.Event_3010 ,
	    a.Event_3011 =b.Event_3011 ,
	    a.Event_3012 =b.Event_3012 ,
	    a.Event_3013 =b.Event_3013 ,
	    a.Event_4003 =b.Event_4003 ,
	    a.Event_4004 =b.Event_4004
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,Event_3001 ,Event_3002 ,Event_3003 ,Event_3004 ,Event_3010 ,Event_3011 ,Event_3012 ,Event_3013 ,Event_4003 ,Event_4004 )
	    VALUES (b.HEAT_NO, b.Event_3001 ,b.EVENT_3002 ,b.EVENT_3003 ,b.EVENT_3004 ,b.EVENT_3010 ,b.EVENT_3011 ,b.EVENT_3012 ,b.EVENT_3013 ,b.EVENT_4003 ,b.EVENT_4004 );
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.6.	炉次吹氧记录表（PRO_BOF_HIS_BOCSM）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_BOCSM_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	    SET	a.SUM_BO_CSM=b.SUM_BO_CSM,
	    a.SUM_BO_DUR=b.SUM_BO_DUR,
	    a.D1_BOSTRT_TIME=b.D1_BOSTRT_TIME ,
	    a.D1_BOEND_TIME=b.D1_BOEND_TIME ,
	    a.D1_BO_DUR=b.D1_BO_DUR  ,
	    a.D1_BO_CSM=b.D1_BO_CSM,
	    a.D2_BOSTRT_TIME=b.D2_BOSTRT_TIME ,
	    a.D2_BOEND_TIME=b.D2_BOEND_TIME ,
	    a.D2_BO_DUR=b.D2_BO_DUR  ,
	    a.D2_BO_CSM=b.D2_BO_CSM,
	    a.D3_BOSTRT_TIME=b.D3_BOSTRT_TIME ,
	    a.D3_BOEND_TIME=b.D3_BOEND_TIME ,
	    a.D3_BO_DUR=b.D3_BO_DUR  ,
	    a.D3_BO_CSM=b.D3_BO_CSM,
	    a.D4_BOSTRT_TIME=b.D4_BOSTRT_TIME ,
	    a.D4_BOEND_TIME=b.D4_BOEND_TIME ,
	    a.D4_BO_DUR=b.D4_BO_DUR  ,
	    a.D4_BO_CSM=b.D4_BO_CSM,
	    a.D5_BOSTRT_TIME=b.D5_BOSTRT_TIME ,
	    a.D5_BOEND_TIME=b.D5_BOEND_TIME ,
	    a.D5_BO_DUR=b.D5_BO_DUR  ,
	    a.D5_BO_CSM=b.D5_BO_CSM,
	    a.D6_BOSTRT_TIME=b.D6_BOSTRT_TIME ,
	    a.D6_BOEND_TIME=b.D6_BOEND_TIME ,
	    a.D6_BO_DUR=b.D6_BO_DUR  ,
	    a.D6_BO_CSM=b.D6_BO_CSM
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,STATION,SUM_BO_CSM,SUM_BO_DUR,D1_BOSTRT_TIME ,D1_BOEND_TIME ,D1_BO_DUR  ,D1_BO_CSM,D2_BOSTRT_TIME ,D2_BOEND_TIME ,D2_BO_DUR  ,D2_BO_CSM,D3_BOSTRT_TIME ,
	D3_BOEND_TIME ,D3_BO_DUR  ,D3_BO_CSM,D4_BOSTRT_TIME ,D4_BOEND_TIME ,D4_BO_DUR  ,D4_BO_CSM,D5_BOSTRT_TIME ,D5_BOEND_TIME ,
	D5_BO_DUR  ,D5_BO_CSM,D6_BOSTRT_TIME ,D6_BOEND_TIME ,D6_BO_DUR  ,D6_BO_CSM )
	    VALUES (b.HEAT_NO, b.STATION,b.SUM_BO_CSM, b.SUM_BO_DUR, b.D1_BOSTRT_TIME , b.D1_BOEND_TIME , b.D1_BO_DUR  , b.D1_BO_CSM, b.D2_BOSTRT_TIME , b.D2_BOEND_TIME , b.D2_BO_DUR  , b.D2_BO_CSM, b.D3_BOSTRT_TIME , b.
	D3_BOEND_TIME , b.D3_BO_DUR  , b.D3_BO_CSM, b.D4_BOSTRT_TIME , b.D4_BOEND_TIME , b.D4_BO_DUR  , b.D4_BO_CSM, b.D5_BOSTRT_TIME , b.D5_BOEND_TIME , b.
	D5_BO_DUR  , b.D5_BO_CSM, b.D6_BOSTRT_TIME , b.D6_BOEND_TIME , b.D6_BO_DUR  , b.D6_BO_CSM );
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.7.	炉次测温表（PRO_BOF_HIS_TEMP）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_TEMP_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	    SET a.final_TEMP_NO =b.final_TEMP_NO ,
	    a.final_TEMP_TIME =b.final_TEMP_TIME ,
	    a.final_TEMP_VALUE =b.final_TEMP_VALUE ,
	    a.final_TEMP_TYPE =b.final_TEMP_TYPE ,
	    a.final_TEMP_ACQ =b.final_TEMP_ACQ ,
	    a.D1_TEMP_TIME =b.D1_TEMP_TIME ,
	    a.D1_TEMP_VALUE =b.D1_TEMP_VALUE ,
	    a.D1_TEMP_TYPE =b.D1_TEMP_TYPE ,
	    a.D1_TEMP_ACQ =b.D1_TEMP_ACQ ,
	    a.D2_TEMP_TIME =b.D2_TEMP_TIME ,
	    a.D2_TEMP_VALUE =b.D2_TEMP_VALUE ,
	    a.D2_TEMP_TYPE =b.D2_TEMP_TYPE ,
	    a.D2_TEMP_ACQ =b.D2_TEMP_ACQ ,
	    a.D3_TEMP_TIME =b.D3_TEMP_TIME ,
	    a.D3_TEMP_VALUE =b.D3_TEMP_VALUE ,
	    a.D3_TEMP_TYPE =b.D3_TEMP_TYPE ,
	    a.D3_TEMP_ACQ =b.D3_TEMP_ACQ ,
	    a.D4_TEMP_TIME =b.D4_TEMP_TIME ,
	    a.D4_TEMP_VALUE =b.D4_TEMP_VALUE ,
	    a.D4_TEMP_TYPE =b.D4_TEMP_TYPE ,
	    a.D4_TEMP_ACQ =b.D4_TEMP_ACQ
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,final_TEMP_NO ,final_TEMP_TIME ,final_TEMP_VALUE ,final_TEMP_TYPE ,final_TEMP_ACQ ,D1_TEMP_TIME ,D1_TEMP_VALUE ,D1_TEMP_TYPE ,D1_TEMP_ACQ ,
	D2_TEMP_TIME ,D2_TEMP_VALUE ,D2_TEMP_TYPE ,D2_TEMP_ACQ ,D3_TEMP_TIME ,D3_TEMP_VALUE ,D3_TEMP_TYPE ,D3_TEMP_ACQ ,D4_TEMP_TIME ,
	D4_TEMP_VALUE ,D4_TEMP_TYPE ,D4_TEMP_ACQ  )
	    VALUES (b.HEAT_NO,b.final_TEMP_NO ,b.final_TEMP_TIME ,b.final_TEMP_VALUE ,b.final_TEMP_TYPE ,b.final_TEMP_ACQ ,b.D1_TEMP_TIME ,b.D1_TEMP_VALUE ,b.D1_TEMP_TYPE ,b.D1_TEMP_ACQ ,
	b.D2_TEMP_TIME ,b.D2_TEMP_VALUE ,b.D2_TEMP_TYPE ,b.D2_TEMP_ACQ ,b.D3_TEMP_TIME ,b.D3_TEMP_VALUE ,b.D3_TEMP_TYPE ,b.D3_TEMP_ACQ ,b.D4_TEMP_TIME ,
	b.D4_TEMP_VALUE ,b.D4_TEMP_TYPE ,b.D4_TEMP_ACQ  );
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.8.	炉次加料表A（PRO_BOF_HIS_CHRGDGEN）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_CHRGDGEN_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	    SET a.D1_CHRGD_TIME=b.D1_CHRGD_TIME,a.D1_CHRGD_TYPE=b.D1_CHRGD_TYPE  ,
	     a.D2_CHRGD_TIME=b.D2_CHRGD_TIME,    a.D2_CHRGD_TYPE=b.D2_CHRGD_TYPE  ,
	     a.D3_CHRGD_TIME=b.D3_CHRGD_TIME,    a.D3_CHRGD_TYPE=b.D3_CHRGD_TYPE  ,
	     a.D4_CHRGD_TIME=b.D4_CHRGD_TIME,    a.D4_CHRGD_TYPE=b.D4_CHRGD_TYPE  ,
	     a.D5_CHRGD_TIME=b.D5_CHRGD_TIME,    a.D5_CHRGD_TYPE=b.D5_CHRGD_TYPE  ,
	     a.D6_CHRGD_TIME=b.D6_CHRGD_TIME,    a.D6_CHRGD_TYPE=b.D6_CHRGD_TYPE  ,
	     a.D7_CHRGD_TIME=b.D7_CHRGD_TIME,    a.D7_CHRGD_TYPE=b.D7_CHRGD_TYPE  ,
	     a.D8_CHRGD_TIME=b.D8_CHRGD_TIME,    a.D8_CHRGD_TYPE=b.D8_CHRGD_TYPE  ,
	     a.D9_CHRGD_TIME=b.D9_CHRGD_TIME,    a.D9_CHRGD_TYPE=b.D9_CHRGD_TYPE  ,
	     a.D10_CHRGD_TIME=b.D10_CHRGD_TIME,    a.D10_CHRGD_TYPE=b.D10_CHRGD_TYPE  ,
	     a.D11_CHRGD_TIME=b.D11_CHRGD_TIME,    a.D11_CHRGD_TYPE=b.D11_CHRGD_TYPE  ,
	     a.D12_CHRGD_TIME=b.D12_CHRGD_TIME,    a.D12_CHRGD_TYPE=b.D12_CHRGD_TYPE  ,
	     a.D13_CHRGD_TIME=b.D13_CHRGD_TIME,    a.D13_CHRGD_TYPE=b.D13_CHRGD_TYPE  ,
	     a.D14_CHRGD_TIME=b.D14_CHRGD_TIME,    a.D14_CHRGD_TYPE=b.D14_CHRGD_TYPE  ,
	     a.D15_CHRGD_TIME=b.D15_CHRGD_TIME,    a.D15_CHRGD_TYPE=b.D15_CHRGD_TYPE  ,
	     a.D16_CHRGD_TIME=b.D16_CHRGD_TIME,    a.D16_CHRGD_TYPE=b.D16_CHRGD_TYPE  ,
	     a.D17_CHRGD_TIME=b.D17_CHRGD_TIME,    a.D17_CHRGD_TYPE=b.D17_CHRGD_TYPE  ,
	     a.D18_CHRGD_TIME=b.D18_CHRGD_TIME,    a.D18_CHRGD_TYPE=b.D18_CHRGD_TYPE  ,
	     a.D19_CHRGD_TIME=b.D19_CHRGD_TIME,    a.D19_CHRGD_TYPE=b.D19_CHRGD_TYPE  ,
	     a.D20_CHRGD_TIME=b.D20_CHRGD_TIME,    a.D20_CHRGD_TYPE=b.D20_CHRGD_TYPE  ,
	     a.D21_CHRGD_TIME=b.D21_CHRGD_TIME,    a.D21_CHRGD_TYPE=b.D21_CHRGD_TYPE  ,
	     a.D22_CHRGD_TIME=b.D22_CHRGD_TIME,    a.D22_CHRGD_TYPE=b.D22_CHRGD_TYPE  ,
	     a.D23_CHRGD_TIME=b.D23_CHRGD_TIME,    a.D23_CHRGD_TYPE=b.D23_CHRGD_TYPE  ,
	     a.D24_CHRGD_TIME=b.D24_CHRGD_TIME,    a.D24_CHRGD_TYPE=b.D24_CHRGD_TYPE  ,
	     a.D25_CHRGD_TIME=b.D25_CHRGD_TIME,    a.D25_CHRGD_TYPE=b.D25_CHRGD_TYPE  ,
	     a.D26_CHRGD_TIME=b.D26_CHRGD_TIME,    a.D26_CHRGD_TYPE=b.D26_CHRGD_TYPE  ,
	     a.D27_CHRGD_TIME=b.D27_CHRGD_TIME,    a.D27_CHRGD_TYPE=b.D27_CHRGD_TYPE  ,
	     a.D28_CHRGD_TIME=b.D28_CHRGD_TIME,    a.D28_CHRGD_TYPE=b.D28_CHRGD_TYPE  ,
	     a.D29_CHRGD_TIME=b.D29_CHRGD_TIME,    a.D29_CHRGD_TYPE=b.D29_CHRGD_TYPE  ,
	     a.D30_CHRGD_TIME=b.D30_CHRGD_TIME,    a.D30_CHRGD_TYPE=b.D30_CHRGD_TYPE
	 WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,STATION, D1_CHRGD_TIME,D1_CHRGD_TYPE  ,
	 D2_CHRGD_TIME,D2_CHRGD_TYPE  ,
	 D3_CHRGD_TIME,D3_CHRGD_TYPE  ,
	 D4_CHRGD_TIME,D4_CHRGD_TYPE  ,
	 D5_CHRGD_TIME,D5_CHRGD_TYPE  ,
	 D6_CHRGD_TIME,D6_CHRGD_TYPE  ,
	 D7_CHRGD_TIME,D7_CHRGD_TYPE  ,
	 D8_CHRGD_TIME,D8_CHRGD_TYPE  ,
	 D9_CHRGD_TIME,D9_CHRGD_TYPE  ,
	 D10_CHRGD_TIME,D10_CHRGD_TYPE  ,
	 D11_CHRGD_TIME,D11_CHRGD_TYPE  ,
	 D12_CHRGD_TIME,D12_CHRGD_TYPE  ,
	 D13_CHRGD_TIME,D13_CHRGD_TYPE  ,
	 D14_CHRGD_TIME,D14_CHRGD_TYPE  ,
	 D15_CHRGD_TIME,D15_CHRGD_TYPE  ,
	 D16_CHRGD_TIME,D16_CHRGD_TYPE  ,
	 D17_CHRGD_TIME,D17_CHRGD_TYPE  ,
	 D18_CHRGD_TIME,D18_CHRGD_TYPE  ,
	 D19_CHRGD_TIME,D19_CHRGD_TYPE  ,
	 D20_CHRGD_TIME,D20_CHRGD_TYPE  ,
	 D21_CHRGD_TIME,D21_CHRGD_TYPE  ,
	 D22_CHRGD_TIME,D22_CHRGD_TYPE  ,
	 D23_CHRGD_TIME,D23_CHRGD_TYPE  ,
	 D24_CHRGD_TIME,D24_CHRGD_TYPE  ,
	 D25_CHRGD_TIME,D25_CHRGD_TYPE  ,
	 D26_CHRGD_TIME,D26_CHRGD_TYPE  ,
	 D27_CHRGD_TIME,D27_CHRGD_TYPE  ,
	 D28_CHRGD_TIME,D28_CHRGD_TYPE  ,
	 D29_CHRGD_TIME,D29_CHRGD_TYPE  ,
	 D30_CHRGD_TIME,D30_CHRGD_TYPE  )
	    VALUES (
	    b.HEAT_NO, b.STATION, b.D1_CHRGD_TIME,b.D1_CHRGD_TYPE  ,
	 b.D2_CHRGD_TIME,b.D2_CHRGD_TYPE  ,
	 b.D3_CHRGD_TIME,b.D3_CHRGD_TYPE  ,
	 b.D4_CHRGD_TIME,b.D4_CHRGD_TYPE  ,
	 b.D5_CHRGD_TIME,b.D5_CHRGD_TYPE  ,
	 b.D6_CHRGD_TIME,b.D6_CHRGD_TYPE  ,
	 b.D7_CHRGD_TIME,b.D7_CHRGD_TYPE  ,
	 b.D8_CHRGD_TIME,b.D8_CHRGD_TYPE  ,
	 b.D9_CHRGD_TIME,b.D9_CHRGD_TYPE  ,
	 b.D10_CHRGD_TIME,b.D10_CHRGD_TYPE  ,
	 b.D11_CHRGD_TIME,b.D11_CHRGD_TYPE  ,
	 b.D12_CHRGD_TIME,b.D12_CHRGD_TYPE  ,
	 b.D13_CHRGD_TIME,b.D13_CHRGD_TYPE  ,
	 b.D14_CHRGD_TIME,b.D14_CHRGD_TYPE  ,
	 b.D15_CHRGD_TIME,b.D15_CHRGD_TYPE  ,
	 b.D16_CHRGD_TIME,b.D16_CHRGD_TYPE  ,
	 b.D17_CHRGD_TIME,b.D17_CHRGD_TYPE  ,
	 b.D18_CHRGD_TIME,b.D18_CHRGD_TYPE  ,
	 b.D19_CHRGD_TIME,b.D19_CHRGD_TYPE  ,
	 b.D20_CHRGD_TIME,b.D20_CHRGD_TYPE  ,
	 b.D21_CHRGD_TIME,b.D21_CHRGD_TYPE  ,
	 b.D22_CHRGD_TIME,b.D22_CHRGD_TYPE  ,
	 b.D23_CHRGD_TIME,b.D23_CHRGD_TYPE  ,
	 b.D24_CHRGD_TIME,b.D24_CHRGD_TYPE  ,
	 b.D25_CHRGD_TIME,b.D25_CHRGD_TYPE  ,
	 b.D26_CHRGD_TIME,b.D26_CHRGD_TYPE  ,
	 b.D27_CHRGD_TIME,b.D27_CHRGD_TYPE  ,
	 b.D28_CHRGD_TIME,b.D28_CHRGD_TYPE  ,
	 b.D29_CHRGD_TIME,b.D29_CHRGD_TYPE  ,
	 b.D30_CHRGD_TIME,b.D30_CHRGD_TYPE   );
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.9.	炉次加料表B（PRO_BOF_HIS_CHRGDDAT）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_CHRGDDAT_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	        SET a.L12010301 = b.L12010301,
	        a.L12010302 = b.L12010302,
	        a.L12010601 = b.L12010601,
	        a.L12010701 = b.L12010701,
	        a.L12020201 = b.L12020201,
	        a.L12020301 = b.L12020301,
	        a.L13010101 = b.L13010101,
	        a.L13010301 = b.L13010301,
	        a.L13020101 = b.L13020101,
	        a.L13020201 = b.L13020201,
	        a.L13020501 = b.L13020501,
	        a.L13040400 = b.L13040400,
	        a.L96020400 = b.L96020400,
	        a.L96040100 = b.L96040100,
	        a.L96040200 = b.L96040200,
	        a.L96053601 = b.L96053601,
	        a.L1602010074 = b.L1602010074
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,STATION,L12010301,L12010302,L12010601,L12010701,L12020201,L12020301,
	    L13010101,L13010301,L13020101,L13020201,L13020501,L13040400,L96020400,L96040100,L96040200,L96053601,L1602010074)
	    VALUES (b.HEAT_NO, b.STATION, b.L12010301,b.L12010302,b.L12010601,b.L12010701,b.L12020201,b.L12020301,
	    b.L13010101,b.L13010301,b.L13020101,b.L13020201,b.L13020501,b.L13040400,b.L96020400,b.L96040100,b.L96040200,b.L96053601,b.L1602010074);
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.10.	线上设备信息（PRO_BOF_HIS_EQPONLINE）	跳过
	# --1.1.1.11.	设备维修记录表（PRO_BOF_HIS_EQPLOG）跳过
	# --1.1.1.12.	取样信息记录（PRO_BOF_HIS_ANAGEN）	(由于原表中存在一个炉次号对应不同个站别的情况，因此删除了站别字段，由其他表进行补充)
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_ANAGEN_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	    SET a.D1_SAMP_TIME =b.D1_SAMP_TIME ,
	    a.D1_SAMP_TYPE =b.D1_SAMP_TYPE ,
	    a.D2_SAMP_TIME =b.D2_SAMP_TIME ,
	    a.D2_SAMP_TYPE =b.D2_SAMP_TYPE ,
	    a.D3_SAMP_TIME =b.D3_SAMP_TIME ,
	    a.D3_SAMP_TYPE =b.D3_SAMP_TYPE ,
	    a.D4_SAMP_TIME =b.D4_SAMP_TIME ,
	    a.D4_SAMP_TYPE =b.D4_SAMP_TYPE ,
	    a.D5_SAMP_TIME =b.D5_SAMP_TIME ,
	    a.D5_SAMP_TYPE =b.D5_SAMP_TYPE
	WHEN NOT MATCHED THEN
	    INSERT (HEAT_NO,D1_SAMP_TIME ,D1_SAMP_TYPE ,D2_SAMP_TIME ,D2_SAMP_TYPE ,D3_SAMP_TIME ,D3_SAMP_TYPE ,D4_SAMP_TIME ,D4_SAMP_TYPE ,D5_SAMP_TIME ,D5_SAMP_TYPE )
	    VALUES (b.HEAT_NO, b.D1_SAMP_TIME ,b.D1_SAMP_TYPE ,b.D2_SAMP_TIME ,b.D2_SAMP_TYPE ,b.D3_SAMP_TIME ,b.D3_SAMP_TYPE ,b.D4_SAMP_TIME ,b.D4_SAMP_TYPE ,b.D5_SAMP_TIME ,b.D5_SAMP_TYPE );
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --1.1.1.13.	成分信息记录（PRO_BOF_HIS_ANADAT）
	sqlVO["sql"]='''MERGE INTO PRO_BOF_HIS_ALLFIELDS A
	USING(select * from PRO_BOF_HIS_ANADAT_RESULT) B
	ON (a.HEAT_NO = b.HEAT_NO)
	WHEN MATCHED THEN
	    UPDATE
	        SET  a.C=b.C,
	        a.Si=b.Si,
	        a.Mn=b.Mn,
	        a.P=b.P,
	        a.S=b.S,
	        a.AL_T=b.AL_T ,
	        a.AL_S=b.AL_S,
	        a.Ni=b.Ni ,
	        a.Cr=b.Cr ,
	        a.Cu=b.Cu ,
	        a.Mo=b.Mo ,
	        a.V=b.V ,
	        a.Ti=b.Ti ,
	        a.Nb=b.Nb ,
	        a.W=b.W ,
	        a.Pb=b.Pb ,
	        a.Sn=b.Sn ,
	        a."AS"=b."AS",
	        a.Bi=b.Bi ,
	        a.B=b.B ,
	        a.Ca=b.Ca ,
	        a.N=b.N ,
	        a.Co=b.Co ,
	        a.Zr=b.Zr ,
	        a.Ce=b.Ce ,
	        a.Fe=b.Fe
	WHEN NOT MATCHED THEN
	    INSERT (a.HEAT_NO,C,Si,Mn,P,S,AL_T,AL_S,Ni,Cr,Cu,Mo,V,Ti,Nb,W,Pb,Sn,"AS",Bi,B,Ca,N,Co,Zr,Ce,Fe)
	    VALUES (b.HEAT_NO, b.C,b.Si,b.Mn,b.P,b.S,b.AL_T,b.AL_S,b.Ni,b.Cr,b.Cu,b.Mo,b.V,b.Ti,b.Nb,b.W,b.Pb,b.Sn,b."AS",b.Bi,b.B,b.Ca,b.N,b.Co,b.Zr,b.Ce,b.Fe );
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1.1.1.14.	实时数据记录（PRO_BOF_HIS_RDATA）	跳过

#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#--------------------------------------------------INSERT SUMMURY TABLE--------------------------------------
#总处理汇总--------------------------------------------------

	# --将铁水重量减去一吨
	sqlVO["sql"]='''update pro_bof_his_allfields set  miron_wgt = miron_wgt - 1000 where  miron_wgt>1000;
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --1、把工序代码(plant_diff)整合到站别（station）,然后删除工序代码字段
	sqlVO["sql"]='''UPDATE pro_bof_his_allfields SET station = plant_diff WHERE station is null;
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column plant_diff''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --2、将各废钢明细加和存储为字段
	sqlVO["sql"]='''alter table pro_bof_his_allfields add  SCRAPWGT_count number(6);--废钢加入量（所有废钢加和得）
	update pro_bof_his_allfields set SCRAPWGT_count=scrap_96053101+scrap_96052200+scrap_16010101+scrap_16020101+scrap_16030101+scrap_16040101+scrap_96052501;
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --3、对出钢量进行补充
	# --首先保留自身出钢量字段（STEELWGT），若不存在，取ccm炉坯重（TOTAL_SLAB_WGT）进行补充，仍缺失，则取计算所得出钢量（STEELWGT_COUNT）进行补充：钢水量=（铁水量+废钢量）*95%
	sqlVO["sql"]='''UPDATE pro_bof_his_allfields a SET a.STEELWGT=(select b.TOTAL_SLAB_WGT from pro_ccm_his_heatplan_Result b where a.heat_no=b.heat_no) WHERE STEELWGT is null or STEELWGT=0;
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''UPDATE pro_bof_his_allfields SET STEELWGT = (MIRON_WGT+SCRAPWGT_count)*0.95 WHERE STEELWGT is null or STEELWGT=0;
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --4、转炉煤气LDG计算
	# --由补充后的出钢量（STEELWGT)计算而来：新建转炉煤气字段：LDG_STEELWGT
	sqlVO["sql"]='''alter table pro_bof_his_allfields add LDG_STEELWGT NUMBER(10,3)'''; 
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''update pro_bof_his_allfields set LDG_STEELWGT=(MIRON_WGT*MIRON_C-STEELWGT*C)*22.4/0.85/12/100;
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --5、计算钢渣，新建钢渣字段：steel_slag 
	sqlVO["sql"]='''alter table pro_bof_his_allfields add steel_slag NUMBER(10,3)''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --更新字段值（使用废钢总和字段进行加和）使用出钢量STEELWGT、转炉煤气LDG_STEELWGT
	sqlVO["sql"]='''update pro_bof_his_allfields set steel_slag =(nvl(SUM_BO_CSM,0)*1.429+SCRAPWGT_COUNT+
	MIRON_WGT+nvl(COLDPIGWGT,0)+nvl(L13010101,0)+nvl(L13010301,0)+nvl(L13020101,0)+nvl(L13020201,0)+nvl(L13020501,0)+nvl(L13040400,0)+nvl(L96020400,0)+
	nvl(L12010301,0)+nvl(L12010302,0)+nvl(L12010601,0)+nvl(L12010701,0)+nvl(L12020201,0)+nvl(L12020301,0)+nvl(L96040100,0)+nvl(L96040200,0)+nvl(L96053601,0)+nvl(L1602010074,0)-
	STEELWGT-nvl(LDG_STEELWGT,0)*1.368)*0.9;
	commit''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)

	# --6、删除字段
	# --删除铁水装入量、铁水入炉温度、渣钢
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column HOTMETALWGT''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column IS_TEMP'''; 
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column SLAGWGT''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --删除出钢开始日期、出钢开始时间、出钢结束日期、出钢结束时间
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column TAPPINGSTARTDATE''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column TAPPINGSTARTTIME'''; 
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column TAPPINGENDDATE''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column TAPPINGENDTIME''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --删除炉长OPERATORD字段，与OPERATORA字段相同
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column OPERATORD''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)
	# --删除炉订号HEATORDER字段，与HEAT_ORDER字段相同
	sqlVO["sql"]='''alter table pro_bof_his_allfields drop column HEATORDER''';
	models.BaseManage().direct_execute_query_sqlVO(sqlVO)


if __name__ == '__main__':
	print ("11111")
	dictionary,conclusionPrint,module_name = sql_stockControl(module,tradeNo,module_unit_key)
	print("stockControl.py文件中的函数执行完毕\n\n")
	#print (module,tradeNo)
'''
drop PUBLIC database link dblink_to_l2;
create public database link dblink_to_l2 connect to report_query identified by qdisqdis
 using '(DESCRIPTION =
(ADDRESS_LIST =
(ADDRESS = (PROTOCOL = TCP)(HOST = 10.30.0.161)(PORT = 1521))
)
(CONNECT_DATA =
(SERVICE_NAME =qgil2dbdg)
)
)';
'''
