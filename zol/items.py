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
	_id 	= scrapy.Field()
	desp 	= scrapy.Field()
	price 	= scrapy.Field()
	name 	= scrapy.Field()
	imgSrc 	= scrapy.Field()
	screenSize 	= scrapy.Field()
	resolution 	= scrapy.Field()
