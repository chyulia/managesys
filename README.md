# managesys
## 使用Django搭建的数据管理系统
### 提供数据整合，分析，以及分析结果展示

### 准备工作
项目启动之前需要安装oracle  client以连接oracle数据库，需要下载相应的basic和sdk，并按照下载页面末端的安装步骤配置oracle client，然后才能成功执行。
```
pip install cx_Oracle
```
[oracle client下载及安装说明](http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html)

### Setting up Django and your web server with uWSGI and nginx
[这是一个非常详尽的Django+uWSGI+nginx安装说明](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)
```
pip install uwsgi  
将项目配置写入mysite_uwsgi.ini中，本项目参考uwsgi.ini  
uwsgi --ini mysite_uwsgi.ini  

网站的配置文件与nginx的配置文件连接，使nginx可以读取到相关配置  
sudo ln -s /home/maksim/venv/qinggang/managesys/managesys_nginx.conf  /etc/nginx/sites-enabled/  
Restart nginx:  
sudo /etc/init.d/nginx restart  
```

## 代码同步
fork代码并与原仓库保持同步（即将原仓库的更新合并到本地仓库）
```
git  remote -v  
git remote add upstream  (rpo you fork from)  

git fetch upstream   //fetch会拉取远程仓库的所有分支
git checkout master  
git merge upstream/master  
```

## 把scrapy框架嵌入django
### 两种方案
1. 使用scrapyd部署scrapy
   [scrapyd部署说明](http://scrapyd.readthedocs.io/en/latest/install.html)
2. 将scrapy嵌入django
   [可能会有效的参考](https://github.com/holgerd77/django-dynamic-scraper/blob/master/example_project/example_project/settings.py)

## 关闭终端时不结束进程
nohup conmand &
任意键返回终端

## 定时处理任务说明
在程序模块中添加子应用django_crontab，在QinggangManageSys.settings.py中添加配置：
```
INSTALLED_APPS = [
    ...
    'data_import',
    ...
    'django_crontab',
]
```

统一在CRONJOBS列表中添加定时执行任务:

```
CRONJOBS = [
    ('*/1 * * * *', 'QinggangManageSys.views.paralle_test1'),
]
```

上面是一个简单的例子，表示每隔1分钟，执行一次QinggangManageSys.views.paralle_test1方法。

表示的核心就是用'* * * * *'表示循环执行的时间，分别代表“分(0-59)时(0-23)日(1-31)月(1-12,or Jan,Feb...)周(0-7,0or7=Sun.)”，后面表示具体执行的操作。

可循环的时间为分钟、 小 时、 每 周、 每月或每年等。

练习时间，以下分别表示什么时间呢，答案在最后^_^

```
59 23 3 7 *
59 21 * * 5
59 23 3 7 5
```

几个例子来说明时间的定义：

| 特殊字符   | 代表意义                                     |
| ------ | ---------------------------------------- |
| *(星号)  | 代表任何时刻都接受的意思！举例来说，范例一内那个日、月、周都是* ， 就代表着『不论何月、何日的礼拜几的12:00 都执行后续指令』的意思！ |
| ,(逗号)  | 代表分隔时段的意思。举例来说，如果要下达的工作是3:00 与6:00 时，就会是：0 3,6 * * * command时间参数还是有五栏，不过第二栏是3,6 ，代表3 与6 都适用！ |
| -(减号)  | 代表一段时间范围内，举例来说， 8 点到12 点之间的每小时的20 分都进行一项工作：20 8-12 * * * command仔细看到第二栏变成8-12 喔！代表8,9,10,11,12 都适用的意思！ |
| /n(斜线) | 那个n 代表数字，亦即是『每隔n 单位间隔』的意思，例如每五分钟进行一次，则：*/5 * * * * command很简单吧！用* 与/5 来搭配，也可以写成0-59/5 ，相同意思！ |


答案：

```
1. 今天是同学生日，所以你在7月3日23:59给自己预定了一个闹钟，每年的7月3日23:59都会有这个闹钟来提醒你
2. 你约好了朋友每周六去爬山，所以你会在每个周五的21:59给朋友发出提醒，让他们不要忘了明天的约定
3. 你一定会以为是7月3日且必须是周五的23:59才会执行操作，其实不会，系统会以为是7月3日，也可能会以为是周五才执行操作，这样行为就变得不可控了，因而日月和星期不可同时指定。
```



> 日月和星期不可同时指定。
>
> 更多详情参考[django-crontab Github](https://github.com/kraiz/django-crontab)和[鸟哥的linux私房菜](http://linux.vbird.org/linux_basic/0430cron.php#cron)。

### 在系统中添加定时任务
```
# run this command to add all defined jobs from CRONJOBS to crontab
python manage.py crontab add
# show current active jobs of this project:
python manage.py crontab show
# removing all defined jobs is straight forward
python manage.py crontab remove
```
