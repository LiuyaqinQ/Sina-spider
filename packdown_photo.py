# -*- coding: utf-8 -*-
#保存相册图片到文件夹
import sina_spider
num=sina_spider.spider()
url=['http://weibo.cn/album/39053726707323420000002589379191?rl=1']
# filhttp://weibo.cn/album/39053726707323420000002589379191?rl=1']
filenames=['ximengyao']
lengh_array=len(url)
for i in range(lengh_array):
	num.start(filenames[i],url[i])

#['http://weibo.cn/album/39245758768052460000005226275418?rl=1','http://weibo.cn/album/38931278111998630000002281056745?rl=1',
# 'http://weibo.cn/album/39202730826867210000002001658431/?rl=1','http://weibo.cn/album/39859864597770110000005886264332?rl=1',
# 'http://weibo.cn/album/39199898665664230000001819354643?rl=1']