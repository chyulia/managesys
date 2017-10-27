#!/usr/bin/env python3.5.2
import os

from django.shortcuts import render, render_to_response
from django.conf import settings

scrapy_root = settings.SCRAPY_ROOT

AllElements = (
    'CRU cugangyuedu fdczs feigang gcck gcjk gkkc gtcl haiyun meitan_ljm '+
    'meiyuan PMI PPI psjgzs pugang tegang_zonghe tiejingfen tksjkl tksykcl tkszs WTI').split(' ')
for extra_ele in ('pugang', 'tegang_zonghe', 'tkszs'):
    AllElements.remove(extra_ele)
# print(AllElements)



def handler404(request):
    return render(request, '404.html', status=404)

def paralle_test1():
    print('hello')
    with open('/home/maksim/venv/qinggang/managesys/QinggangManageSys/test_crontab.txt','a') as f:
        f.write("hello\n")

# TODO 部署时还需要注意的问题 SCRAPY_ROOT的路径
def scrapy_elements():
    AllElements = ['CRU']
    scrapy_project_root = os.path.join(scrapy_root, 'scrapy')
    cmd = os.path.join(scrapy_project_root, 'scrapy_elements.sh')
    for ele_type in AllElements:
        cmd_params = " ".join([cmd, scrapy_project_root, ele_type])
        cmd_str = "%s %s %s" % (cmd, scrapy_project_root, ele_type)
        # os.system("%s %s %s" % (cmd, scrapy_project_root, ele_type))
        print(cmd_params == cmd_str)
        os.system(cmd_params)