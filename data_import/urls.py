from django.conf.urls import url, include
from . import views
from . import bof_dataanalysis
from . import bof_singlecost
from . import bof_fluccost
from . import bof_singlequality
from . import bof_flucquality
from data_import.PricePredict import price_predict
from . import quality_prediction
from . import batchprocess
from . import violent_analyse
from . import update
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
    url(r'^update_data_sales',views.update_data_sales),
    url(r'^update_orderno_orderItem',views.update_orderno_orderItem),
    url(r'^update_displistno',views.update_displistno),
    url(r'^update_loadno',views.update_loadno),
    url(r'^update_collectno',views.update_collectno),
    url(r'^update_receiveno',views.update_receiveno),
    url(r'^update_rtnno',views.update_rtnno),
    url(r'^update_millsheetno',views.update_millsheetno),
    url(r'^update_space_comparsion',views.update_space_comparsion),
    url(r'^update_space_marketshare',views.update_space_marketshare),

    #暴力求解
    # url(r'^violent_ananlyse',qualityzhuanlu.violent_ananlyse),

    #钢铁价格预测
    #price-predict
    url(r'^steelprice$', price_predict.steelprice),#加载价格预测界面，并初始化参数
    url(r'^price_history$', price_predict.price_history),#价格历史数据

    url(r'^price_predict$', price_predict.price_predict),#价格预测

    #铁矿石价格预测
    url(r'^ironstoneprice',price_predict.ironstoneprice),
    # url(r'^iron_price_history', ironstoneprice.iron_price_history),stone_price_predict
    url(r'^stone_price_history',price_predict.stone_price_history),
    url(r'^stone_price_predict',price_predict.stone_price_predict),

    url(r'^violent_analyse$',violent_analyse.violent_analyse),

    #质量预测
    #quelity-predict
    url(r'^quality_prediction',quality_prediction.quality_prediction),
    url(r'^lf_quality_predict',quality_prediction.lf_quality_predict),
    url(r'^lf_quality_history',quality_prediction.lf_quality_history),


    #成本质量相关页面的跳转
    #1、显示统计分析页面
    url(r'^bof_dataanalysis', views.bof_dataanalysis),
    #2、跳转到成本单炉次页面
    url(r'^bof_singlecost', views.bof_singlecost),
    #3、跳转到成本波动率页面
    url(r'^bof_fluccost$',views.bof_fluccost),
    #4、跳转到质量单炉次页面
    url(r'^bof_singlequality',views.bof_singlequality),
    #5、跳转到质量波动率计算页面
    url(r'^bof_flucquality',views.bof_flucquality),
    #跳转到分析工具页面
    url(r'^analysis_tool$',views.analysis_tool),


    #统计分析页面
    #按表结构加载下拉框
    url(r'^lond_to',bof_dataanalysis.lond_to),
    url(r'^no_lond_to',bof_dataanalysis.no_lond_to),
    url(r'^little_lond_to',bof_dataanalysis.little_lond_to),
    #转炉统计分析综合条件筛选
    url(r'^zong_analy_ha',bof_dataanalysis.multi_analy),
    #加载钢种
    url(r'^paihao_getGrape',bof_dataanalysis.paihao_getGrape),
    #统计分析方法
    url(r'^describe_ha',bof_dataanalysis.describe_ha),



    #转炉-单炉次-成本
    #自动加载钢种
    url(r'^getGrape',bof_singlecost.getGrape),
    #四大类成本字段的分析
    url(r'^cost_produce',bof_singlecost.cost_produce),
    #单炉次成本统一追溯函数
    url(r'^singlefurnace_regression_analyse',bof_singlecost.singlefurnace_regression_analyse),
    #同时计算正态分布和概率分布
    url(r'^probability_normal',bof_singlecost.probability_normal),
    #定期更新数据库中表结构表中的期望等参数值(全部数据)，每月更新
    url(r'^updatevalue',bof_singlecost.updatevalue),


    #转炉-多炉次-成本
    #四大类字段的总体波动率分析
    url(r'^fluc_cost_produce',bof_fluccost.fluc_cost_produce),
    #成本字段的波动率追溯（单个字段，鼠标触发）
    url(r'^fluc_influence',bof_fluccost.fluc_influence),
    #多炉次成本字段的统一追溯
    url(r'^multifurnace_regression_analyse',bof_fluccost.multifurnace_regression_analyse),
    #定期更新数据库中表结构表中的期望等参数值（本月及上月数据），每日更新
    url(r'^daily_updatevalue',bof_fluccost.daily_updatevalue),


    #转炉-单炉次-质量
    #质量字段的单炉次分析
    url(r'^qualityfields',bof_singlequality.qualityfields),
    #同时计算正态分布和概率分布
    url(r'^probability_distribution',bof_singlequality.probability_distribution),
    #单炉次原因追溯
    url(r'^quality_singlefurnace_regression_analyse',bof_singlequality.quality_singlefurnace_regression_analyse),


    #转炉=多炉次-质量

    #质量字段的总体波动率分析
    url(r'^fluc_qualityfields',bof_flucquality.fluc_qualityfields),
    #质量字段的波动率追溯（单个字段，鼠标触发）
    url(r'^quality_fluc_influence',bof_flucquality.quality_fluc_influence),
    #多炉次质量字段的统一追溯
    url(r'^quality_multifurnace_regression_analyse',bof_flucquality.quality_multifurnace_regression_analyse),



    #添加工具类方法，之后处理为批处理事件
    url(r'^relation_ana$',batchprocess.relation_ana),
    url(r'^report$',batchprocess.report),


    #更新bof数据
    url(r'^updatebof', update.updatebof),

]
