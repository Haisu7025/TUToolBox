#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_learn_msg(msg_list=[]):
    sender = 'from@runoob.com'
    receivers = ['tsinghua_yuhs15@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    strr = ""
    for msg in msg_list:
        strr = strr + msg + "\n"
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(strr, 'plain', 'utf-8')
    message['From'] = Header("aaa", 'utf-8')
    message['To'] = Header("bbb", 'utf-8')

    subject = '网络学堂提醒'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('127.0.0.1')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
