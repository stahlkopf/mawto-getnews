# -*- coding: utf-8 -*-

# Scrapy settings for getnews project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


from os.path import dirname,  join,  abspath
from datetime import datetime

BOT_NAME = 'getnews'

SPIDER_MODULES = ['getnews.spiders']
NEWSPIDER_MODULE = 'getnews.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'

LOG_ENABLED = True
LOG_LEVEL = 'WARNING'


DEBUG=True
JSON_DIR = 'json'
DATA_DIR = 'data'
LOG_DIR = 'log'
NOW = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
LOG_FILENAME =  NOW + '_' + BOT_NAME + '.log'
BASE_PATH = dirname(dirname(abspath(__file__)))
JSON_PATH = join(BASE_PATH,  JSON_DIR)
DATA_PATH = join(BASE_PATH,  DATA_DIR)
LOG_PATH = join(BASE_PATH,  LOG_DIR)
LOG_FULLPATH = join(LOG_PATH,  LOG_FILENAME)

LOG_FORMAT = "%(levelname)s [%(name)s] ( %(filename)s:%(lineno)s, in %(funcName)s) ______ %(message)s"


LOG_FILE = LOG_FULLPATH
  # options: CRITICAL, ERROR, WARNING, INFO, DEBUG


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'getnews (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'getnews.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'getnews.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'getnews.pipelines.RethinkdbPipeline': 300,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
