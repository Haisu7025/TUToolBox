# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import codecs
import mailtest
import urlparse
import scrapy
import requests
from items import HWItem, LFItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem


class HWPipeline(object):
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


class LFPipeline(scrapy.pipelines.files.FilesPipeline):
    item_list = []

    def get_media_requests(self, item, info):
        print "media requests"
        self.item_list.append(item)
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={"lessoname": item['lessonname'], "filename": item['filename']})

    def item_completed(self, results, item, info):
        print "COMPLETED"
        file_paths = [x['path'] for ok, x in results if ok]

        if not file_paths:
            raise DropItem("Item contains no files")
        #item['file_paths'] = file_paths
        return item

    def file_path(self, request, response=None, info=None):
        lessonname = ""
        filename = ""
        for item in self.item_list:
            if item['file_urls'][0] == request.url:
                print "url MATCH!!!!"
                lessonname = item['lessonname']
                filename = item['filename']
                break
        path = ''.join([lessonname, "/", filename])
        return path
