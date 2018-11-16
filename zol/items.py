# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PhoneItem(scrapy.Item):
    _id     = scrapy.Field()
    desp    = scrapy.Field()
    price   = scrapy.Field()
    name    = scrapy.Field()
    imgSrc  = scrapy.Field()
    url     = scrapy.Field()
    screenSize  = scrapy.Field()
    resolution  = scrapy.Field()
    onSaleDate  = scrapy.Field()
    osName      = scrapy.Field()
    nCpuCores   = scrapy.Field()
    cpuType     = scrapy.Field()
    cpuSpeed    = scrapy.Field()
    gpuType     = scrapy.Field()
    ram         = scrapy.Field()
    rom         = scrapy.Field()


class CarItem(scrapy.Item):
    name0       = scrapy.Field()    #名字，型号名
    name1       = scrapy.Field()    #名字，型号下面的分支，不同配置
    alpha       = scrapy.Field()    #品牌首字母，用于索引查询
    brand       = scrapy.Field()    #品牌
    factory     = scrapy.Field()    #厂商
    price       = scrapy.Field()    #厂商指导价
    level       = scrapy.Field()    #级别
    energy      = scrapy.Field()    #能源类型
    onSaleTime  = scrapy.Field()    #上市时间
    engine      = scrapy.Field()    #发动机

