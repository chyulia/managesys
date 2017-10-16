import os
import datetime
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QinggangManageSys.settings")


# application = get_wsgi_application()

from django.conf import settings
from data_import  import models
# Create your tests here.
class BaseManageTeatCase():
    heatlist = None
    def __init__(self):

        sqlVO = {}
        sqlVO["db_name"] = "l2own"
        sqlVO["sql"] = "select distinct heat_no from PRO_BOF_HIS_PLAN_TESTUPDATE"
        self.heatlist = models.BaseManage().direct_select_query_sqlVO(sqlVO)


    def updateRecordbof(self):  # 定期更新完成后更新记录表
        # 从各个表中读取各自的最新数据时间
        sqlVO = {}
        sqlVO["db_name"] = "l2own"
        # tableNamelist = ['PRO_BOF_HIS_PLAN','PRO_BOF_HIS_MIRON','PRO_BOF_HIS_SCRAP','PRO_BOF_HIS_POOL','PRO_BOF_HIS_EVENTS','PRO_BOF_HIS_BOCSM','PRO_BOF_HIS_TEMP','PRO_BOF_HIS_CHRGDGEN','PRO_BOF_HIS_CHRGDDAT','PRO_BOF_HIS_ANAGEN','PRO_BOF_HIS_ANADAT']
        tableNamelist = ['PLAN', 'MIRON', 'SCRAP', 'POOL', 'EVENTS', 'BOCSM', 'TEMP', 'CHRGDGEN', 'CHRGDDAT', 'ANAGEN',
                         'ANADAT']
        for singlename in tableNamelist:
            sqlVO["sql"] = "select MAX(MSG_DATE) FROM PRO_BOF_HIS_" + singlename
            latestTime = models.BaseManage().direct_select_query_sqlVO(sqlVO)[0].get('MAX(MSG_DATE)', None)
            str_latestTime = datetime.datetime.strftime(latestTime, '%Y-%m-%d %H:%M:%S')
            sqlVO[
                "sql"] = "update PRO_BOF_HIS_RECORD set TABLE_" + singlename + " = to_date(' " + str_latestTime + " ','yyyy-mm-dd hh24:mi:ss')"
            models.BaseManage().direct_execute_query_sqlVO(sqlVO)

        # 最后更新记录表的更新时间
        # time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))#当前时间
        # sqlVO["sql"]= "update PRO_BOF_HIS_RECORD set RECORD_TIME = to_date(' " +time_now+" ','yyyy-mm-dd hh24:mi:ss')"
        sqlVO["sql"] = "update PRO_BOF_HIS_RECORD set RECORD_TIME = sysdate";
        models.BaseManage().direct_execute_query_sqlVO(sqlVO)

from django.db import transaction
# @transaction.atomic

# TODO 目前按照这种方式进行调用是可以执行事务的
def transaction_test():
    sqlVO = {}
    bsg = models.BaseManage()
    # bsg.identify_db('l2own')

    sql = "INSERT INTO person VALUES('%s', '%s', '%s')"
    persons = [(11, 'ccx', 'basketball'), (12, 'ccx', 'basketball'), ('13', 'cx', 'travle')]
    try:
        with transaction.atomic():
            for p in persons:
                sqlVO['sql'] = sql % p
                print('SQL [%s]' % sqlVO.get('sql'))
                bsg.execute_single(sqlVO)
    except Exception as e:
        print('ERROR:[', e, ']')
        print("事务执行出错")

def transaction_decorator(f):
    bsm = models.BaseManage()
    try:
        with transaction.atomic():
            f(bsm)
    except Exception as e:
        print("transaction error！")
        print('ERROR:[', e, ']')


def insert_people(base_manage_instnce):
    sqlVO = {}
    sql = "INSERT INTO person VALUES('%s', '%s', '%s')"
    persons = [(11, 'ccx', 'basketball'), (12, 'ccx', 'basketball'), ('13', 'cx', 'travle')]
    for p in persons:
        sqlVO['sql'] = sql % p
        print('SQL [%s]' % sqlVO.get('sql'))
        base_manage_instnce.execute_single(sqlVO)

def test_transaction_decorator():
    sqlVO = {}
    sql = "INSERT INTO person VALUES('%s', '%s', '%s')"
    persons = [(18, 'ccx', 'basketball'), (19, 'ccx', 'basketball'), ('20', 'cx', 'travle')]
    def inner_exe(bsm):
        """业务具体的执行逻辑
        Args:
            bsm: BaseManage实例对象，已经初始化数据库连接
        Returns:
            None
        """
        for p in persons:
            sqlVO['sql'] = sql % p
            print('SQL [%s]' % sqlVO.get('sql'))
            bsm.execute_single(sqlVO)

    models.transaction_decorator(inner_exe)

def updateRecordbof():  # 定期更新完成后更新记录表
    # 从各个表中读取各自的最新数据时间
    sqlVO = {}
    sqlVO["db_name"] = "l2own"
    # tableNamelist = ['PRO_BOF_HIS_PLAN','PRO_BOF_HIS_MIRON','PRO_BOF_HIS_SCRAP','PRO_BOF_HIS_POOL','PRO_BOF_HIS_EVENTS','PRO_BOF_HIS_BOCSM','PRO_BOF_HIS_TEMP','PRO_BOF_HIS_CHRGDGEN','PRO_BOF_HIS_CHRGDDAT','PRO_BOF_HIS_ANAGEN','PRO_BOF_HIS_ANADAT']
    tableNamelist = ['PLAN', 'MIRON', 'SCRAP', 'POOL', 'EVENTS', 'BOCSM', 'TEMP', 'CHRGDGEN', 'CHRGDDAT', 'ANAGEN',
                     'ANADAT']
    for singlename in tableNamelist:
        sqlVO["sql"] = "select MAX(MSG_DATE) FROM PRO_BOF_HIS_" + singlename
        latestTime = models.BaseManage().direct_select_query_sqlVO(sqlVO)[0].get('MAX(MSG_DATE)', None)
        str_latestTime = datetime.datetime.strftime(latestTime, '%Y-%m-%d %H:%M:%S')
        sqlVO["sql"] = "update PRO_BOF_HIS_RECORD set TABLE_" + singlename + " = to_date(' " + str_latestTime + " ','yyyy-mm-dd hh24:mi:ss')"
        models.BaseManage().direct_execute_query_sqlVO(sqlVO)

    # 最后更新记录表的更新时间
    # time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))#当前时间
    # sqlVO["sql"]= "update PRO_BOF_HIS_RECORD set RECORD_TIME = to_date(' " +time_now+" ','yyyy-mm-dd hh24:mi:ss')"
    sqlVO["sql"] = "update PRO_BOF_HIS_RECORD set RECORD_TIME = sysdate";
    models.BaseManage().direct_execute_query_sqlVO(sqlVO)

# updateRecordbof事务改写
def updateRecordbof_transaction():
    sqlVO = {}
    tableNamelist = ['PLAN', 'MIRON', 'SCRAP', 'POOL', 'EVENTS', 'BOCSM', 'TEMP', 'CHRGDGEN', 'CHRGDDAT', 'ANAGEN',
                     'ANADAT']
    def inner_exe(bsm):
        bsm.identify_db('l2own')
        for singlename in tableNamelist:
            sqlVO["sql"] = "select MAX(MSG_DATE) FROM PRO_BOF_HIS_" + singlename
            latestTime = bsm.select_single(sqlVO)[0].get('MAX(MSG_DATE)', None)
            str_latestTime = datetime.datetime.strftime(latestTime, '%Y-%m-%d %H:%M:%S')
            sqlVO["sql"] = "update PRO_BOF_HIS_RECORD set TABLE_" + singlename + \
                         " = to_date(' " + str_latestTime + " ','yyyy-mm-dd hh24:mi:ss')"
            bsm.execute_single(sqlVO)
    models.transaction_decorator(inner_exe)

@models.transaction_decorator
def tesr_sql(bsm):
    sqlVO = dict()
    # sqlVO['sql'] = "drop table PRO_BOF_HIS_TEMP_Middle1"
    sqlVO['sql'] = "create table PRO_BOF_HIS_ANADAT_Middle1 as select t2.*, t1.samp_type from PRO_BOF_HIS_ANAGEN t1 right join  PRO_BOF_HIS_ANADAT t2 on t1.samp_no = t2.samp_no and t1.heat_no =t2.heat_no where t2.msg_date >= to_date(' 2017-06-12 14:55:44 ','yyyy-mm-dd hh24:mi:ss')"
    bsm.execute_single(sqlVO)
@models.transaction_decorator
def tesr_drop_sql(bsm):
    sqlVO = dict()
    sqlVO['sql'] = "drop table PRO_BOF_HIS_TEMP_Middle1"
    # sqlVO['sql'] = "create table PRO_BOF_HIS_ANADAT_Middle1 as select t2.*, t1.samp_type from PRO_BOF_HIS_ANAGEN t1 right join  PRO_BOF_HIS_ANADAT t2 on t1.samp_no = t2.samp_no and t1.heat_no =t2.heat_no where t2.msg_date >= to_date(' 2017-06-12 14:55:44 ','yyyy-mm-dd hh24:mi:ss')"
    bsm.execute_single(sqlVO)
# TODO 在数据库内创建dblink的语句
"""
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
在实验室相关的配置应该是本机
-- Drop existing database link 
drop public database link DBLINK_TO_L2;
-- Create database link 
create public database link DBLINK_TO_L2
  connect to QG_USER identified by "123456"
  using '202.204.54.42:1521/orcl';
"""

from data_import import dynamic_update

if __name__ == '__main__':
    bsm = models.BaseManage()
    bsm.identify_db("l2own")
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QinggangManageSys.settings")
    # settings.configue()
    # abm = BaseManageTeatCase()
    # transaction_test()
    # test_transaction_decorator()
    # updateRecordbof_transaction()
    # updateRecordbof()
    dynamic_update.batch_dyupdatebof()

    # tesr_sql(bsm)
