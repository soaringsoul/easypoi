from sqlalchemy import create_engine

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
region_name_list = ["成都市"]
addcode_list = []
# 设置需要获取的关键词
query_word_list = ['大学']

# 设置mysql 信息
MYSQL_HOST = 'localhost'  # mysql ip

MYSQL_USER = 'root'  # mysql用户名
MYSQL_PASSWORD = 'adas123456'  # mysql用户名密码
MYSQL_DBNAME = 'adas'  # mysql 中数据库名，必须提前创建好

MYSQL_TableName = ''  # 将要写入的数据库中的表名，若不存在会自动创建，若为空，则自动以"指定的区域名_bd_map_pois"命名
engine = create_engine(
    'mysql+pymysql://{user}:{passwd}@{host}:3306/{db_name}?charset=utf8'.format(user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                                                                host=MYSQL_HOST, db_name=MYSQL_DBNAME),
    echo=False)


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'BaiduMapWebApiSpier (+http://www.yourdomain.com)'

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

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'BaiduMapWebApiSpier.middlewares.BaidumapwebapispierSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'BaiduMapWebApiSpier.middlewares.BaidumapwebapispierDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'BaiduMapWebApiSpier.pipelines.BaidumapwebapispierPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
