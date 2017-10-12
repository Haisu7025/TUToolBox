# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import codecs
import mailtest
from items import TulearnItem


class TulearnPipeline(object):
    def open_spider(self, spider):
        self.msg_list = []
        self.file = codecs.open('items.json', 'w', 'utf-8')

    def close_spider(self, spider):
        mailtest.send_learn_msg(self.msg_list)
        self.file.close()  # 爬虫关闭时关闭文件

    def process_item(self, item, spider):
        ln_s = item['lesson_name'].encode("utf-8").lstrip().rstrip()
        hn_s = item['homework_name'].encode("utf-8").lstrip().rstrip()
        ht_s = item['homework_time'].encode("utf-8").lstrip().rstrip()
        hs_s = item['homework_state'].encode("utf-8").lstrip().rstrip()
        print "课程名:", ln_s
        print "作业名:", hn_s
        print "截止时间:", ht_s
        print "状态:", hs_s
        now = datetime.datetime.now()
        ddl = datetime.datetime.strptime(
            ht_s + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        time_msg = str(ddl - now)
        if hs_s.find("尚") != -1:
            # not submmited
            self.msg_list.append("课程【" + ln_s + "】有未提交作业:" + hn_s +
                                 "(截止时间:" + ht_s + ")，距离结束还有" + time_msg + "，请抓紧完成或提交")
