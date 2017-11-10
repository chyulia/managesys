#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
steel_type = {
    "tanhuang": "弹簧钢",
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

INFO = "描述信息：以2017年9月以前的历史数据外延预测2017年9月之后的价格数据。"
ELE_INFOS = {
    'steel':"描述信息：数据爬取自<a href='http://search.mysteel.com/market/list.ms'>我的钢铁</a>",
    'WTI':"描述信息：数据爬取自<a href='http://index.mysteel.com/data/#0402-1'>我的钢铁</a>",
    'feigang':"描述信息：数据爬取自<a href='http://www.96369.net/Indices/78'>西本新干线</a>",
    'tkszs_qdg':"描述信息：数据爬取自<a href='http://index.glinfo.com/xpic/detail.ms?tabName=kuangsi'>我的钢铁</a>",
    'tegang_zonghe_zhishu':"描述信息：数据爬取自<a href='http://index.glinfo.com/xpic/detail.ms?tabName=kuangsi'>我的钢铁</a>",
    'meiyuan':"描述信息：数据爬取自<a href='https://cn.investing.com/quotes/us-dollar-index-historical-data'>investing.com</a>",
    'psjgzs':"描述信息：数据爬取自<a href='http://www.96369.net/Indices/125'>西本新干线</a>",
    'haiyun_BDI':"描述信息：数据爬取自<a href='http://index.glinfo.com/data/#0403-1'>我的钢铁</a>",
    'haiyun_BDTI':"描述信息：数据爬取自<a href='http://index.glinfo.com/data/#0403-1'>我的钢铁</a>",
    'pugang_zhishu':"描述信息：数据爬取自<a href='http://index.mysteel.com/xpic/detail.ms?tabName=pugang'>我的钢铁</a>",
}
"""
<select class="form-control input-lg" id="yinsu_type" name="yinsu_type" placeholder="铁矿石价格因素">
  <option value="WTI">WTI原油价格</option>
  <option value="feigang">废钢价格</option>
  <option value="tkszs_qdg">铁矿石指数</option>
  <option value="tegang_zonghe_zhishu">特钢综合指数</option>
  <option value="meiyuan">美元指数</option>
  <option value="psjgzs">普氏价格指数</option>
  <option value="haiyun_BDTI">波罗的海原油指数</option>
  <option value="haiyun_BDI">波罗的海指数</option>
  <option value="pugang_zhishu">普刚指数</option>
</select>
"""
WARNING = "数据处理耗时较长，请耐心等待..."

model_classname = {
    "ExtremeLM": "ExtremeLM",
    "SVR_": "SVR_",
    "RandomForest": "RandomForest",
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

search_advice = {
    "22A":"""22A 天津 邢钢 Φ6.5-20 <br/>
22A 天津 荣钢 Φ6.5 <br/>""",
    "35K":"""
35K 温州 安钢 Φ6.5-20 <br/>
35K 温州 马钢 Φ6.5-16 <br/>
35K 宁波 沙钢 Φ16-24 <br/>
35K 宁波 沙钢 Φ26-30 <br/>
35K 海盐 沙钢 Φ16-24 <br/>
""",
    "ML08AL":"""
ML08AL 海盐 沙钢 Φ16-24 <br/>
""",
    "45K":"""
45K 海盐 沙钢 Φ16-24 <br/>
""",
    "20MnTiB":"",
    "65Mn":"""
65Mn 全国 济源钢铁 Φ5.5<br/>
65Mn 全国 济源钢铁 Φ6.5-20<br/>
65Mn 全国 安钢 Φ6.5-20<br/>
65Mn 全国 鞍钢 Φ6.5-25<br/>
65Mn 全国 宝钢 Φ6.5-26<br/>
65Mn 全国 沙钢 Φ10-12<br/>
""",
    "Si2Mn":"""
   
60Si2MnA 全国 济源钢铁 Φ6.5-20<br/>
60Si2MnA 全国 鞍钢 Φ6.5-25<br/>
60Si2MnA 全国 宝钢 Φ6.5-26<br/>
60Si2CrA 全国 宝钢 Φ6.5-26<br/>
 """,
    "50CrVA":"""
50CrVA 全国 中天钢铁 Φ50-130<br/>
""",
    "55SiCrA":"""
55SiCrA 全国 安钢 Φ6.5-20<br/>
55SiCrA 全国 宝钢 Φ6.5-26<br/>
55SiCrA 全国 沙钢 Φ5.5-20<br/>
55SiCrA 全国 济源 Φ6.5-20<br/>
"""
}