# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import rethinkdb as r
import datetime
import json
import yaml
import ast
import sys
import hashlib
from urltools import *
reload(sys)
sys.setdefaultencoding('utf-8')

class GetnewsPipeline(object):
    def process_item(self, item, spider):
        return item


def stringify_dict(dct_or_tuples, encoding='utf-8', keys_only=True):
    """Return a (new) dict with the unicode keys (and values if, keys_only is
    False) of the given dict converted to strings. `dct_or_tuples` can be a
    dict or a list of tuples, like any dict constructor supports.
    """
    d = {}
    for k, v in dict(dct_or_tuples).iteritems():
        k = k.encode(encoding) if isinstance(k, unicode) else k
        if not keys_only:
            v = v.encode(encoding) if isinstance(v, unicode) else v
        d[k] = v
    return d

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class RethinkdbPipeline(object):
    table_name1 = "ArticleIndex"
    table_name2 = "ArticleStatus"
    table_name3 = "ArticleGnews"


    def __init__(self, rdb_host, rdb_database, rdb_port, rdb_authkey):
        #Init Database connection
        self.rdb_host = rdb_host
        self.rdb_database = rdb_database
        self.rdb_port = rdb_port
        self.rdb_authkey= rdb_authkey



    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            rdb_host=crawler.settings.get('RDB_HOST', 'testdata.mawto.com'),
            rdb_database=crawler.settings.get('RDB_DATABASE', 'Mawto'),
            rdb_port=crawler.settings.get('RDB_PORT', 28015),
            rdb_authkey=crawler.settings.get('RDB_AUTHKEY', 'atom')

        )

    def open_spider(self, spider):
        r.connect(host='testdata.mawto.com',
                 port=28015,
                 db='Mawto',
                 auth_key='atom').repl()

    def process_item(self, item, spider):

        data = yaml.safe_dump(dict(item), allow_unicode=True)
        data2 = yaml.safe_load(data)
        data2.update({'dateinserted':r.now()})


        links = {k: ''.join(v) for k, v in data2.items() if k.startswith('link')}
        link = {k: ''.join(v) for k, v in data2.items() if k.startswith('link')}

        x=links.get('link')
        url=''.join(x).decode('utf-8')
        dbid = hashlib.sha1(urltools.normalize(url)).hexdigest()
        link.update({'id': dbid})

        links.update({'id': dbid})
        links.update({'dateinserted':r.now()})
        links.update({'summarizable':1})
        links.update({'summarized':0})
        links.update({'animated':0})
        data2.update({'id': dbid})
        response = r.db(self.rdb_database).table(self.table_name1).insert(link, conflict='error').run()
        error = response.get('first_error')

        if error:
            print (error)
        else:
            r.db(self.rdb_database).table(self.table_name2).insert(links).run()
            r.db(self.rdb_database).table(self.table_name3).insert(data2).run()
        return item
