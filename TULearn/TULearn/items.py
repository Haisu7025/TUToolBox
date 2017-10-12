# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TulearnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    lesson_name = scrapy.Field()  # 课程名
    homework_name = scrapy.Field()  # 作业名
    homework_time = scrapy.Field()  # 作业ddl
    homework_state = scrapy.Field()
    pass
