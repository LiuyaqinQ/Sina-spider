# -*- coding:utf-8 -*-
#2016年8月15日，软件可以实现http软件可以实现http://www.zngirls.com/g/XXXXX/1.html'的某个图片编号范围的图片批量下载到各自名字下的文件夹
#2016年8月16日，软件完善到self.user
#8月16日，部分网址导入后报错，'gbk' codec can't encode character u'\ubc15' in position 4: illegal multibyte sequence
#部分字符从utf-8解析为unicode后无法被gkb编码，需要进行处理decode('utf-8','ignore').encode('gbk','ignore')
#2016年8月30日试图完善timeout报错问题,已经解决，并试图完成模块化处理

import re
import random
import os  
import urllib
import urllib2
import socket
import string

class xiazai:
	#初始化方法，定义一些变量
    def __init__(self):
        self.url = 'http://www.zngirls.com/g/'
        self.cookie='__cfduid=d7f4822c782bf98c06ef29b35b2b145a91472541361; Hm_lvt_1bb490b9b92efa27' \
               '8bd96f00d3d8ebb4=1476430165,1477456083,1477549594,1478678268; Hm_lpvt_1bb490b9b92' \
               'efa278bd96f00d3d8ebb4=1478678275'
        #19999,19976,18246,19916,19270,19041,18247,19610,19925,19643,19642,19551,19993
        #'16022','19626','18925', '18924','17602','18649', '18648'
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari']
       #存放程序是否继续运行的变量
        self.enable = True

    def getPage(self, url):
        try:
            request1 = urllib2.Request(url)
            response1 = urllib2.urlopen(request1, timeout=10)
            # 将页面转化为UTF-8编码
            pageCode = response1.read()
            return pageCode
        except socket.timeout, e:
            print 'onece start'
            return self.getPage(url)
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败,错误原因", e.reason,e.code
                if hasattr(e, 'code'):
                    if e.code.real == 404:
                        self.enable = False
                        print '404404'
                        return None
                            # 将超时的错误原因输出为str格式，方便进行循环比较。
                error = e.reason.message  # str格式，timed out
                print error.decode('utf-8')
                    # error = (getattr(e.reason, 'message'))
                if (error == 'timed out'):
                    print 'restart once again'
                    return self.getPage(url)

    def getPhoto_url(self,url):
        pageCode=self.getPage(url)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('''<div class="photos">.*?<img src='(.*?).jpg' alt='.*?'>''',re.S)
        items = re.findall(pattern,pageCode)
        if len(items)>0:
            print items[0]
            return items[0]
        else:
            return None

    #获取网页对应的文档题目
    def getPhoto_title(self,url):
        pageCode=self.getPage(url)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('''<title>(.*?)</title>''',re.S)
        items = re.findall(pattern,pageCode)
        # print items[0]
        judge=['\xe8\xaf\xa5\xe9\xa1\xb5\xe9\x9d\xa2\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0-\xe5\xae\x85\xe7\
        x94\xb7\xe5\xa5\xb3\xe7\xa5\x9e']
        # print items[0]
        # print judge
        # print items[0]==judge[0]
        if items[0]!=judge[0]:
            return items[0]
        else:
            return None

    #保存图片地址   
    def savePhoto(self,url):
        pageCode=self.getPage(url)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('''<title>(.*?)</title>''',re.S)
        items = re.findall(pattern,pageCode)
        return items[0]

    #设置代理IP
    def proxy_setting(self,http):
        enable_proxy = True
        proxy_handler = urllib2.ProxyHandler({"http" : http})
        null_proxy_handler = urllib2.ProxyHandler({})
        if enable_proxy:
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener(null_proxy_handler)
        urllib2.install_opener(opener)
        return None

        #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False
    #保存图片
    def saveImg(self,data,fileName):
         f = open(fileName, 'wb')
         f.write(data)
         print u"保存她的一张图片为",fileName
         f.close()

    #下载某个图册的所有照片
    def saveImg_in_a_page(self,filename_file,url_firstphoto):
        # 计数器
        i = 1
        # 创建目录操作函数
        self.mkdir(filename_file)
        # 将图片保存路径改到当前新建目录
        os.chdir(filename_file)
        self.enable = True
        while self.enable:
            if i == 1:
                url_firstphotoi = url_firstphoto + '.jpg'
                filename1 = filename_file + str(0) + str(i) + '.jpg'
            elif i < 11:
                url_firstphotoi = url_firstphoto + str(0) + str(i - 1) + '.jpg'
                filename1 = filename_file + str(0) + str(i) + '.jpg'
            else:
                url_firstphotoi = url_firstphoto + str(i - 1) + '.jpg'
                filename1 = filename_file + str(i) + '.jpg'
                # if urllib2.URLError:
                # print i
                # continue
            # print url_fistphotoi
            # print 'saving the photos in '+str(i)
            # 获取图片url解析data,需要使用新的headers
            self.proxy_setting('http://img.zngirls.com')
            data = self.getPage(url_firstphotoi)
            if self.enable and data:
                self.saveImg(data, filename1)
                i = i + 1
            else:
                break
                # 形成新目录保存文件后，转换到原始目录。

    def start(self,url_download):
        #获取当前目录路径
        currentpath=os.getcwd()
        for j in url_download:
            self.proxy_setting('http://www.zngirls.com/')
            url_new = self.url + str(j) + '/1.html'
            # 'http://www.zngirls.com/g/19612/1.html'
            # 获取图片url地址，不包括.jpg
            url_firstphoto = self.getPhoto_url(url_new)
            # 获取网址对应的图片名称
            # filename=(self.getPhoto_title(url_new))
            filename = (self.getPhoto_title(url_new))
            if not filename or not url_firstphoto:
                continue
            else:
                filename = filename.decode('utf-8', 'ignore').encode('gbk', 'ignore')
            filename_file = 'No.' + str(j) + filename
            self.saveImg_in_a_page( filename_file, url_firstphoto)
            os.chdir(currentpath)
spider=xiazai()
url=range(13449,13455)
spider.start(url)

