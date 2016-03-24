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

    table_name = "ArticleURL"

    def __init__(self, rdb_host, rdb_database, rdb_port, rdb_authkey):
        #Init Database connection
        self.rdb_host = rdb_host
        self.rdb_database = rdb_database
        self.rdb_port = rdb_port
        self.rdb_authkey= rdb_authkey



    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            rdb_host=crawler.settings.get('RDB_HOST', '159.203.16.47'),
            rdb_database=crawler.settings.get('RDB_DATABASE', 'Mawto'),
            rdb_port=crawler.settings.get('RDB_PORT', 28015),
            rdb_authkey=crawler.settings.get('RDB_AUTHKEY', 'atom')

        )

    def open_spider(self, spider):
        r.connect(host='159.203.16.47',
                 port=28015,
                 db='Mawto',
                 auth_key='atom').repl()

    def process_item(self, item, spider):

        #data= repr(item).decode("unicode-escape")
        #category = {k: v for k, v in item.items() if k.startswith('category')}
        #print (category)
        #text = {k: v for k, v in dict(item).items()}
        #text = stringify_dict(text)
        #for k,v in text.items():
           #for item in v:
              #print(item)
           #print k, 'corresponds to', v

        #Jsonify an item
        #data = json.dumps(dict(item), ensure_ascii=False).encode('utf8')
        data = yaml.safe_dump(dict(item), allow_unicode=True)


        #Remove the Unicode escaped characters
        #data = data.decode('unicode_escape').encode('ascii','ignore')
        #Reload as JSON and strip the unicode u'
        data2 = yaml.safe_load(data)
        #print (data2)
        #Add the date inserted field
        data2.update({'dateinserted':r.now()})

        #########data2 = {k: ''.join(v) for k, v in data2.items()}
        #Create a links dict/JSON entity containing URLs
        links = {k: ''.join(v) for k, v in data2.items() if k.startswith('link')}
        links.update({'dateinserted':r.now()})
        links.update({'summarizable':1})
        links.update({'summarized':0})
        links.update({'animated':0})
        links.update({'id': r.uuid(v).run() for k, v in links.items() if k.startswith('link')})
        r.db(self.rdb_database).table(self.table_name).insert(links).run()
        r.db(self.rdb_database).table('ArticleGnews').insert(data2).run()
        return item
