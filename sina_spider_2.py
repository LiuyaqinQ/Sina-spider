# -*- coding: utf-8 -*-
from Get_url_pagecode import *
import re
import urllib2
import urllib
import time
import os
import sys

class spider:
	def __init__(self):
		self.enable='True'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

	def get_pageconten(self,pagecode,pattern):
		if pagecode:
			#pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
			result = re.findall(pattern, pagecode)
			if result:
				return result
			else:
				return None
		return None

	def saveImg(self, data, fileName):
		f = open(fileName, 'wb')
		f.write(data)
		print u"保存她的一张图片为".encode('gbk'), fileName
		f.close()

	def GetPage_photo(self,url,num):
		time.sleep(random.uniform(1, 2))
		try:
			request1 = urllib2.Request(url,headers=self.headers)
			response1 = urllib2.urlopen(request1)
			# 将页面转化为UTF-8编码
			pageCode = response1.read()
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				dir(e.reason)
				print u"连接失败,错误原因".encode('gbk'), e.reason
				print 'restart'+str(num)
				return self.GetPage_photo(url,num+1)
				# 	return GetPage(url)
			# 创建新目录

	def mkdir(self, path):
		path = path.strip()
		# 判断路径是否存在
		# 存在     True
		# 不存在   False
		isExists = os.path.exists(path)
		# 判断结果
		if not isExists:
			# 如果不存在则创建目录
			print u"新建了名字叫做".encode('gbk').encode('gbk'), path, u'的文件夹'.encode('gbk')
			# 创建目录操作函数
			os.makedirs(path)
			return True
		else:
			# 如果目录存在则不创建，并提示目录已存在
			print u"名为".encode('gbk'), path, u'的文件夹已经创建成功'.encode('gbk')
			return False

	def proxy_setting(self, http):
		enable_proxy = True
		proxy_handler = urllib2.ProxyHandler({"http": http})
		null_proxy_handler = urllib2.ProxyHandler({})
		if enable_proxy:
			opener = urllib2.build_opener(proxy_handler)
		else:
			opener = urllib2.build_opener(null_proxy_handler)
		urllib2.install_opener(opener)
		return None

	def start(self ,filename , url):
		origin = sys.stdout
		f = open('file.txt', 'w')
		sys.stdout = f
		self.proxy_setting('http://weibo.cn/')
		#图片计数器
		num1=1
		#获取当前目录，然后新建目录保存图片
		currentpath = os.getcwd()
		#建立目录
		self.mkdir(filename)
		#改变目录到指定目录
		os.chdir(filename)
		#获取默认第一页网页信息，用来筛选
		url_new = url + str(1)
		pagecode = GetPage(url_new)
		##筛选当前页面总页码
		# pattern_pagenumber=re.compile('''<div class="pa" id="pagelist"><form action=.*?&nbsp;1/(.*?)\xe9\xa1\xb5</div></form></div>''',re.S)
		# pattern = re.compile('''<img src="(.*?)" alt="" class="c">''', re.S)
		# pattern = re.compile(u'''</span>&nbsp;[<a href="(*.?)">[\u4e00-\u9fa5]{3}\d[\u4e00-\u9fa5]]</div><div>''', re.S)
		# pattern = re.compile(u'''/span>&nbsp;[<a href="(*.?)">[\u4e00-\u9fa5]{3}\d''', re.S)
		# pattern = re.compile(r'''<span class="cmt">(.*?)</span><span class="ctt">(.*?)</a></span>&nbsp;[<a href="(.*?)">\xe7\xbb\x84\xe5\x9b\xbe\xe5\x85\xb1\x39\xe5\xbc\xa0</a>]''',re.S)
		#各种匹配不成功，将[替换为\D后搜索成功，并将后续文字改变为utf-8编码,筛选当前页面图总计
		pattern_pagenumber=re.compile('''<div class="pa" id="pagelist"><form action=.*?&nbsp;1/(.*?)\xe9\xa1\xb5</div></form></div>''',re.S)
		print pattern_pagenumber
		pagenumber=int((self.get_pageconten(pagecode,pattern_pagenumber))[0])
		#按照页面进行筛选组图，然后进入组图页码筛选高清图片进行保存
		for index in range(1,pagenumber+1):
			#根据页面页码，获取当前页面url地址
			url_new = url + str(index)
			#打印当前遍历url详细信息
			print 'this is a new page '+url_new
			#获取当前页面信息
			self.proxy_setting('http://weibo.cn/')
			pagecode = GetPage(url_new)
			#筛选当前页码对应的图册url地址
			pattern1 = re.compile(r'''</span>&nbsp;\D<a href="(.*?)">\xe7\xbb\x84\xe5\x9b\xbe\xe5\x85\xb1''', re.S)

			#获取单个消息中所有图片url,并打印
			Photo_url = self.get_pageconten(pagecode, pattern1)
			print 'thera are the following photo packing url in this page '
			print Photo_url
			#如果筛选图册存在，则下载
			if Photo_url:
				#对当前页面对应的多个图册进行寻找
				for photo_url in Photo_url:
					#获取每个图册对应的url
					self.proxy_setting('http://weibo.cn/')
					pagecode_new=GetPage(photo_url)
					#设定图册中图片搜索地址
					pattern=re.compile(u'''<img src="(.*?)" alt=".*?...">''',re.S)
					#筛选当前图册对应的图片url
					Photo_url_new = self.get_pageconten(pagecode_new, pattern)
					print 'there are the following photos in this photo packing: '
					print Photo_url_new
					if Photo_url_new:
						self.proxy_setting('http://ww4.sinaimg.cn/')
						#对于图册中每个图片地址进行下载
						for url_new_one in Photo_url_new:
							#对应每个组图进行筛选图片地址并下载
							filename1 = filename + str(num1) + '.jpg'
							#将图片对应的180的缩略图改为大图地址
							url2=url_new_one.replace('thumb180','large')
							#获取图片地址对应图片源代码
							data = self.GetPage_photo(url2,num1)
							#如果图片源代码存在，就下载
							if data:
								self.saveImg(data, filename1)
								#图片下载后自动增加编码
								num1=num1+1
			else:
				print u'程序抓取完毕，请检查'.encode('gbk')
		os.chdir(currentpath)
		sys.stdout = origin
		f.close()
mm=spider()
mm.start(url='http://weibo.cn/dkvision?filter=2&page=',filename='test')
#http://weibo.cn/tuigod  tuigod
#http://weibo.cn/u/2623416535  hemiaoyan
#http://weibo.cn/u/1961857111 lixueting
#http://weibo.cn/lxhjx  funnny1
#http://weibo.cn/lengxiaohua funny2
#http://weibo.cn/jokewin?filter=2 funny3
#http://weibo.cn/u/3884592975?filter=2 funny4
#http://weibo.cn/209992419 scenery
#http://weibo.cn/511297898?filter=2 scenery2