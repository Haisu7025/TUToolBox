# coding=utf-8

import requests
import urlparse
import re


def get_lessonname(url="", headers={}):
    res_qu = urlparse.urlparse(url)
    res_qs = urlparse.parse_qs(res_qu.query, True)
    params = {'module_id': res_qs['module_id'],
              'filePath': res_qs['filePath'],
              'course_id': res_qs['course_id'],
              'file_id': res_qs['file_id']}
    r = requests.head(res_qu.scheme + "://" + res_qu.netloc +
                      res_qu.path, params=params, headers=headers)
    t = re.findall(r'attachment;filename="(.*)"',
                   r.headers['Content-Disposition'])[0]
    return t.decode('gbk')
