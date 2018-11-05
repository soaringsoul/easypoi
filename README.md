

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


----------

## 项目结构

> 后续补充 
>

----------

## 准备工作

* 1 安装 `Twisted` 库，需要离线安装

  > 可以到[https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted)下载相应python版本的Twisted 的离线文件
  
  > 然后使用 `pip install Twisted_xxxx版本.whl` 安装
  


* 2 安装[pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/)

> 注意：如果使用virtualenv 环境，请参考此博客[https://blog.csdn.net/qingche456/article/details/54587898](https://blog.csdn.net/qingche456/article/details/54587898)

* 3 使用`pip install requirements.txt`安装依赖库


> 注意：前提是必须先安装`Twisted`库，不然安装时会报错
>
	lxml==4.2.5
	numpy==1.15.4
	pandas==0.23.4
	PyMySQL==0.9.2
	pypinyin==0.33.2
	requests==2.20.0
	Scrapy==1.5.1
	Shapely==1.6.4.post2
	SQLAlchemy==1.2.12
	yagmail==0.11.214




### 设置

设置文件位置： `china_region_pois_spider\BaiduMapWebApiSpier\settings.py`

#### 1 设置高德地图开发平台api_key

默认已经设置（但有次数限制1000/天），这个key主要用来调用行政区划边界api，1000/天其实是足够了。

高德地图开发平台：[https://lbs.amap.com/](https://lbs.amap.com/)
	
	GaoDeMap_API_KEY = '182ad5d7061ed1e421091c22089c3677'


#### 2 设置百度地图开发平台ak

可移步申请：[百度地图开放平台](http://lbsyun.baidu.com/)

	ak_list = ['iMplFNfYyAf4e7EleegtObtcOZdliriG']

注意：这里是以个列表，你可以放置多个ak,程序会随机调用，调用前会检测ak是否有效，若无效自动使用列表中的下一个ak，直至使用完毕

#### 3 设置需要获取的区域 列表,可以填写多个省、市、区县，也可以填写省、市、区县的代码，具体可参考高德地图开放平台：行政区划查询接口

	region_name_list = ["成都市", "德阳市"]


#### 4 设置需要获取的兴趣点关键词，同样是列表，可填写多个

	query_word_list = ['大学', '咖啡馆']

#### 5 设置mysql 存储信息
	
		# 设置mysql 信息
		MYSQL_HOST = 'localhost'  # mysql ip
		MYSQL_USER = 'root'  # mysql用户名
		MYSQL_PASSWORD = 'test123456'  # mysql用户名密码
		MYSQL_DBNAME = 'test'  # mysql 中数据库名，必须提前创建好
		MYSQL_TableName = ''  # 将要写入的数据库中的表名，若不存在会自动创建，若为空，则自动以"指定的区域名_bd_map_pois"命名



#### 6 配置ak消耗完毕时的邮件预警通知选项，这里以163邮箱为例，实际可以设置为qq邮箱、hotmail等

	def send_email_163(subject, body, file):
	    # 配置163发送邮件的主体账户选项
	    yag = yagmail.SMTP(user='xugongli2012@163.com', password='', host='smtp.163.com', port='465')
	    body = body
	    # 配置接收邮件的邮箱
	    yag.send(to=['982749459@qq.com'], subject=subject, contents=[body, r'%s' % file])



### 运行

直接运行根目录下的`run.py`即可：`python run.py`

![run](/img/run.gif)



## 联系我

你可以在这里找到我：[夜雨微寒的个人主页](https://xugongli.github.io/about/)


## License


[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).



