# -*- coding: utf-8 -*
from collections import OrderedDict
PRO_BOF_HIS_ALLFIELDS_S=OrderedDict([

								('FURNACESEQ','炉龄'),
								('SPRAYGUNSEQ','枪龄'),
								('MIRON_WGT','铁水重量'),
								('MIRON_TEMP','铁水温度'),
								('MIRON_C','铁水C含量'),
								('MIRON_SI','铁水SI含量'),
								('MIRON_MN','铁水MN含量'),
								('MIRON_P','铁水P含量'),
								('MIRON_S','铁水S含量'),
								('SCRAP_NUM','废钢数量'),
								('scrap_96053101','大渣钢'),
								('scrap_96052200','自产废钢'),
								('scrap_16010101','重型废钢'),
								('scrap_16020101','中型废钢'),
								('scrap_16030101','未知废钢'),
								#('scrap_16040101','破碎废钢'),
								#('scrap_96052501','小渣钢'),
								('COLDPIGWGT','生铁装入量'),
								('SCRAPWGT','废钢装入量'),
								('SCRAPWGT_COUNT','废钢装入计算量'),
								#('RETURNSTEELWEIGHT','回炉钢液量'),
								#('LADLESTATUS','包况'),
								#('LADLEAGE','包龄'),

								('L96020400','1#烧结矿'),
								#('L12010301','石灰石_15-40mm'),
								('L12010302','石灰石_40-70mm'),
								('L12010601','萤石_FL80'),
								#('L12010701','硅灰石'),
								('L12020201','增碳剂'),
								('L12020301','低氮增碳剂'),
								('L96040100','石灰'),
								('L96040200','轻烧白云石'),
								('L96053601','钢渣'),
								('L1602010074','未知料'),
								('HEAT_WGT','炉重(KG)'),
								('BEFARTEMP','氩前温度'),
								('N2CONSUME','氮气耗量'),
								('TOTALOXYGENCONSUME','总供氧耗量'),
								('SUM_BO_CSM','总吹氧消耗'),
								('FIRSTCATCHOXYGENCONSUME','一倒氧气耗量'),
								('CARBONTEMPERATURE','一倒温度(℃)'),
								('FIRSTCATCHCARBONC','一倒C%'),
								('FIRSTCATCHCARBONP','一倒P%'),
								('DOWNFURNACETIMES','倒炉次数'),
								('SUBLANCE_AGE','副枪枪龄'),
								('SUBLANCE_INDEPTH','副枪插入深度'),
								('O_CONT','定氧'),
								#('C_CONT','定碳'),
								('LEQHEIGH','液面高度'),
								('D1_BO_CSM','第一次吹氧消耗'),
								('D2_BO_CSM','第二次吹氧消耗'),
								('D3_BO_CSM','第三次吹氧消耗'),
								('D4_BO_CSM','第四次吹氧消耗'),
								('D5_BO_CSM','第五次吹氧消耗'),
								('D6_BO_CSM','第六次吹氧消耗'),
								('D1_TEMP_VALUE','第一次测温值'),
								('D2_TEMP_VALUE','第二次测温值'),
								('D3_TEMP_VALUE','第三次测温值'),
								('D4_TEMP_VALUE','第四次测温值'),

								('STEELWGT_COUNT','出钢量1'),
								('TOTAL_SLAB_WGT','出钢量2'),
								('LDG_STEELWGT_COUNT','煤气发生量1'),
								('LDG_TOTAL_SLAB_WGT','煤气发生量2'),
								('STEEL_SLAG','钢渣量'),
								('C','C'),
								('Si','Si'),
								('Mn','Mn'),
								('P','P'),
								('S','S'),
								('Al_T','Al_T'),
								('"AS"','AS'),
								('Ni','Ni'),
								('Cr','Cr'),
								('Cu','Cu'),
								('Mo','Mo'),
								('V','V'),
								('Ti','Ti'),
								('Nb','Nb'),
								('W','W'),
								('Pb','Pb'),
								('Sn','Sn'),
								('Bi','Bi'),
								('B','B'),
								('Ca','Ca'),
								('N','N'),
								('Co','Co'),
								('Zr','Zr'),
								('Ce','Ce'),
								('Fe','Fe'),

								('L13010101','硅铁_Si72-80%、AL≤2%(粒度10-60mm)'),
								('L13010301','微铝硅铁_Si 72-80%、AL≤0.1%、Ti≤0.1%'),
								('L13020101','硅锰合金_Mn 65-72%、Si 17-20%'),
								('L13020201','高硅硅锰_Mn ≥60%、Si ≥27%'),
								('L13040400','中碳铬铁'),
								#('SLAGTHICK','渣层厚度'),#1,8
								#('SCRAPSTEEL','调温废钢'),#2,7
								#('INSULATIONAGENT','保温剂(包)'),
								#('TEMPOFARRIVE','进站温度(℃)'),#数据量少
								#'TEMPOFDEPARTURE','出站温度(℃)'),


						])

PRO_BOF_HIS_ALLFIELDS_C=OrderedDict([
								('scrap_16040101','破碎废钢'),
								('scrap_96052501','小渣钢'),
								('RETURNSTEELWEIGHT','回炉钢液量'),
								('LADLESTATUS','包况'),
								('LADLEAGE','包龄'),
								('L12010301','石灰石_15-40mm'),
								('L12010701','硅灰石'),
								('C_CONT','定碳'),
								('SLAGTHICK','渣层厚度'),#1,8
								('SCRAPSTEEL','调温废钢'),#2,7
								('INSULATIONAGENT','保温剂(包)'),
								('TEMPOFARRIVE','进站温度(℃)'),#数据量少
								('TEMPOFDEPARTURE','出站温度(℃)'),
								])


PRO_BOF_HIS_ALLFIELDS_B=OrderedDict([

								('Event_3003','兑铁时间'),
								('Event_3004','兑废钢时间'),
								('Event_3001','处理开始时间'),
								('PUTSPRAYGUNTIME','下枪时间'),
								('TOTALTIMEOFOXYGEN','总供氧时间'),
								('BOTTOMBLOWING','底吹模式'),
								('TIMEOFOXYGEN','一倒供氧时间'),
								('Event_3002','处理结束时间'),
								('PERIOD','冶炼周期'),
								('Event_4003','通电开始时间'),
								('Event_4004','通电结束时间'),
								('STOVEHEATSNUM','补炉炉次'),
								('PITPATCHINGKIND','补炉炉次项目'),
								('D1_CHRGD_TIME','第1批加料时间'),
								('D1_CHRGD_TYPE','第1批加料类型'),
								('D2_CHRGD_TIME','第2批加料时间'),
								('D2_CHRGD_TYPE','第2批加料类型'),
								('D3_CHRGD_TIME','第3批加料时间'),
								('D3_CHRGD_TYPE','第3批加料类型'),
								('D4_CHRGD_TIME','第4批加料时间'),
								('D4_CHRGD_TYPE','第4批加料类型'),
								('D5_CHRGD_TIME','第5批加料时间'),
								('D5_CHRGD_TYPE','第5批加料类型'),
								('D6_CHRGD_TIME','第6批加料时间'),
								('D6_CHRGD_TYPE','第6批加料类型'),
								('D7_CHRGD_TIME','第7批加料时间'),
								('D7_CHRGD_TYPE','第7批加料类型'),
								('D8_CHRGD_TIME','第8批加料时间'),
								('D8_CHRGD_TYPE','第8批加料类型'),
								('D9_CHRGD_TIME','第9批加料时间'),
								('D9_CHRGD_TYPE','第9批加料类型'),
								('D10_CHRGD_TIME','第10批加料时间'),
								('D10_CHRGD_TYPE','第10批加料类型'),
								('D11_CHRGD_TIME','第11批加料时间'),
								('D11_CHRGD_TYPE','第11批加料类型'),
								('D12_CHRGD_TIME','第12批加料时间'),
								('D12_CHRGD_TYPE','第12批加料类型'),
								('D13_CHRGD_TIME','第13批加料时间'),
								('D13_CHRGD_TYPE','第13批加料类型'),
								('D14_CHRGD_TIME','第14批加料时间'),
								('D14_CHRGD_TYPE','第14批加料类型'),
								('D15_CHRGD_TIME','第15批加料时间'),
								('D15_CHRGD_TYPE','第15批加料类型'),
								('D16_CHRGD_TIME','第16批加料时间'),
								('D16_CHRGD_TYPE','第16批加料类型'),
								('D17_CHRGD_TIME','第17批加料类型'),
								('D18_CHRGD_TIME','第18批加料时间'),
								('D18_CHRGD_TYPE','第18批加料类型'),
								('D19_CHRGD_TIME','第19批加料时间'),
								('D19_CHRGD_TYPE','第19批加料类型'),
								('D20_CHRGD_TIME','第20批加料类型'),
								('D21_CHRGD_TIME','第21批加料时间'),
								('D21_CHRGD_TYPE','第21批加料类型'),
								('D22_CHRGD_TIME','第22批加料时间'),
								('D22_CHRGD_TYPE','第22批加料类型'),
								('D23_CHRGD_TIME','第23批加料时间'),
								('D23_CHRGD_TYPE','第23批加料类型'),
								('D24_CHRGD_TIME','第24批加料时间'),
								('D24_CHRGD_TYPE','第24批加料类型'),
								('D25_CHRGD_TIME','第25批加料时间'),
								('D25_CHRGD_TYPE','第25批加料类型'),
								('D26_CHRGD_TIME','第26批加料时间'),
								('D26_CHRGD_TYPE','第26批加料类型'),
								('D27_CHRGD_TIME','第27批加料时间'),
								('D27_CHRGD_TYPE','第27批加料类型'),
								('D28_CHRGD_TIME','第28批加料时间'),
								('D28_CHRGD_TYPE','第28批加料类型'),
								('D29_CHRGD_TIME','第29批加料时间'),
								('D29_CHRGD_TYPE','第29批加料类型'),
								('D30_CHRGD_TIME','第30批加料时间'),
								('D30_CHRGD_TYPE','第30批加料类型'),
								('D1_BOSTRT_TIME','第一次吹氧开始时间'),
								('D1_BOEND_TIME','第一次吹氧结束时间'),
								('D1_BO_DUR','第一次吹氧时间'),
								('D2_BOSTRT_TIME','第二次吹氧开始时间'),
								('D2_BOEND_TIME','第二次吹氧结束时间'),
								('D2_BO_DUR','第二次吹氧时间'),
								('D3_BOSTRT_TIME','第三次吹氧开始时间'),
								('D3_BOEND_TIME','第三次吹氧结束时间'),
								('D4_BOSTRT_TIME','第四次吹氧开始时间'),
								('D4_BOEND_TIME','第四次吹氧结束时间'),
								('D4_BO_DUR','第四次吹氧时间'),
								('D5_BOSTRT_TIME','第五次吹氧开始时间'),
								('D5_BOEND_TIME','第五次吹氧结束时间'),
								('D5_BO_DUR','第五次吹氧时间'),
								('D6_BOSTRT_TIME','第六次吹氧开始时间'),
								('D6_BOEND_TIME','第六次吹氧结束时间'),
								('D6_BO_DUR','第六次吹氧时间'),
								('D1_TEMP_TIME','第一次测温时间'),
								('D1_TEMP_TYPE','第一次测温位置'),
								('D1_TEMP_ACQ','第一次测温操作方式'),
								('D2_TEMP_TIME','第二次测温时间'),
								('D2_TEMP_TYPE','第二次测温位置'),
								('D2_TEMP_ACQ','第二次测温操作方式'),
								('D3_TEMP_TIME','第三次测温时间'),
								('D3_TEMP_TYPE','第三次测温位置'),
								('D3_TEMP_ACQ','第三次测温操作方式'),
								('D4_TEMP_TIME','第四次测温时间'),
								('D4_TEMP_TYPE','第四次测温位置'),
								('D4_TEMP_ACQ','第四次测温操作方式'),
								('D1_SAMP_TIME','第一次取样时间'),
								('D1_SAMP_TYPE','第一次取样类型'),
								('D2_SAMP_TIME','第二次取样时间'),
								('D2_SAMP_TYPE','第二次取样类型'),
								('D3_SAMP_TIME','第三次取样时间'),
								('D3_SAMP_TYPE','第三次取样类型'),
								('D4_SAMP_TIME','第四次取样时间'),
								('D4_SAMP_TYPE','第四次取样类型'),
								('D5_SAMP_TIME','第五次取样时间'),
								('D5_SAMP_TYPE','第五次取样类型'),

								('final_TEMP_NO','最后一次测温的序号'),
								('final_TEMP_TIME','最后一次测温时间'),
								('final_TEMP_VALUE','最终测温值'),
								('final_TEMP_TYPE','最后一次测温位置'),
								('final_TEMP_ACQ','最后一次测温操作方式'),

								('Event_3010','出钢开始'),
								('Event_3011','出钢结束'),
								('TIMEOFSLAGSPLISHING','溅渣护炉时间'),
								('Event_3012','溅渣开始'),
								('Event_3013','溅渣结束'),
								('OPERATETIME','吹氩时间(min)'),
								('ARRIVEDATE','进吹氩站日期'),
								('ARRIVETIME','进吹氩站时刻'),
								('DEPARTUREDATE','出吹氩站日期'),
								('DEPARTURETIME','出吹氩站时刻'),
						])
PRO_BOF_HIS_ALLFIELDS=OrderedDict([
								('FURNACESEQ','炉龄'),
								('SPRAYGUNSEQ','枪龄'),
								('MIRON_WGT','铁水重量'),
								('MIRON_TEMP','铁水温度'),
								('MIRON_C','铁水C含量'),
								('MIRON_SI','铁水SI含量'),
								('MIRON_MN','铁水MN含量'),
								('MIRON_P','铁水P含量'),
								('MIRON_S','铁水S含量'),
								('SCRAP_NUM','废钢数量'),
								('SCRAP_96053101','大渣钢'),
								('SCRAP_96052200','自产废钢'),
								('SCRAP_16010101','重型废钢'),
								('SCRAP_16020101','中型废钢'),
								('SCRAP_16030101','未知废钢'),
								('COLDPIGWGT','生铁装入量'),
								('SCRAPWGT','废钢装入量'),
								('SCRAPWGT_COUNT','废钢装入计算量'),
								('L96020400','1#烧结矿'),
								#('L12010301','石灰石_15-40mm'),
								('L12010302','石灰石_40-70mm'),
								('L12010601','萤石_FL80'),
								#('L12010701','硅灰石'),
								('L12020201','增碳剂'),
								('L12020301','低氮增碳剂'),
								('L96040100','石灰'),
								('L96040200','轻烧白云石'),
								('L96053601','钢渣'),
								('L1602010074','未知料'),
								('HEAT_WGT','炉重(KG)'),
								('BEFARTEMP','氩前温度'),
								('N2CONSUME','氮气耗量'),
								('TOTALOXYGENCONSUME','总供氧耗量'),
								('SUM_BO_CSM','总吹氧消耗'),
								('FIRSTCATCHOXYGENCONSUME','一倒氧气耗量'),
								('CARBONTEMPERATURE','一倒温度(℃)'),
								('FIRSTCATCHCARBONC','一倒C%'),
								('FIRSTCATCHCARBONP','一倒P%'),
								('DOWNFURNACETIMES','倒炉次数'),
								('SUBLANCE_AGE','副枪枪龄'),
								('SUBLANCE_INDEPTH','副枪插入深度'),
								('O_CONT','定氧'),
								#('C_CONT','定碳'),
								('LEQHEIGH','液面高度'),
								('D1_BO_CSM','第一次吹氧消耗'),
								('D2_BO_CSM','第二次吹氧消耗'),
								('D3_BO_CSM','第三次吹氧消耗'),
								('D4_BO_CSM','第四次吹氧消耗'),
								('D5_BO_CSM','第五次吹氧消耗'),
								('D6_BO_CSM','第六次吹氧消耗'),
								('D1_TEMP_VALUE','第一次测温值'),
								('D2_TEMP_VALUE','第二次测温值'),
								('D3_TEMP_VALUE','第三次测温值'),
								('D4_TEMP_VALUE','第四次测温值'),

								('STEELWGT_COUNT','出钢量1'),
								('TOTAL_SLAB_WGT','出钢量2'),
								('LDG_STEELWGT_COUNT','煤气发生量1'),
								('LDG_TOTAL_SLAB_WGT','煤气发生量2'),
								('STEEL_SLAG','钢渣量'),
								('C','C'),
								('SI','Si'),
								('MN','Mn'),
								('P','P'),
								('S','S'),
								('AL_T','Al_T'),
								('AL_S','Al_S'),
								('"AS"','AS'),
								('NI','Ni'),
								('CR','Cr'),
								('CU','Cu'),
								('MO','Mo'),
								('V','V'),
								('TI','Ti'),
								('NB','Nb'),
								('W','W'),
								('PB','Pb'),
								('SN','Sn'),
								('BI','Bi'),
								('B','B'),
								('CA','Ca'),
								('N','N'),
								('CO','Co'),
								('ZR','Zr'),
								('CE','Ce'),
								('FE','Fe'),

								('L13010101','硅铁_Si72-80%、AL≤2%(粒度10-60mm)'),
								('L13010301','微铝硅铁_Si 72-80%、AL≤0.1%、Ti≤0.1%'),
								('L13020101','硅锰合金_Mn 65-72%、Si 17-20%'),
								('L13020201','高硅硅锰_Mn ≥60%、Si ≥27%'),
								('L13040400','中碳铬铁'),
								('SCRAP_16040101','破碎废钢'),
								('SCRAP_96052501','小渣钢'),
								('RETURNSTEELWEIGHT','回炉钢液量'),
								('LADLESTATUS','包况'),
								('LADLEAGE','包龄'),
								('L12010301','石灰石_15-40mm'),
								('L12010701','硅灰石'),
								('C_CONT','定碳'),
								('SLAGTHICK','渣层厚度'),#1,8
								('SCRAPSTEEL','调温废钢'),#2,7
								('INSULATIONAGENT','保温剂(包)'),
								('TEMPOFARRIVE','进站温度(℃)'),#数据量少
								('TEMPOFDEPARTURE','出站温度(℃)'),

								('EVENT_3003','兑铁时间'),
								('EVENT_3004','兑废钢时间'),
								('EVENT_3001','处理开始时间'),
								('PUTSPRAYGUNTIME','下枪时间'),
								('TOTALTIMEOFOXYGEN','总供氧时间'),
								('BOTTOMBLOWING','底吹模式'),
								('TIMEOFOXYGEN','一倒供氧时间'),
								('EVENT_3002','处理结束时间'),
								('PERIOD','冶炼周期'),
								('EVENT_4003','通电开始时间'),
								('EVENT_4004','通电结束时间'),
								('STOVEHEATSNUM','补炉炉次'),
								('PITPATCHINGKIND','补炉炉次项目'),
								('D1_CHRGD_TIME','第1批加料时间'),
								('D1_CHRGD_TYPE','第1批加料类型'),
								('D2_CHRGD_TIME','第2批加料时间'),
								('D2_CHRGD_TYPE','第2批加料类型'),
								('D3_CHRGD_TIME','第3批加料时间'),
								('D3_CHRGD_TYPE','第3批加料类型'),
								('D4_CHRGD_TIME','第4批加料时间'),
								('D4_CHRGD_TYPE','第4批加料类型'),
								('D5_CHRGD_TIME','第5批加料时间'),
								('D5_CHRGD_TYPE','第5批加料类型'),
								('D6_CHRGD_TIME','第6批加料时间'),
								('D6_CHRGD_TYPE','第6批加料类型'),
								('D7_CHRGD_TIME','第7批加料时间'),
								('D7_CHRGD_TYPE','第7批加料类型'),
								('D8_CHRGD_TIME','第8批加料时间'),
								('D8_CHRGD_TYPE','第8批加料类型'),
								('D9_CHRGD_TIME','第9批加料时间'),
								('D9_CHRGD_TYPE','第9批加料类型'),
								('D10_CHRGD_TIME','第10批加料时间'),
								('D10_CHRGD_TYPE','第10批加料类型'),
								('D11_CHRGD_TIME','第11批加料时间'),
								('D11_CHRGD_TYPE','第11批加料类型'),
								('D12_CHRGD_TIME','第12批加料时间'),
								('D12_CHRGD_TYPE','第12批加料类型'),
								('D13_CHRGD_TIME','第13批加料时间'),
								('D13_CHRGD_TYPE','第13批加料类型'),
								('D14_CHRGD_TIME','第14批加料时间'),
								('D14_CHRGD_TYPE','第14批加料类型'),
								('D15_CHRGD_TIME','第15批加料时间'),
								('D15_CHRGD_TYPE','第15批加料类型'),
								('D16_CHRGD_TIME','第16批加料时间'),
								('D16_CHRGD_TYPE','第16批加料类型'),
								('D17_CHRGD_TIME','第17批加料类型'),
								('D18_CHRGD_TIME','第18批加料时间'),
								('D18_CHRGD_TYPE','第18批加料类型'),
								('D19_CHRGD_TIME','第19批加料时间'),
								('D19_CHRGD_TYPE','第19批加料类型'),
								('D20_CHRGD_TIME','第20批加料类型'),
								('D21_CHRGD_TIME','第21批加料时间'),
								('D21_CHRGD_TYPE','第21批加料类型'),
								('D22_CHRGD_TIME','第22批加料时间'),
								('D22_CHRGD_TYPE','第22批加料类型'),
								('D23_CHRGD_TIME','第23批加料时间'),
								('D23_CHRGD_TYPE','第23批加料类型'),
								('D24_CHRGD_TIME','第24批加料时间'),
								('D24_CHRGD_TYPE','第24批加料类型'),
								('D25_CHRGD_TIME','第25批加料时间'),
								('D25_CHRGD_TYPE','第25批加料类型'),
								('D26_CHRGD_TIME','第26批加料时间'),
								('D26_CHRGD_TYPE','第26批加料类型'),
								('D27_CHRGD_TIME','第27批加料时间'),
								('D27_CHRGD_TYPE','第27批加料类型'),
								('D28_CHRGD_TIME','第28批加料时间'),
								('D28_CHRGD_TYPE','第28批加料类型'),
								('D29_CHRGD_TIME','第29批加料时间'),
								('D29_CHRGD_TYPE','第29批加料类型'),
								('D30_CHRGD_TIME','第30批加料时间'),
								('D30_CHRGD_TYPE','第30批加料类型'),
								('D1_BOSTRT_TIME','第一次吹氧开始时间'),
								('D1_BOEND_TIME','第一次吹氧结束时间'),
								('D1_BO_DUR','第一次吹氧时间'),
								('D2_BOSTRT_TIME','第二次吹氧开始时间'),
								('D2_BOEND_TIME','第二次吹氧结束时间'),
								('D2_BO_DUR','第二次吹氧时间'),
								('D3_BOSTRT_TIME','第三次吹氧开始时间'),
								('D3_BOEND_TIME','第三次吹氧结束时间'),
								('D4_BOSTRT_TIME','第四次吹氧开始时间'),
								('D4_BOEND_TIME','第四次吹氧结束时间'),
								('D4_BO_DUR','第四次吹氧时间'),
								('D5_BOSTRT_TIME','第五次吹氧开始时间'),
								('D5_BOEND_TIME','第五次吹氧结束时间'),
								('D5_BO_DUR','第五次吹氧时间'),
								('D6_BOSTRT_TIME','第六次吹氧开始时间'),
								('D6_BOEND_TIME','第六次吹氧结束时间'),
								('D6_BO_DUR','第六次吹氧时间'),
								('D1_TEMP_TIME','第一次测温时间'),
								('D1_TEMP_TYPE','第一次测温位置'),
								('D1_TEMP_ACQ','第一次测温操作方式'),
								('D2_TEMP_TIME','第二次测温时间'),
								('D2_TEMP_TYPE','第二次测温位置'),
								('D2_TEMP_ACQ','第二次测温操作方式'),
								('D3_TEMP_TIME','第三次测温时间'),
								('D3_TEMP_TYPE','第三次测温位置'),
								('D3_TEMP_ACQ','第三次测温操作方式'),
								('D4_TEMP_TIME','第四次测温时间'),
								('D4_TEMP_TYPE','第四次测温位置'),
								('D4_TEMP_ACQ','第四次测温操作方式'),
								('D1_SAMP_TIME','第一次取样时间'),
								('D1_SAMP_TYPE','第一次取样类型'),
								('D2_SAMP_TIME','第二次取样时间'),
								('D2_SAMP_TYPE','第二次取样类型'),
								('D3_SAMP_TIME','第三次取样时间'),
								('D3_SAMP_TYPE','第三次取样类型'),
								('D4_SAMP_TIME','第四次取样时间'),
								('D4_SAMP_TYPE','第四次取样类型'),
								('D5_SAMP_TIME','第五次取样时间'),
								('D5_SAMP_TYPE','第五次取样类型'),

								('FINAL_TEMP_NO','最后一次测温的序号'),
								('FINAL_TEMP_TIME','最后一次测温时间'),
								('FINAL_TEMP_VALUE','最终测温值'),
								('FINAL_TEMP_TYPE','最后一次测温位置'),
								('FINAL_TEMP_ACQ','最后一次测温操作方式'),

								('EVENT_3010','出钢开始'),
								('EVENT_3011','出钢结束'),
								('TIMEOFSLAGSPLISHING','溅渣护炉时间'),
								('EVENT_3012','溅渣开始'),
								('EVENT_3013','溅渣结束'),
								('OPERATETIME','吹氩时间(min)'),
								('ARRIVEDATE','进吹氩站日期'),
								('ARRIVETIME','进吹氩站时刻'),
								('DEPARTUREDATE','出吹氩站日期'),
								('DEPARTURETIME','出吹氩站时刻'),
								('STEELWGT','出钢量'),
								('SUM_BO_DUR','总吹氧时间_计算'),
						        ('D3_BO_DUR','第三次吹氧时间'),
						        ('LDG_STEELWGT','煤气发生量'),
						        ('L13020501','中碳锰铁_Mn78.0-85.0%, C≤1.0%'),
						])

PRO_BOF_HIS_ALLFIELDS_SCORE=dict([

								('FURNACESEQ',('炉龄',1)),
								('SPRAYGUNSEQ',('枪龄',2)),
								('MIRON_WGT',('铁水重量',3)),
								('MIRON_TEMP',('铁水温度',4)),
								('MIRON_C',('铁水C含量',5)),
								('MIRON_SI',('铁水SI含量',6)),
								('MIRON_MN',('铁水MN含量',7)),
								('MIRON_P',('铁水P含量',8)),
								('MIRON_S',('铁水S含量',9)),
								('SCRAP_NUM',('废钢数量',10)),
								('SCRAP_96053101',('大渣钢',11)),
								('SCRAP_96052200',('自产废钢',12)),
								('SCRAP_16010101',('重型废钢',13)),
								('SCRAP_16020101',('中型废钢',14)),
								('SCRAP_16030101',('未知废钢',15)),
								('COLDPIGWGT',('生铁装入量',16)),
								('SCRAPWGT',('废钢装入量',17)),
								('SCRAPWGT_COUNT',('废钢装入计算量',18)),
								('L96020400',('1#烧结矿',19)),
								#('L12010301','石灰石_15-40mm'),
								('L12010302',('石灰石_40-70mm',20)),
								('L12010601',('萤石_FL80',21)),
								#('L12010701','硅灰石'),
								('L12020201',('增碳剂',22)),
								('L12020301',('低氮增碳剂',23)),
								('L96040100',('石灰',24)),
								('L96040200',('轻烧白云石',25)),
								('L96053601',('钢渣',26)),
								('L1602010074',('未知料',27)),
								('HEAT_WGT',('炉重(KG)',28)),
								('BEFARTEMP',('氩前温度',29)),
								('N2CONSUME',('氮气耗量',30)),
								('TOTALOXYGENCONSUME',('总供氧耗量',31)),
								('SUM_BO_CSM',('总吹氧消耗',32)),
								('FIRSTCATCHOXYGENCONSUME',('一倒氧气耗量',33)),
								('CARBONTEMPERATURE',('一倒温度(℃)',34)),
								('FIRSTCATCHCARBONC',('一倒C%',35)),
								('FIRSTCATCHCARBONP',('一倒P%',36)),
								('DOWNFURNACETIMES',('倒炉次数',37)),
								('SUBLANCE_AGE',('副枪枪龄',38)),
								('SUBLANCE_INDEPTH',('副枪插入深度',39)),
								('O_CONT',('定氧',40)),
								#('C_CONT','定碳'),
								('LEQHEIGH',('液面高度',41)),
								('D1_BO_CSM',('第一次吹氧消耗',42)),
								('D2_BO_CSM',('第二次吹氧消耗',43)),
								('D3_BO_CSM',('第三次吹氧消耗',44)),
								('D4_BO_CSM',('第四次吹氧消耗',45)),
								('D5_BO_CSM',('第五次吹氧消耗',46)),
								('D6_BO_CSM',('第六次吹氧消耗',47)),
								('D1_TEMP_VALUE',('第一次测温值',48)),
								('D2_TEMP_VALUE',('第二次测温值',49)),
								('D3_TEMP_VALUE',('第三次测温值',50)),
								('D4_TEMP_VALUE',('第四次测温值',51)),

								('STEELWGT_COUNT',('出钢量1',52)),
								('TOTAL_SLAB_WGT',('出钢量2',53)),
								('LDG_STEELWGT_COUNT',('煤气发生量1',54)),
								('LDG_TOTAL_SLAB_WGT',('煤气发生量2',55)),
								('STEEL_SLAG',('钢渣量',56)),
								('C',('C',57)),
								('SI',('Si',58)),
								('MN',('Mn',59)),
								('P',('P',60)),
								('S',('S',61)),
								('AL_T',('Al_T',62)),
								('AL_S',('Al_S',63)),
								('"AS"',('AS',64)),
								('NI',('Ni',65)),
								('CR',('Cr',66)),
								('CU',('Cu',67)),
								('MO',('Mo',68)),
								('V',('V',69)),
								('TI',('Ti',70)),
								('NB',('Nb',71)),
								('W',('W',72)),
								('PB',('Pb',73)),
								('SN',('Sn',74)),
								('BI',('Bi',75)),
								('B',('B',76)),
								('CA',('Ca',77)),
								('N',('N',78)),
								('CO',('Co',79)),
								('ZR',('Zr',80)),
								('CE',('Ce',81)),
								('FE',('Fe',82)),

								('L13010101',('硅铁_Si72-80%、AL≤2%(粒度10-60mm)',83)),
								('L13010301',('微铝硅铁_Si 72-80%、AL≤0.1%、Ti≤0.1%',84)),
								('L13020101',('硅锰合金_Mn 65-72%、Si 17-20%',85)),
								('L13020201',('高硅硅锰_Mn ≥60%、Si ≥27%',86)),
								('L13040400',('中碳铬铁',87)),
								('SCRAP_16040101',('破碎废钢',88)),
								('SCRAP_96052501',('小渣钢',89)),
								('RETURNSTEELWEIGHT',('回炉钢液量',90)),
								('LADLESTATUS',('包况',91)),
								('LADLEAGE',('包龄',92)),
								('L12010301',('石灰石_15-40mm',93)),
								('L12010701',('硅灰石',94)),
								('C_CONT',('定碳',95)),
								('SLAGTHICK',('渣层厚度',96)),#1,8
								('SCRAPSTEEL',('调温废钢',97)),#2,7
								('INSULATIONAGENT',('保温剂(包)',98)),
								('TEMPOFARRIVE',('进站温度(℃)',99)),#数据量少
								('TEMPOFDEPARTURE',('出站温度(℃)',100)),

								('EVENT_3003',('兑铁时间',101)),
								('EVENT_3004',('兑废钢时间',102)),
								('EVENT_3001',('处理开始时间',103)),
								('PUTSPRAYGUNTIME',('下枪时间',104)),
								('TOTALTIMEOFOXYGEN',('总供氧时间',105)),
								('BOTTOMBLOWING',('底吹模式',106)),
								('TIMEOFOXYGEN',('一倒供氧时间',107)),
								('EVENT_3002',('处理结束时间',108)),
								('PERIOD',('冶炼周期',109)),
								('EVENT_4003',('通电开始时间',110)),
								('EVENT_4004',('通电结束时间',111)),
								('STOVEHEATSNUM',('补炉炉次',112)),
								('PITPATCHINGKIND',('补炉炉次项目',113)),
								('D1_BOSTRT_TIME',('第一次吹氧开始时间',114)),
								('D1_BOEND_TIME',('第一次吹氧结束时间',115)),
								('D1_BO_DUR',('第一次吹氧时间',116)),
								('D2_BOSTRT_TIME',('第二次吹氧开始时间',117)),
								('D2_BOEND_TIME',('第二次吹氧结束时间',118)),
								('D2_BO_DUR',('第二次吹氧时间',119)),
								('D3_BOSTRT_TIME',('第三次吹氧开始时间',120)),
								('D3_BOEND_TIME',('第三次吹氧结束时间',121)),
								('D4_BOSTRT_TIME',('第四次吹氧开始时间',121)),
								('D4_BOEND_TIME',('第四次吹氧结束时间',122)),
								('D4_BO_DUR',('第四次吹氧时间',123)),
								('D5_BOSTRT_TIME',('第五次吹氧开始时间',124)),
								('D5_BOEND_TIME',('第五次吹氧结束时间',125)),
								('D5_BO_DUR',('第五次吹氧时间',126)),
								('D6_BOSTRT_TIME',('第六次吹氧开始时间',127)),
								('D6_BOEND_TIME',('第六次吹氧结束时间',128)),
								('D6_BO_DUR',('第六次吹氧时间',129)),
								('D1_TEMP_TIME',('第一次测温时间',130)),
								('D1_TEMP_TYPE',('第一次测温位置',131)),
								('D1_TEMP_ACQ',('第一次测温操作方式',132)),
								('D2_TEMP_TIME',('第二次测温时间',133)),
								('D2_TEMP_TYPE',('第二次测温位置',134)),
								('D2_TEMP_ACQ',('第二次测温操作方式',135)),
								('D3_TEMP_TIME',('第三次测温时间',136)),
								('D3_TEMP_TYPE',('第三次测温位置',137)),
								('D3_TEMP_ACQ',('第三次测温操作方式',138)),
								('D4_TEMP_TIME',('第四次测温时间',139)),
								('D4_TEMP_TYPE',('第四次测温位置',140)),
								('D4_TEMP_ACQ',('第四次测温操作方式',141)),
								('D1_SAMP_TIME',('第一次取样时间',142)),
								('D1_SAMP_TYPE',('第一次取样类型',145)),
								('D2_SAMP_TIME',('第二次取样时间',146)),
								('D2_SAMP_TYPE',('第二次取样类型',147)),
								('D3_SAMP_TIME',('第三次取样时间',148)),
								('D3_SAMP_TYPE',('第三次取样类型',149)),
								('D4_SAMP_TIME',('第四次取样时间',150)),
								('D4_SAMP_TYPE',('第四次取样类型',151)),
								('D5_SAMP_TIME',('第五次取样时间',152)),
								('D5_SAMP_TYPE',('第五次取样类型',153)),

								('FINAL_TEMP_NO',('最后一次测温的序号',154)),
								('FINAL_TEMP_TIME',('最后一次测温时间',155)),
								('FINAL_TEMP_VALUE',('最终测温值',156)),
								('FINAL_TEMP_TYPE',('最后一次测温位置',157)),
								('FINAL_TEMP_ACQ',('最后一次测温操作方式',158)),

								('EVENT_3010',('出钢开始',159)),
								('EVENT_3011',('出钢结束',160)),
								('TIMEOFSLAGSPLISHING',('溅渣护炉时间',161)),
								('EVENT_3012',('溅渣开始',162)),
								('EVENT_3013',('溅渣结束',163)),
								('OPERATETIME',('吹氩时间(min)',164)),
								('ARRIVEDATE',('进吹氩站日期',165)),
								('ARRIVETIME',('进吹氩站时刻',166)),
								('DEPARTUREDATE',('出吹氩站日期',167)),
								('DEPARTURETIME',('出吹氩站时刻',168)),
						])
