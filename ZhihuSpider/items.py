# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    userid = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    business = scrapy.Field()
    gender = scrapy.Field()
    employment = scrapy.Field()
    position = scrapy.Field()
    education = scrapy.Field()
    major = scrapy.Field()
    follower_num = scrapy.Field()
    followee_num = scrapy.Field()
    ask_num = scrapy.Field()
    answer_num = scrapy.Field()
    post_num = scrapy.Field()
    agree_num = scrapy.Field()
    thanks_num = scrapy.Field()
    pass
