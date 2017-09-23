# -*- coding: utf-8 -*-
steel_type = {
	"2501":"2501",
	"60Si2Mn":"60Si2Mn",
	"C82A":"C82A",
}
predict_method = {
	"linear_regression":"线性回归",
	"random_forest":"随机森林",
	"elm":"超限学习机elm",
	"svm":"支持向量机svm",
	# "BP":"BP神经网络",
}
# time_scale = {
# 	"day":"日",
# 	"week":"周",
# 	"halfmonth":"半月",
# 	"month":"月",
# 	"threemonth":"季度",
# 	"halfyear":"半年",
# 	"year":"年",
# }

INFO = "描述信息：以2016年1月以前的历史数据外延预测2016年1月之后的价格数据。"

WARNING = "数据处理耗时较长，请耐心等待..."

model_classname = {
	"elm":"ExtremeLM",
	"svm":"SVM",
	"BP":"BP",
	"linear_regression":"LR",
	"random_forest":"RandomForest",
}

# 铁矿石参数
iron_type = {
	"tkszs":"铁矿石指数",
	"price_qingdao":"到岸价",
}
stone_predict_method = {
	"logistic_regression":"逻辑回归",
	"random_forest":"随机森林",
	"elm":"超限学习机elm",
	"svm":"支持向量机svm",
}
time_scale = {
	"day":"日",
	"month":"月",
}


yinsu_type = {
 "tkszs_qdg":"铁矿石指数",
 "psjgzs":"普氏价格指数",
 "meiyuan":"美元指数",
 "tegang_zonghe_zhishu":"特钢综合指数",
 "pugang_zhishu":"普刚指数",
 "haiyun_BDI":"波罗的海指数",
 "haiyun_BDTI":"波罗的海原油指数",
 "feigang":"废钢价格",
 "WTI":"WTI原油价格",
}