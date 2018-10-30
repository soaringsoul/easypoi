

<img align="right" width="200" height="200" src="https://pic4.zhimg.com/v2-78d1472351272f41d8dd76a6d8a635c7_xll.jpg">

# 中国行政区域POIS(兴趣点)采集工具
===========================================

[![image](https://img.shields.io/pypi/v/requests.svg)](https://pypi.org/project/requests/)
[![image](https://img.shields.io/pypi/l/requests.svg)](https://pypi.org/project/requests/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)






## 功能概述

### 功能
1. 获取中国境内指定行政区域内（最大可精确到街道）的指定关键词的所有兴趣点
例如可以获取一个城市内所有的便利店、商场、超市、咖啡店等兴趣点信息
2. 组合批量获取中国境内多个行政区域内多个关键词的所有兴趣点信息
3. 将所有采集到兴趣点数据存储到指定的`mysql`数据库中

### 获取结果示例

![beijing_food_pois_examples](/img/beijing_food_pois_examples.jpg)



![beijing_food_pois_examples_markers](/img/beijing_food_pois_examples_markers.jpg)


## 项目结构

> 后续补充 
>

## 依赖库

可以直接使用`pip install requirements.txt`安装

	pandas
	PyMySQL==0.9.2
	requests==2.19.1
	requests-download==0.1.2
	Scrapy==1.5.1
	Shapely==1.6.4.post2
	SQLAlchemy==1.2.12
	Twisted==18.7.0
	xlrd==1.0.0
	yagmail==0.11.214


注意以下两点：

* `scrapy`中使用到了`Twisted`框架，如果在安装scrapy过程中提示Twisted安装错误：

  可以到[https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted)下载Twisted 的离线文件安装。


* 若出现 `ImportError: No module named 'win32api'` 错误，下载安装 [pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/)

## 使用说明

### 设置

设置文件位置： `china_region_pois_spider\BaiduMapWebApiSpier\settings.py`

1. 设置高德地图开发平台api_key，默认已经设置（但有次数限制1000/天），高德地图开发平台：[https://lbs.amap.com/](https://lbs.amap.com/)
	
	GaoDeMap_API_KEY = '182ad5d7061ed1e421091c22089c3677'

2. 设置百度地图开发平台ak，可移步申请：[百度地图开放平台](http://lbsyun.baidu.com/)

		ak_list = ['iMplFNfYyAf4e7EleegtObtcOZdliriG']
注意：这里是以个列表，你可以放置多个ak,程序会随机调用，调用前会检测ak是否无效，若无效自动使用列表中的下一个ak，直至使用完毕

3. 设置需要获取的区域 列表,可以填写多个省、市、区县，也可以填写省、市、区县的代码，具体可参考高德地图开放平台：行政区划查询接口

		region_name_list = ["成都市", "德阳市"]

4. 设置需要获取的兴趣点关键词，同样是列表，可填写多个

		query_word_list = ['大学', '咖啡馆']

6. 设置mysql 存储信息

	# 设置mysql 信息
	MYSQL_HOST = 'localhost'  # mysql ip
	MYSQL_USER = 'root'  # mysql用户名
	MYSQL_PASSWORD = 'test123456'  # mysql用户名密码
	MYSQL_DBNAME = 'test'  # mysql 中数据库名，必须提前创建好
	MYSQL_TableName = ''  # 将要写入的数据库中的表名，若不存在会自动创建，若为空，则自动以"指定的区域名_bd_map_pois"命名



7.配置ak消耗完毕时的邮件预警通知选项，这里以163邮箱为例，实际可以设置为qq邮箱、hotmail等

	def send_email_163(subject, body, file):
	    # 配置163发送邮件的主体账户选项
	    yag = yagmail.SMTP(user='xugongli2012@163.com', password='', host='smtp.163.com', port='465')
	    body = body
	    # 配置接收邮件的邮箱
	    yag.send(to=['982749459@qq.com'], subject=subject, contents=[body, r'%s' % file])



### 运行根目录下的`run.py`，即`python run.py`即可

![run](/img/run.gif)


## License

[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).



