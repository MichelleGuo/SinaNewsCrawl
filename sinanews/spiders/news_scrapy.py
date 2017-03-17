# -*- coding: utf-8 -*-

import sys
sys.path.append("./sinanews")
import time
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Rule
from items import SinanewsItem
from ..startWork import initialization


# 列表数据结构合并
def ListCombiner(lst):
    string = ''
    for e in lst:
        string += e
    return string

class SinanewsSpider(scrapy.Spider):
    name = "sinanews"
    # allowed_domains = ["finance.sina.com.cn"]
    # dateNow = GetDate()
    target_date, path = initialization()
    start_urls = []
    # 国内财经滚动新闻入口
    gncj = 'http://roll.finance.sina.com.cn/finance/gncj/gncj/'
    pattern = '.shtml'
    # 每日新闻页面在五页以内
    for i in range(1,5):
        target_url = gncj + target_date + '_' + str(i) + pattern
        # 构建爬取目标
        start_urls.append(target_url)
    # url_pattern = r'(http://roll.finance.sina.com.cn)/finance/gncj/gncj/)'+ datenow +'_\d{4}(\d{8})\.(?:s)html'
    # rules = [Rule(LinkExtractor(allow=('./'+datenow+'_[2-4].shtml', ),))]

    def parse(self, response):
        # pattern = re.match(self.url_pattern, str(response.url))
        for sel in response.css('.list_009 li a::attr(href)'):
            # 获取当前页面所有新闻的url：response.xpath('//ul[@class="list_009"]/li')
            new_url = sel.extract()
            # 负责子页面内容的爬取:callback
            yield scrapy.Request(new_url, callback=self.parse_news)

    # 子页面新闻解析
    def parse_news(self, response):
        sel = Selector(response)
        item = SinanewsItem()
        item['title'] = sel.xpath("//h1[@id='artibodyTitle']/text()").extract()[0]
        item['link'] = str(response.url)
        item['desc'] = ListCombiner(sel.xpath('//p/text()').extract())
        # item['source'] = 'sina_financial_gncj'
        # item['date'] = dateNow
        yield item


