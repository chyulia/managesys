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
time_scale = {
	"day":"日",
	"week":"周",
	"halfmonth":"半月",
	"month":"月",
	"threemonth":"季度",
	"halfyear":"半年",
	"year":"年",
}

INFO = "描述信息：以2016年1月以前的历史数据外延预测2016年1月之后的价格数据。"

WARNING = "数据处理耗时较长，请耐心等待..."

model_classname = {
	"elm":"ExtremeLM",
	"svm":"SVM",
	"BP":"BP",
	"linear_regression":"LR",
	"random_forest":"RandomForest",
}
