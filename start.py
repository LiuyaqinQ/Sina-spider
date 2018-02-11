from sina_spider_4 import spider
import sys

try:
	origin = sys.stdout
	ff = open('file.txt', 'w')
	sys.stdout = ff
	mm = spider()
	mm.start(url='https://weibo.cn/aimisheimiss?filter=2&page=', filename='aimisheimiss')
finally:
	sys.stdout = origin
	ff.close()


