#!/usr/bin/python
# -*- coding: UTF-8 -*-
from APP.TBRobots import Robot
import time
import threading

#------------------------------------------
#开机自动运行部分
RB = Robot()
browser, cookies = RB.login()
sleeptime=0
def timesleep():
    global browser
    global sleeptime
    while True:
        while sleeptime<=30:
            time.sleep(1)
            sleeptime+=1
            print(sleeptime)
        browser.refresh()
        sleeptime=0

def set_zero():
    global sleeptime
    sleeptime=0

t1=threading.Thread(target=timesleep)
t1.start()

#--------------------------------------------


class Method(object):
    def __init__(self,robots=RB,browser=browser,cookies=cookies):
        self.robots=robots
        self.browser=browser
        self.cookies=cookies


    def AskPrice_SH_MN(self,dic):
        while True:
            try:
                info = self.robots.findcarinfoSH(browser=self.browser, LicenseNo=dic['LicenseNo'])
                baojia = self.robots.Baojia(browser=self.browser, dic=dic)
                self.browser.refresh()
                return baojia
            except:
                if self.browser.current_url=='http://issue.cpic.com.cn/ecar/view/portal/page/quick_quotation/quick_quotation.html':
                    self.browser.refresh()
                    continue
                else:
                    self.browser,self.cookies=self.robots.login()
                    continue





