# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaonvlangItem(scrapy.Item):
    # define the fields for your item here like:
    user_id=scrapy.Field()
    album_id=scrapy.Field()
    title=scrapy.Field()
    picurl=scrapy.Field()

