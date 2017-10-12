#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import urllib2
import sys
import getopt
import md5


# username = sys.argv[0]
# password = sys.argv[1]
def usage_help():
    print \
        '''
    login [-u] username [-p] password
    '''
    return


opts, args = getopt.getopt(sys.argv[1:], "u:p:h")

username = ""
password = ""

for op, value in opts:
    if op == "-u":
        # account
        username = value
    elif op == "-p":
        # password
        password = value
    elif op == "-h":
        # help
        usage_help()
        sys.exit()
        pass

if username == "" or password == "":
    print "Blank username or password!"
    sys.exit()


m1 = md5.new()
m1.update(password)

headers = {'UserAgent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'};
values = {'action': 'login', 'username': username,
          'password': m1.hexdigest(), 'ac_id': '1'};
data = urllib.urlencode(values)
ins_pos = data.index('password=') + 9
data = data[:ins_pos] + '{MD5_HEX}' + data[ins_pos:];

request = urllib2.Request(
    "https://net.tsinghua.edu.cn/do_login.php", headers=headers, data=data);
response = urllib2.urlopen(request)

res = response.read()

if res == "Login is successful.":
    # 登录成功
    request = urllib2.Request(
        "https://net.tsinghua.edu.cn/rad_user_info.php", headers=headers, data=data);
    response = urllib2.urlopen(request)
    res = response.read()
    res_s = res.split(",")

    print "登录成功，本月已用流量", int(res_s[6]) / 1000 / 1000, "M"
elif res == "IP has been online, please logout.":
    # 已经在线
    print "您已经在线,是否下线？(y/n)"
    logout_confirm = raw_input()
    if logout_confirm == "y":
        values = {'action': 'logout'}
        data = urllib.urlencode(values)
        request = urllib2.Request(
            "https://net.tsinghua.edu.cn/do_login.php", headers=headers, data=data);
        pass
        response = urllib2.urlopen(request)
        print response.read()
    elif logout_confirm == "n":
        print "保持在线"
        sys.exit()
