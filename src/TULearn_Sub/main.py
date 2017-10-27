## -*- coding:utf-8 -*-
# Oct 26, 2017
# Unix/Linux only, must have access to 'learn.tsinghua.edu.cn'
# Dependencies: requests_2.18.4+ - https://pypi.python.org/pypi/requests#downloads, requests-x.xx.x.tar.gz

import re, json #, requests 
import os, getpass, datetime

## -*- Settings -*-
# Default destination path in Unix/Linux will be '/Users/UserName/Desktop/LearnWeb/MicroEcnomics'
# DO NOT change this item.
DesktopPath = os.path.join(os.path.expanduser("~"), 'Desktop')

# You can use desktopPath or whatever you like, default "DesktopPath+'/LearnWeb'".
home_path = DesktopPath+'/LearnWeb'

# To disable HTTPS link, change 'https' in host to 'http', default enabled.
host = 'https://learn.tsinghua.edu.cn'

# Change the max filesize(MB) limit to deny the download when syn, default 20.
maxsize = 20

# Move files in '电子教案' to root folder in each course, default enabled.
vroot = True

# Detailed output, default disabled.
detailed_output = False


## -*- Program Starts -*-
def mkdir(path):
    global detailed_output
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print '成功创建目录',path
        return True
    else:
        if detailed_output:
            print '读取已存在目录',path
    return False

g_cookie = ''
new_list = []
bad_network = False

try:  
    import requests
except ImportError:  
    print '* Install module \'requests\' with command "sudo pip install requests"\nor visit "https://pypi.python.org/pypi/requests#downloads"\n'
    os._exit(-1)

def get_course_list():
    global g_cookie,host,detailed_output
    begin = datetime.datetime.now()

    # 获取课程列表网页
    get_url = host+r'/MultiLanguage/lesson/student/MyCourse.jsp?language=cn'
    headers = {'Cookie': g_cookie}
    resp = requests.get(get_url, headers=headers, verify=True, allow_redirects=False)

    # 解析列表
    patt = [r'<!--td height="25" class="tableNO">(.*?)</td-->',
            r'<a href="(.*?)" target="_blank">',
            r'(.*)</a><span style="color:red"></span></td>',
            r'<td width="15%" ><span class="red_text">(.*?)</span>个未交作业</td>',
            r'<td width="15%" ><span class="red_text">(.*?)</span>个未读公告</td>',
            r'<td width="15%" ><span class="red_text">(.*?)</span>个新文件</td>']
    res = []
    courses = []

    for columnid in range(patt.__len__()):
        res.append(re.findall(patt[columnid], resp.text.encode('utf8')))

    for courseid in range(res[0].__len__()):
        tmp_course = (res[0][courseid], res[1][courseid], re.findall("(.*)\(\d*\)\(.*\)$",res[2][courseid].strip())[0], res[3][courseid], res[4][courseid], res[5][courseid])
        courses.append(tmp_course)
    print 
    print "Retrived", courses.__len__(), "Courses."
    if detailed_output:
        for t in courses:
            print t[2]
    end = datetime.datetime.now()
    #print (end-begin)
    if (end-begin) > datetime.timedelta(seconds=1.0):
        print '\n 【当前网络环境较差】'
        bad_network = True
    return courses


def login_web(account_dict):
    global g_cookie, username, password,host
    url = host + '/MultiLanguage/lesson/teacher/loginteacher.jsp'
    data = account_dict

    # 提交用户名与密码进行登陆, 初始化g_cookie
    resp = requests.post(url, data=data, allow_redirects=False)
    #print resp.headers['set-cookie']
    g_cookie = resp.headers['set-cookie'].replace(r' path=/,','').replace(r' path=/','')


def get_file_info(url_raw, t_cookies):
    r = requests.head(url_raw, headers={'Cookie': t_cookies})
    #print r.headers
    #print '.',
    t = re.findall(r'attachment;filename="(.*)"', r.headers['Content-Disposition'])[0]
    s = r.headers['Content-Length']
    return (t.decode('gbk').encode('utf8'),s)


def get_course_detail(course):
    global host
    course_url = host + course[1]
    resp = requests.get(course_url, headers ={'Cookie': g_cookie}, verify=True, allow_redirects=False)
    detail_page = resp.text.encode('utf8')
    course_cookie = resp.headers['set-cookie'].replace(r' path=/,','').replace(r' path=/','')
    announce_url = re.findall(r'<a href="(.*)" target="content_frame" >课程公告</a>', detail_page)[0]
    file_url = re.findall(r'<a href="(.*?)" target="content_frame" >课程文件</a>', detail_page)[0]
    assignment_url = re.findall(r'<a href="(.*)" target="content_frame" >课程作业</a>', detail_page)[0]
    #print 'resp.text:',resp.text
    #print 'file_url:',file_url

    resp = requests.get(host+file_url, headers = {'Cookie': course_cookie}, verify=True, allow_redirects=False)
    filelist_cookie = resp.headers['set-cookie'].replace(r' path=/,','').replace(r' path=/','')
    filelist_page = resp.text.encode('utf8')
    tables = re.findall(r'<table>([.\s]*)</table>', filelist_page)
    #print tables.__len__()

    folder_names = re.findall(r';NN_showImage\(\d,\d\)">(.*?)</td>', filelist_page)
    #print 'filelist_page',filelist_page
    #print 'folder_names:',folder_names

    patt = [r'<td width="80">(\d*?)</td>'  # 序号
        , r'left=100,top=100"\);\'>(.*?)</a></td>-->'  # 下载链接
        , r'<a target="_top" href="(.*)" >'  # 标题
            # ,r'<td width="300" align="center">(.*)</td>'  #简介
        , r'<td width="80" align="center">(.*)</td>'  # 大小
        , r'<td width="100" align="center">(.*)</td>'  # 上传日期
            # ,r"<td width='100' align='center'>(.*)\s*</td>",  #新文件
            ]

    folder = []
    tables = re.findall('<table \s*?id="table_box" cellspacing="1" cellpadding="0">([\s\S]*?)</table>', filelist_page)
    for folder_i in range(tables.__len__()):
        res = []
        for i in range(patt.__len__()):
            res.append(re.findall(patt[i], tables[folder_i]))

        tListInOneFolder = []
        for j in range(res[folder_i].__len__()):
            tTouple = ()
            for k in range(patt.__len__()):
                tTouple += (res[k][j],)
            tTouple += get_file_info(host+tTouple[2],course_cookie)
            tListInOneFolder.append(tTouple)
        folder.append(tListInOneFolder)
        #print 'Retrived', tListInOneFolder.__len__(), 'file in folder', folder_i
    #print
    #print folder.__len__(), 'folders got:',folder
    return (folder, folder_names, course_cookie)


def syn_file_in_course(course, folder_names, folders, t_cookie):
    global home_path, host, new_files, maxsize, vroot, detailed_output
    passed = 0
    new = 0
    for i in range(folders.__len__()):  #got 3 folder
        if folder_names[i]=='电子教案' and vroot:
            folder_path = home_path + '/' + course[2]
        else:
            folder_path = home_path + '/' + course[2] + '/' + folder_names[i]
        #print 'folder_path',folder_path
        mkdir(folder_path)
        for file in folders[i]:    #got 14 files in folder[0]
            file_path = folder_path + '/' + file[5]
            if os.path.exists(file_path) and os.path.getsize(file_path)==int(file[6]):
                passed += 1
                if detailed_output:
                    print file[5],"文件完整，跳过"
            else:
                if int(file[6])>(maxsize*1024*1024):
                    print file[5],'超过'+str(maxsize)+'M:',int(file[6])/1024.00/1024.00,'MB'
                else:
                    new += 1
                    new_list.append('['+course[2]+']: '+file[5])
                    print "正在同步:",file[5], '文件大小:',int(file[6])/1024.00/1024.00,'MB'
                    r = requests.get(host+file[2], headers = {'Cookie': t_cookie})
                    with open(file_path, "wb") as code:
                        code.write(r.content)
    return new,passed


def _init_cfg(t):
    # 获取当前路径
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = curr_dir + os.sep + "acc.cfg"
    if (os.path.exists(config_file)) and t == 1:
        with open(config_file, 'r') as json_file:
            account = json.load(json_file)
    else:
        username = raw_input("Input username: ")
        password = getpass.getpass("Please input your password, (非加密本地保存，注意PC安全):")
        account = {'userid':username, 'userpass':password,'submit1':'%E7%99%BB%E5%BD%95'}  # 数据
        with open(config_file, 'w') as json_file:
            json.dump(account, json_file, ensure_ascii=False)
    #print account
    return account


if __name__ == '__main__':
    try:
        # *-- 登录学堂 --*
        res = login_web(_init_cfg(1))
        
        # 记录运行开始时刻
        begin = datetime.datetime.now()

        # *-- 获取课程列表 --*
        courses = get_course_list()

        # *-- 账户登录失败允许重新输入凭据 --*
        while courses.__len__() == 0:
            print '账户验证失败'
            begin = datetime.datetime.now() #更新运行时刻
            res = login_web(_init_cfg(0))
            courses = get_course_list()

        # *-- 同步课程文件 --*
        new = 0
        for course in courses:
            print "\n>>", course[2]
            (folders, folder_names, course_cookie) = get_course_detail(course)
            (new_files,passed) = syn_file_in_course(course, folder_names, folders, course_cookie)
            new += new_files
            print '获取到',new_files,'个新文件, 跳过',passed,'个完整文件'
    
    except KeyboardInterrupt:
        print "\n>> *User aborted operation\n"

    else:
        end = datetime.datetime.now()
        print '\n-*- ',(courses.__len__()),'门课程同步完毕, 下载了',new,'个新文件, 用时', end-begin ,' -*-'
        if bad_network:
            print '网络环境较差'
        if new_list.__len__():
            for str in new_list:
                print str
        print 

    # *-- 读取课程作业 --*


    # *-- 读取课程公告 --*

