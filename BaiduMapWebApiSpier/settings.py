from sqlalchemy import create_engine
import yagmail
BOT_NAME = 'BaiduMapWebApiSpier'

SPIDER_MODULES = ['BaiduMapWebApiSpier.spiders']
NEWSPIDER_MODULE = 'BaiduMapWebApiSpier.spiders'

LOG_LEVEL = 'INFO'

LOG_FILE = 'log.txt'
# 设置高德地图API Key
GaoDeMap_API_KEY = '182ad5d7061ed1e421091c22089c3677'

# 设置百度地图， 在这里填入你的百度ak,可填写多个，程序会随机调用，调用前会检测ak是否无效，若无效自动使用列表中的下一个ak，直至使用完毕
ak_list = ['iMplFNfYyAf4e7EleegtObtcOZdliriG']

# 设置需要获取的区域 列表,可以填写省、市、区县，也可以填写省、市、区县的代码，具体可参考高德地图开放平台：行政区划查询接口
region_name_list = ["成都市", "德阳市"]
# 设置需要获取的关键词
query_word_list = ['大学']

# 设置mysql 信息
MYSQL_HOST = 'localhost'  # mysql ip
MYSQL_USER = 'root'  # mysql用户名
MYSQL_PASSWORD = 'test123456'  # mysql用户名密码
MYSQL_DBNAME = 'adas'  # mysql 中数据库名，必须提前创建好
MYSQL_TableName = ''  # 将要写入的数据库中的表名，若不存在会自动创建，若为'default'，则自动以"指定的区域名_bd_map_pois"命名

# mysql sqlalchemy引擎数据，不用修改，自动读取以上配置。
engine = create_engine(
    'mysql+pymysql://{user}:{passwd}@{host}:3306/{db_name}?charset=utf8'.format(user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                                                                host=MYSQL_HOST, db_name=MYSQL_DBNAME),
    echo=False)

# 配置ak消耗完毕时的邮件发送选项
def send_email_163(subject, body, file):
    # 配置163发送邮件的主体账户选项
    yag = yagmail.SMTP(user='xugongli2012@163.com', password='', host='smtp.163.com', port='465')
    body = body
    # 配置接收邮件的邮箱
    yag.send(to=['982749459@qq.com'], subject=subject, contents=[body, r'%s' % file])

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_TIMEOUT = 180

ITEM_PIPELINES = {
    'BaiduMapWebApiSpier.pipelines.BaidumapwebapispierPipeline': 300,
}


