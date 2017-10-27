import os
import datetime
from django.test import TestCase
from django.conf import settings
from QinggangManageSys.data_import  import models
from QinggangManageSys.data_import.models import BaseManage
# Create your tests here.


class BaseManageTeatCase(TestCase):

    def __init__(self):
        sqlVO = {}
        sqlVO["db_name"] = "l2own"
        sqlVO["sql"] = "select distinct heat_no from PRO_BOF_HIS_PLAN_TESTUPDATE"
        # heatlist = models.BaseManage().direct_select_query_sqlVO(sqlVO)
        # print(heatlist)




from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QinggangManageSys.QinggangManageSys.settings")


application = get_wsgi_application()

if __name__ == '__main__':
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QinggangManageSys.settings")
    # settings.configue()
    BaseManageTeatCase()