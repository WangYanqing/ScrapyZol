# -*- coding: utf-8 -*-
import scrapy
from zol.items import *
import re
import os, os.path
import urllib
import copy


class PhonespiderSpider(scrapy.Spider):
    name = 'PhoneSpider'
    allowed_domains = ['detail.zol.com.cn']
    start_urls = ['http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html']

    _id = 0
    folder = 'phonesImg'
    items = []

    keyMap = {
    unicode('上市日期', 'utf-8') : 'onSaleDate',
    unicode('主屏尺寸', 'utf-8') : 'screenSize',
    unicode('主屏分辨率', 'utf-8') : 'resolution',
    unicode('操作系统', 'utf-8') : 'osName',
    unicode('核心数', 'utf-8') : 'nCpuCores',
    unicode('CPU型号', 'utf-8') : 'cpuType',
    unicode('CPU频率', 'utf-8') : 'cpuSpeed',
    unicode('GPU型号', 'utf-8') : 'gpuType',
    unicode('RAM容量', 'utf-8') : 'ram',
    unicode('ROM容量', 'utf-8') : 'rom',
    }

    def parse(self, response):
        if os.path.exists(self.folder) == False:
        	os.mkdir(self.folder)


        phones = response.xpath('//ul[@class="clearfix"]/li')

        print('--------N phones: %d' % len(phones))
        for phone in phones:
            item = PhoneItem()
            item['_id']    = self._id
            self._id = self._id + 1


            #img src
            imgStr = phone.xpath('a[@class="pic"]/img').extract_first()
            # print('------img=%s' % imgStr)
            m = re.match('.+ \.src="(\S+)".+', imgStr)
        	# print(m)
            if m != None:
            	item['imgSrc'] = m.group(1)
            item['desp']	= phone.xpath('h3/a/@title').extract_first()
            item['price']	= phone.xpath('div[@class="price-row"]//b[@class="price-type"]/text()').extract_first()
        	# print(self.item)

            url = response.urljoin(phone.xpath('a/@href').extract_first())
            item['url'] = url
            request =  scrapy.Request(url, callback = self.parseDetail)
            request.meta['item'] = copy.deepcopy(item)
            yield request

        nodeNext = response.xpath('//div[@class="page-box"]//a[@class="next"]/@href').extract_first()
        # print('----------==========', nodeNext)
        if nodeNext:
            url = response.urljoin(nodeNext)
            yield scrapy.Request(url, callback = self.parse)
            # yield scrapy.Request(url, callback = self.parse, dont_filter = True)



    def parseDetail(self, response):
    	param = response.xpath('//ul[@class="nav__list clearfix"]/li[4]/a/@href').extract_first()
    	# print('====')
    	# print(param)
    	url = response.urljoin(param)
    	# print('----url: %s' % url)

    	request = scrapy.Request(url, callback = self.parseParam)
        # print('-------------xxxxxxxxxxxx')
        # print(response.meta['item'])
        request.meta['item'] = copy.deepcopy(response.meta['item'])
        yield request



    def parseParam(self, response):
    	node = response.xpath('//dd[@class="clearfix"]/ul/li[1]')

        # print('------------yyyyyyyy')
        metaItem = response.meta['item']

        item = PhoneItem()
        item['_id']         = metaItem['_id']
        item['imgSrc']      = metaItem['imgSrc']
        item['desp']        = metaItem['desp']
        item['price']       = metaItem['price']
        item['url']       = metaItem['url']

    	item['screenSize'] 	= node.xpath('p[1]/@title').extract_first()
    	item['resolution'] 	= node.xpath('p[2]/@title').extract_first()
    	item['name']		= response.xpath('//div[@class="version-series"]/span/text()').extract_first()

        paramTables = response.xpath('//div[@id="paramTable"]/div[@id="newTb"]/table')

        #Get the params
        for pt in paramTables:
            liNodes = pt.xpath('.//ul[@class="category-param-list"]/li')
            for ln in liNodes:
                tag = ln.xpath('span[1]/text()').extract_first().strip()
                val = ln.xpath('span[2]/text()').extract_first()
                if val == None:
                    val = ln.xpath('span[2]/a/text()').extract_first()
                # print('%s : %s' % (tag, val))
                if self.keyMap.has_key(tag):
                    item[self.keyMap[tag]] = val

        # print(item)

        # Scratch the phone image
    	# urllib.urlretrieve(item['imgSrc'], os.path.join(self.folder, ('%d.png' % item['_id'])))
    	yield item
