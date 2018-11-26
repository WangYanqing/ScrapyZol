# coding: utf8

import scrapy
from zol.items import *
import copy
import re


class CarSpider(scrapy.Spider):
    name = 'CarSpider'
    allowed_domains = ['www.autohome.com.cn', 'car.autohome.com.cn']
    start_urls = ['https://www.autohome.com.cn/car/']


    def parse(self, response):
        nodeAlphabets = response.xpath('//div[@class="uibox" and starts-with(@id, "box")]/div[starts-with(@class, "uibox-con rank-list") and starts-with(@id, "html")]')
        print('============test len=%d' % (len(nodeAlphabets)))

        for nodeAlp in nodeAlphabets:
            # letter = nodeAlp.xpath('div[contains(@class, "uibox-title")]/span/text()').extract_first()
            letter = nodeAlp.xpath('@id').extract_first()
            # scrapy.Selector.get()

            letter = letter[4:]
            if len(letter) != 1:
                continue
            print('--Alphabet=' + letter)

            nodeBrands = nodeAlp.xpath('dl')
            for nodeBrand in nodeBrands:
                brandName = nodeBrand.xpath('dt/div/a/text()').extract_first()

                nodeFactories = nodeBrand.xpath('dd/div[@class="h3-tit"]/a/text()').extract()
                nodeFacCars = nodeBrand.xpath('dd/ul[@class="rank-list-ul"]')

                print('  --Trunk=%s %d branches' % (brandName, len(nodeFactories)))
                i = 1
                for nodeFac in nodeFacCars:
                    # nodeFac = nodeFactories.get(i)
                    # nodeCars = nodeFacCars.get(i)
                    print '    %2d %s' % (i, nodeFactories[i - 1])
                    j = 1
                    nodeCars = nodeFac.xpath('li/h4/a')
                    for nodeCar in nodeCars:
                        carName = nodeCar.xpath('text()').extract_first()
                        carHref = nodeCar.xpath('@href').extract_first()

                        url = response.urljoin(carHref)
                        print '      %2d %s %s' % (j, carName, '')

                        item = CarItem()
                        item['brand']      = brandName
                        item['alpha']      = letter[4:]
                        item['factory']    = nodeFactories[i - 1]
                        item['name0']      = carName

                        request = scrapy.Request(url, callback = self.parseCarHome)
                        request.meta['item'] = copy.deepcopy(item)
                        yield request
                        j += 1
                        break
                    i += 1
                    break
                break
        print '----FINISH----'



    def parseCarHome(self, response):
        nodeNav = response.xpath('//div[starts-with(@class, "container athm-sub-nav")]/div[2]/ul/li[2]/a')

        if nodeNav != None and len(nodeNav) > 0:
            # print ' ====%s|%s' % (type(nodeNav), nodeNav)
            url0 = response.urljoin(nodeNav[0].xpath('@href').extract_first())
            name = nodeNav[0].xpath('text()').extract_first()
            # print '          %s %s' % (url0, name)
            print '----parseCarHome 1 ' + url0
            request = scrapy.Request(url0, callback = self.parseDetail)
            request.meta['item'] = copy.deepcopy(response.meta['item'])

            yield request
            print '----parseCarHome 2'



    def parseDetail(self, response):
        print '===============parseDetail 1'
        nodeTypes = response.xpath('//*[@id="config_nav"]')
        # nodeTypes = response.xpath('//div[@class="operation" and @id="config_nav"]/table/tbody')
        # nodeTypes = response.xpath('//div[@id="content" and @class="pzbox"]/div/table/tbody/tr/td[1]/div[2]/div/a')
        # if nodeTypes == None or len(nodeTypes) <= 0:
        #     return
        print '==types.len=%d' % len(nodeTypes.xpath('//tbody'))
        data0 = nodeTypes[0].xpath('//comment()').re(r'<!--(.*)-->')[0]
        print unicode(data0)
        print '===============parseDetail 2'

        for nType in nodeTypes:
            print '-=-= %s' % nType.xpath('text()')[0]

        print '===============parseDetail 3'
