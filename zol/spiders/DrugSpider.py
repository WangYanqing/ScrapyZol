# coding: utf8

import scrapy
from zol.items import *
import copy
import re


class DrugSpider(scrapy.Spider):
    name = 'DrugSpider'
    allowed_domains = ['www.drugbank.ca']
    start_urls = ['https://www.drugbank.ca/pharmaco/transcriptomics']

    def parse(self, response):
        items = response.xpath('//*[@id="gene_regulation_search"]/table/tbody/tr')
        pageId = 1
        m = re.search('page=(\\d+)', response.url)
        if m != None:
            pageId = int(m.group(1))

        print '----Drug table----len=%d PAGE=%d' % (len(items), pageId)
        for i in items:
            cols = i.xpath('td')
            # print cols
            print cols[0].xpath('a/text()').extract_first()

            drug = DrugItem()
            drug['drug']        = cols[0].xpath('a/text()').extract_first()
            drug['drugUrl']     = response.urljoin(cols[0].xpath('a/@href').extract_first())
            drug['drugGroup']   = cols[1].xpath('span/text()').extract_first()
            drug['gene']        = cols[2].xpath('a/text()').extract_first()
            drug['geneUrl']     = cols[2].xpath('a/@href').extract_first()
            drug['geneId']      = cols[3].xpath('a/text()').extract_first()
            drug['geneIdUrl']   = cols[3].xpath('a/@href').extract_first()
            drug['change']      = cols[4].xpath('span/text()').extract_first()
            drug['interaction'] = cols[5].xpath('text()').extract_first()
            drug['chromosome']  = cols[6].xpath('text()').extract_first()
            drug['references']  = cols[7].xpath('ul/li/a/text()').extract_first()
            drug['refUrl']      = cols[7].xpath('ul/li/a/@href').extract_first()

            yield drug
            break

        nextArr = response.xpath('//div[@class="pagination-holder"]/nav/ul/li[@class="page-item next"]/a/@href').extract_first()

        if nextArr != None:
            urlNext = response.urljoin(nextArr)
            yield scrapy.Request(urlNext, callback = self.parse)




