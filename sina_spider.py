# -*- coding: utf-8 -*-
from Get_url_pagecode import *
import re
import urllib2
import urllib
import time
import os

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
		print u"保存她的一张图片为", fileName
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
				print u"连接失败,错误原因", e.reason
				print 'restart'+str(num)
				return self.GetPage_photo(url,num+1)
				# if hasattr(e, 'code'):
				# 	if e.code.real == 404:
				# 		return None
				# # 将超时的错误原因输出为str格式，方便进行循环比较。
				# error = e.reason.message  # str格式，timed out
				# if (error == 'timed out'):
				# 	print 'restart once again'
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
			print u"新建了名字叫做", path, u'的文件夹'
			# 创建目录操作函数
			os.makedirs(path)
			return True
		else:
			# 如果目录存在则不创建，并提示目录已存在
			print u"名为", path, '的文件夹已经创建成功'
			return False

	def start(self ,filename , url):
		# pattern = re.compile('''<img src="(.*?)" alt="" class="c">''', re.S)
		pattern = re.compile(r'''<a href=".*?rl=11"><img src="(.*?)" alt='' class="c"/></a>''', re.S)
		index=1
		num1=1
		currentpath = os.getcwd()
		self.mkdir(filename)
		os.chdir(filename)
		while self.enable:
			if index==1:
				url_new=url
			else:
				url_new=url+'1&page='+str(index)
			print url_new
			pagecode=GetPage(url_new)
			#将当前页面输出
			# filename='page.txt'
			# self.saveImg(pagecode,filename)

			Photo_url=self.get_pageconten(pagecode,pattern)
			if Photo_url:
				length=len(Photo_url)
				print ('this page contain '+str(length)+' photos in '+str(index)+' page')
				for i in range(length-1):
					filename1 = filename + str(num1)+'.jpg'
					url1 = (Photo_url[i+1])
					url2=url1.replace('square','large')
					data = self.GetPage_photo(url2,num1)
					if data:
						self.saveImg(data, filename1)
						num1=num1+1
				index=index+1
			else:
				print u'程序抓取完毕，请检查'
				break
		os.chdir(currentpath)
# mm=spider()
# mm.start()