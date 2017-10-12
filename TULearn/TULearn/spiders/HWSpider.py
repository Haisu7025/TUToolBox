# -*- coding:utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.selector import Selector
from TULearn.items import TulearnItem


class HWSpider(scrapy.Spider):
    name = 'homework_spider'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://www.zhihu.com/"
    }

    def start_requests(self):
        return [Request("https://learn.tsinghua.edu.cn", meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        print Selector(response)
        formdate = {
            'userid': "**",
            'userpass': "**",
            'submit1': "登录"
        }
        print "login！！！！！"
        return [FormRequest.from_response(response, formdata=formdate, callback=self.after_login)]

    def after_login(self, response):
        print "login successful!!!"
        lnk = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/mainstudent.jsp'
        yield Request(lnk, self.parse)

    def parse(self, response):
        problem = Selector(response)
        yield Request("http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?language=cn", self.getClass)

    def getClass(self, response):
        for sel in response.xpath('//*[@id="info_1"]/tr/td[1]/a'):
            hzg = re.search(
                'href="(.*)([0-9]{6})"', sel.extract())
            hz = hzg.group(1)
            course_id = hzg.group(2)
            class_link = "http://learn.tsinghua.edu.cn" + hz + course_id
            yield Request(class_link, self.getClassDetails, meta={'course_id': course_id})

    def getClassDetails(self, response):
        course_id = response.meta['course_id']
        yield Request("http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_brw.jsp?course_id=" + course_id, callback=self.getHomeworkInfo)

    def getHomeworkInfo(self, response):
        for sel in response.xpath('//*[@id="info_1"]/tr[1]/td/text()'):
            ln = sel.extract()
        hn_selector_ls = response.xpath(
            '//*[@id="table_box"]/tr/td[1]/a/text()')
        ht_selector_ls = response.xpath('//*[@id="table_box"]/tr/td[3]/text()')
        is_selector_ls = response.xpath('//*[@id="table_box"]/tr/td[4]/text()')

        for i in range(len(hn_selector_ls)):
            ri = TulearnItem()
            ri['homework_name'] = hn_selector_ls[i].extract()
            ri['homework_time'] = ht_selector_ls[i + 1].extract()
            ri['lesson_name'] = ln
            ri['homework_state'] = is_selector_ls[i + 1].extract()
            yield ri
