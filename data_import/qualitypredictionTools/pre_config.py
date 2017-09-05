from django.conf import settings
import pandas as pd

media_root = settings.MEDIA_ROOT
data_root = media_root + 'files/data/'
path_lf = data_root + 'LF_test3.csv'
data = pd.read_csv(path_lf, encoding = 'gbk')
heatno = {}
for i in range(len(data['HEAT_NO'])):
    heatno[data['HEAT_NO'][i]] =data['HEAT_NO'][i]

lf_type = {
	"temp":"LF温度",
	"C":"C含量",
	"S":"S含量",
	"O":"O含量",
}
predict_method = {
	"logistic_regression":"逻辑回归",
	"random_forest":"随机森林",
	"elm":"超限学习机elm",
	"svm":"支持向量机svm",
}
# time_scale = {
# 	"day":"日",
# 	"month":"月",
# }
yinsu_type = {
	"tkszs":"铁矿石指数",
	"psjgzs":"普氏价格指数",
	"meiyuan_zhishu":"美元指数",
	"tegang_zonghe_zhishu":"特钢综合指数",
	"gangtie_cugang":"粗钢指数",
	"gangtie_gangcai":"钢材指数",
	"pugang_zhishu":"普刚指数",
	"haiyun_BDI":"波罗的海指数",
	"haiyun_BDTI":"波罗的海原油指数",
	"WTI":"WTI原油价格",
}
