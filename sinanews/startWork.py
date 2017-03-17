# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("./sinanews")
reload(sys)
import time

# 获取当前日期
def GetDate():
    string = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return string

def initialization():
    # 设置目标日期
    # date = GetDate()
    date = "2017-03-03"
    resultPath = "../result/"
    return date,resultPath

if __name__ == '__main__':
    print "Start ... "
    os.system("scrapy crawl sinanews")
    print "Work Done!"