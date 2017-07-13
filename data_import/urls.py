from django.conf.urls import url, include
from . import views
from . import chyulia
from . import fluc_chyulia
from . import hashuang
from data_import.SteelPricePredict import steelprice
from . import qualityzhuanlu
from . import fluc_quality
from . import batchprocess
from . import ironstoneprice
from . import violent_analyse

urlpatterns = [
    #需要对相同业务的加载与处理写一个分发器
    url(r'^$', views.home),
    url(r'^index$', views.home),
    url(r'^module_nav$', views.module_nav),
    #用户登录
    url(r'^login$',views.user_login),
    #用户注册
    url(r'^register$', views.user_register),
    #用户登出
    url(r'^logout$',views.user_logout),
    #修改密码
    url(r'^modify_password$', views.modify_password),
    #项目控制
    url(r'^(?P<slug>[-\w\d]+),(?P<post_id>\d+)/$', views.contentpost),
    url(r'^summary$', views.summary),
    url(r'^tasks$', views.tasks),
    url(r'^advices$',views.advices),
    url(r'^shares$',views.shares),
    #数据迁移
    url(r'^data_import$', views.data_import),
    # url(r'^multikey_data_import', views.multikey_data_import),
    #文件
    url(r'^upload_file$',views.upload_file),
    url(r'^load_procedure_name$',views.load_procedure_name),
    url(r'^ana_data_lack$',views.ana_data_lack),
    url(r'^download_file$',views.download_file),

    #重置密码
    url(r'^reset_password$',views.reset_password),
    url(r'^success$',views.success),
    #
    url(r'^ajaxtest$',views.ajaxtest),
    #功能测试
    url(r'^delete$',views.delete_records),
    url(r'^functionDemo$',views.functionDemo),

    #echarts展示示例
    url(r'^echarts$',views.echarts),
    #sinuo
    #显示分析页面
    url(r'^space',views.space),
    url(r'^time',views.time),
    url(r'^trade',views.trade),
    url(r'^cust_time',views.cust_time),
    url(r'^cust_trade',views.cust_trade),
    url(r'^liusinuo',views.space),
    url(r'^stockControl',views.stockControl),
    url(r'^market_share',views.market_share),
    #钢种自动加载
    url(r'^GetTradeNo',views.getAllTradeNo_time),
    #数据仓库更新
    url(r'^update_mysql_space',views.update_mysql_space),


    #ha
    #显示统计分析页面
    url(r'^ha', hashuang.ha),
    #按表结构加载下拉框
    url(r'^lond_to',hashuang.lond_to),
    url(r'^no_lond_to',hashuang.no_lond_to),
    url(r'^little_lond_to',hashuang.little_lond_to),
    #转炉统计分析综合条件筛选
    url(r'^zong_analy_ha',hashuang.multi_analy),
    #加载钢种
    url(r'^paihao_getGrape',hashuang.paihao_getGrape),
    #统计分析方法
    url(r'^describe_ha',hashuang.describe_ha),
    #质量回溯
    #加载单炉次质量回溯页面（product_quality.html）
    url(r'^product_quality',hashuang.product_quality),
    #同时计算正态分布和概率分布
    url(r'^probability_distribution',qualityzhuanlu.probability_distribution),
    url(r'^qualityfields',qualityzhuanlu.qualityfields),
    #单炉次原因追溯
    #url(r'^q_max_influence',qualityzhuanlu.max_influence),
    url(r'^quality_singlefurnace_regression_analyse',qualityzhuanlu.quality_singlefurnace_regression_analyse),
    #比较多炉次波动率计算(m_fluc_qulity.html)
    url(r'^w_fluc_quality',hashuang.w_fluc_quality),
    #波动率原因追溯
    url(r'^fluc_qualityfields',fluc_quality.fluc_qualityfields),
    url(r'^quality_fluc_influence',fluc_quality.quality_fluc_influence),
    url(r'^quality_multifurnace_regression_analyse',fluc_quality.quality_multifurnace_regression_analyse),
    
    #暴力求解
    # url(r'^violent_ananlyse',qualityzhuanlu.violent_ananlyse),

    #钢铁价格预测
    #price-predict
    url(r'^steelprice$',steelprice.steelprice),#加载价格预测界面，并初始化参数
    url(r'^price_history$', steelprice.price_history),#价格历史数据

    url(r'^price_predict$', steelprice.price_predict),#价格预测

    #铁矿石价格预测
    url(r'^ironstoneprice',ironstoneprice.ironstoneprice),
    # url(r'^iron_price_history', ironstoneprice.iron_price_history),stone_price_predict
    url(r'^stone_price_history',ironstoneprice.price_history),
    url(r'^stone_price_predict',ironstoneprice.price_predict),

    #chen
    #显示chen页面
    url(r'^chen', chyulia.chen),
    url(r'^cost_produce',chyulia.cost_produce),
    #自动加载钢种
    url(r'^getGrape',chyulia.getGrape),
    #跳转到波动率页面fluctuation.html
    url(r'^fluctuation$',chyulia.fluctuation),
    #定期更新数据库中表结构表中的期望等参数值(全部数据)，每月更新
    url(r'^updatevalue',chyulia.updatevalue),
    #同时计算正态分布和概率分布
    url(r'^probability_normal',chyulia.probability_normal),
    #比较总体的波动率计算(fluctuation.html)
    url(r'^fluc_cost_produce',fluc_chyulia.fluc_cost_produce),
    #波动率原因追溯
    url(r'^fluc_influence',fluc_chyulia.fluc_influence),
    #定期更新数据库中表结构表中的期望等参数值（本月及上月数据），每日更新
    url(r'^daily_updatevalue',fluc_chyulia.daily_updatevalue),
    url(r'^test',chyulia.test),
    url(r'^analysis_tool$',chyulia.analysis_tool),
    url(r'^violent_analyse$',violent_analyse.violent_analyse),
    url(r'^singlefurnace_regression_analyse',chyulia.singlefurnace_regression_analyse),
    url(r'^multifurnace_regression_analyse',fluc_chyulia.multifurnace_regression_analyse),
    url(r'^regression_analyse$',chyulia.regression_analyse),


    #添加工具类方法，之后处理为批处理事件
    url(r'^relation_ana$',batchprocess.relation_ana),
    url(r'^report$',batchprocess.report),

]
