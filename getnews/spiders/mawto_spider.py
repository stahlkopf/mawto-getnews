# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import schedule
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from getnews.items import GnewsItem

class MawtoSpiderSpider(scrapy.Spider):
    name = "mawto_spider"
    allowed_domains = ["google.com"]
    start_urls=['https://news.google.com/news/section?cf=all&pz=1&topic=b','https://news.google.com/news/section?cf=all&pz=1&topic=tc','https://news.google.com/news/section?cf=all&pz=1&topic=e''https://news.google.com/news/section?cf=all&pz=1&topic=s','https://news.google.com/news/section?cf=all&pz=1&topic=snc','https://news.google.com/news/section?cf=all&pz=1&topic=m','https://news.google.com/news/section?cf=all&pz=1&topic=w']

    def parse(self,response):
            item=GnewsItem()
            catitem=GnewsItem()

            #unicode(response.body.decode(response.encoding)).encode('utf-8')


            div2=response.xpath('//div[starts-with(@class,"section story-section")]')

            for sel1 in div2.xpath('.//div[starts-with(@class,"blended-wrapper")]'):

                    catitem['topstory']=sel1.xpath('.//h2//span[@class="titletext"]/text()').extract()
                    catitem['link']=sel1.xpath('.//h2//@href').extract()
                    catitem['link']=''.join(catitem['link'])
                    catitem['originallink']=sel1.xpath('.//h2//@url').extract()
                    catitem['category']=sel1.xpath('./preceding-sibling::div[@class="section-header"]//div[@class="section-name"]/text()').extract()
                    if not catitem['category']:
                        catitem['category']=sel1.xpath('./preceding-sibling::div[@class="section-header"]//span[@class="section-name"]/text()').extract()
                    #This converts the category JSON item from a list into strings
                    # For some reason the crawler returns everything back as
                    # a list or dictionary, even a URL or single word

                    catitem['category']=''.join(catitem['category'])
                    catitem['category']= (str(catitem['category'])).replace("»","")
                    #print (catitem['category'])
                    catitem['snippet']=sel1.xpath('.//div[@class="esc-lead-snippet-wrapper"]/text()').extract()
                    catitem['sublinks']=sel1.xpath('.//div[@class="esc-secondary-article-wrapper"]//@url').extract()
                    catitem['gpost']=sel1.xpath('.//div[@class="gpost-body"]//@href').extract()
                    catitem['gpostsnip']=sel1.xpath('.//div[@class="gpost-body"]//text()').extract()
                    catitem['related']=sel1.xpath('.//div//span//a[@class="esc-topic-link"]//@href').extract()
                    catitem['extras']=sel1.xpath('.//div[@class="esc-diversity-wrapper"]//span/text()').extract()
                    catitem['extraslink']=sel1.xpath('.//div[@class="esc-diversity-wrapper"]//@href').extract()
                    yield catitem
