#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
steel_type = {
    "1": "弹簧钢",
    # "2": "冷墩拉丝",
}
predict_method = {
    "RandomForest": "随机森林",
    "ExtremeLM": "超限学习机elm",
    "SVR_": "支持向量回归svr",
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
ELE_INFOS = {
    'steel':"描述信息：数据爬取自<a href='http://search.mysteel.com/market/list.ms'>我的钢铁</a>",
}

WARNING = "数据处理耗时较长，请耐心等待..."

model_classname = {
    "elm": "ExtremeLM",
    "svm": "SVM",
    "BP": "BP",
    "linear_regression": "LR",
    "random_forest": "RandomForest",
}

# 铁矿石参数
iron_type = {
    "tkszs": "铁矿石指数",
    "price_qingdao": "到岸价",
}
stone_predict_method = {
    "logistic_regression": "逻辑回归",
    "random_forest": "随机森林",
    "elm": "超限学习机elm",
    "svm": "支持向量机svm",
}
time_scale = {
    # "day": "日",
    "month": "月",
}

yinsu_type = {
    "tkszs_qdg": "铁矿石指数",
    "psjgzs": "普氏价格指数",
    "meiyuan": "美元指数",
    "tegang_zonghe_zhishu": "特钢综合指数",
    "pugang_zhishu": "普刚指数",
    "haiyun_BDI": "波罗的海指数",
    "haiyun_BDTI": "波罗的海原油指数",
    "feigang": "废钢价格",
    "WTI": "WTI原油价格",
}

choose_col_meaning = {
    'steeltype': '钢材种类（小类）',
    'tradeno': '钢材牌号',
    'delivery': '工艺',
    'specification': '规格',
    'factory': '工厂',
    'region': '地区'
}

all_select = {'delivery': ['热轧'],
              'factory': ['济源钢铁','安钢','鞍钢','宝钢','沙钢','南钢','邢钢','中天','中天钢铁','邢台','济源'],
              'region': ['全国'],
              'specification': ['Φ5.5','Φ6.5-20','Φ6.5-25','Φ6.5-26','Φ10-12','Φ6.5-12','Φ5.5-14','Φ13-180','Φ5.5-16',
                                'Φ6.5-14','Φ6.5-15.5','Φ50-130','Φ5.5-20'],
              'steeltype': ['弹簧钢'],
              'tradeno': ['65Mn', '60Si2Mn', '60Si2MnA', '60Si2CrA', '50CrVA', '55SiCrA']
              },
"""
 ('steeltype', 'tradeno', 'delivery', 'specification', 'factory', 'region')
"""

# 生成原始数据集
table_name = ['tkszs', 'meiyuan', 'steelprice', 'meitan_ljm', 'jkk_qingdao', 'fgzs', 'gtcl'] # 'tiejingfen'
table_name_all = ['rmbmyhl', 'CRU', 'jkk_qingdao_1', 'tksykcl', 'lwgcl', 'tegang_ yougang', 'wymzs', 'psjgzs',
                  'cugangyuedu', 'ljmzs', 'steelprice', 'tegang_buxiugang', 'PMI', 'PPI', 'gdzctz', 'pugang', 'dlmzs',
                  'tksjkl', 'fdctz', 'haiyun_oto', 'pcmzs', 'gyzzz', 'jtzs', 'haiyun', 'meitan_wym', 'xgxjtzs', 'CPI',
                  'M2', 'gtcl', 'meiyuan', 'jkk_qingdao', 'tegang_zonghe', 'WTI', 'tegang_tegang', 'meitan_ljm', 'fgzs',
                  'meitan_dlm']
table_name_meanings = {
    'jkk_qingdao': '青岛港进口矿现货',
    'jkk_qingdao_1': '青岛港进口矿现货价格',
    'steelprice': '各牌号钢材价格',
    'meitan_wym': '日照港喷吹无烟煤价格',
    'meitan_dlm': '山东动力煤价格',
    'meitan_ljm': '炼焦煤价格表',
    'xgxjtzs': '新干线焦炭指数',
    'WTI': 'WTI原油价格',
    'haiyun': '油轮海运指数',
    'meiyuan': '美元指数',
    'PMI': 'PMI指数',
    'psjgzs': '普氏价格指数',
    'tksykcl': '铁矿石原矿产量',
    'tksjkl': '铁矿石进口量',
    'gtcl': '钢铁产量',
    'pugang': '钢铁普刚指数',
    'tegang_zonghe': '特铁综合指数',
    'tegang_tegang': '特铁特钢指数',
    'tegang_ yougang': '特铁优刚指数',
    'tegang_buxiugang': '特铁不锈刚指数表',
    'lwgcl': '螺纹钢产量表',
    'CPI': 'CPI指数',
    'wymzs': '无烟煤指数表',
    'dlmzs': '动力煤指数',
    'pcmzs': '喷吹煤指数表',
    'ljmzs': '炼焦煤指数',
    'jtzs': '焦炭指数',
    'haiyun_oto': '海运运费',
    'fgzs': '废钢指数',
    'fdctz': '房地产资产投资额（月度）',
    'gdzctz': '固定资产投资额（月度）',
    'cugangyuedu': '全球粗钢月度产量',
    'gyzzz': '规模以上工业增加值（月度）',
    'rmbmyhl': '广义人民币名义有效汇率(ER)(月度)',
    'PPI': '生产者价格指数(PPI)、（每月）',
    'M2': '货币和准货币（M2）（月度）',
    'CRU': '国际钢铁综合价格指数(CRU)（月度）',
}
price_field = {
    'tkszs': 'tkszs_qdg',
    'meiyuan': 'meiyuan_zhishu',
    'steelprice': 'price',
    'meitan_ljm': 'coal_ljm_jiage',
    'jkk_qingdao': 'jkk_jizhunjia',
    'fgzs': 'fgzs_zhi',
    'gtcl': 'gangtie_gangcai',
}

time_fields = {
    'tkszs':'tkszs_date',
    'meiyuan':'meiyuan_date',
    'steelprice':'updatetime',
    'meitan_ljm':'coal_ljm_date',
    'jkk_qingdao':'jkk_date',
    'fgzs':'fgzs_date',
    'gtcl':'gangtie_date',
}