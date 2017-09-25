#工作站
db_host = '202.204.54.212'
db_user = 'qg_user'
db_password = '123456'
db_name = 'orcl'
db_port = 1521



#单炉次
#单炉次进行追溯的偏离阈值
single_doretrospect=0.2
#对字段偏离程度的定性判断：表示-0.2~0.2为正常，±（0.2~0.35）为偏高/低，>0.35或<-0.35为高/低
qualitative_standard=[0.2,0.35]
#雷达图中期望上下范围的对比
updesired=1.2#上范围
downdesired=0.8#下范围


#多炉次波动率
#多炉次进行追溯的偏离阈值
fluc_doretrospect=0.05
#对分析字段偏离程度进行定性判断：表示<0为理想，0~0.05为正常，0.05~0.1为偏高，>0.1为高
qualitative_standard_anafield=[0.05,0.1]
#追溯时对影响字段的定性判断：表示<0为理想，0~0.01为正常，0.01~0.05为偏高，>0.0.05为高
qualitative_standard_influcfield=[0.01,0.05]











