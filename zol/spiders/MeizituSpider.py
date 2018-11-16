# coding: utf8

from zol.items import *
import scrapy


class MeizituSpider(scrapy.Spider):
    name = 'MeizituSpider'
    allowed_domains = ['www.meizitu.com']
    start_urls = ['http://www.meizitu.com/']
    pageId = 0

    def parse(self, response):
        nodes = response.xpath('//div[@id="pagecontent"]//div[@class="postmeta  clearfix"]')

        print('==========PAGE: %d' % self.pageId)
        for node in nodes:
            a0      = node.xpath('div[1]/h2/a')
            url0    = a0.xpath('@href').extract_first()
            ttl0    = a0.xpath('@title').extract_first()

            print unicode(ttl0), url0

        self.pageId += 1

        nextPageLi = response.xpath('//div[@class="navigation"]/div[@id="wp_page_numbers"]/ul/li[2]')
        an = nextPageLi.xpath('a/@href').extract_first()
        print 'next page href=' + an