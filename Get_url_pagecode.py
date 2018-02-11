# -*- coding: utf-8 -*-

import urllib2, time, random
COOKIE='SUB=_2A250WZIFDeThGeNM6VcV9y7MyD-IHXVXpT5NrDV6PUJbkdANLWn5kW2OFw2qPMsSFtK0SqHngbBFbIWwOw..; SUHB=0d4u7xIZLZeFix; SCF=AjoiKVevWhiaDYvE2VnmikHlNqcY0Ten93MFOqKtSHgkICAlPsVU0VSeUS_aPPCvInF-3ERlC2W-Ge_fpshtV04.; SSOLoginState=1499325013; _T_WM=89f3f972a8097adad7b053dd03868cd2' #换自己的COOKIE
header = {
    'Cache-Control' : 'max-age=0',
    'Connection' : 'keep-alive',
    'cookie' : COOKIE,
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)'
                   ' Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
    'Host':'weibo.cn',
    'Referer':'http://weibo.cn/'
     }

TIME_SLEEP_MIN = 1
TIME_SLEEP_MAX = 2

def GetPage(url):
    # print(url)
    time.sleep(random.uniform(TIME_SLEEP_MIN, TIME_SLEEP_MAX))
    try:
        request1 = urllib2.Request(url, headers=header)
        response1 = urllib2.urlopen(request1, timeout=10)
        # 将页面转化为UTF-8编码
        pageCode = response1.read()
        # print pageCode
        return pageCode
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            dir(e.reason)
            print u"连接失败,错误原因".encode('gbk'), e.reason
            if hasattr(e, 'code'):
                if e.code.real == 404:
                    return None
                print e.code

            # 将超时的错误原因输出为str格式，方便进行循环比较。
            error = e.reason.message  # str格式，timed out
            if (error == 'timed out'):
                print 'restart once again'
                return GetPage(url)
            return GetPage(url)
        else:
            print 'other error'
            return GetPage(url)

