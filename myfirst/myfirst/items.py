# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BdtbItem(scrapy.Item):
    title = scrapy.Field()
    message = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    userNum = scrapy.Field()
    postNum = scrapy.Field()
