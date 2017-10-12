## 清华大学脚本工具箱

### TULearn

* 清华大学网络学堂作业邮件提醒工具

### TUNet

* 清华大学校园网登录脚本

### 使用说明
初次使用，运行

```
python conf_init.py -u [username for tsinghua] -p [password for tsinghua]
```

检查生成的user.conf是否对应正确的用户名和密码，再运行其他功能

### 更新日志

#### 2017.10.12

* 将TULearn和TUNet从原仓库移到这里
* 更新了configparser部分，从user.conf中读取用户和服务器配置信息，但似乎对mac系统不够支持
* 更新README
* 完成configparser部分