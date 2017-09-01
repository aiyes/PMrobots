#!/usr/bin/python
# -*- coding: UTF-8 -*-
from APP.TBRobots import Robot
import time
import threading

#------------------------------------------
#开机自动运行部分
try:
    RB = Robot()
    browser, cookies = RB.login()
except Exception as e:
    print(e)

sleeptime=0
def timesleep():
    global browser
    global sleeptime
    while True:
        while sleeptime<=40:
            time.sleep(1)
            sleeptime+=1
        browser.refresh()
        sleeptime=0


t1=threading.Thread(target=timesleep)
t1.start()

#--------------------------------------------

def set_zero():
    global sleeptime
    sleeptime=0

class Method(object):
    def __init__(self,robots=RB,browser=browser,cookies=cookies):
        self.robots=robots
        self.browser=browser
        self.cookies=cookies


    def AskPrice_SH_MN(self,dic):
        while True:
            try:
                info = self.robots.findcarinfoSH(browser=self.browser, LicenseNo=dic['carNo'])
                if info==False:
                    message={'isSuccess':'500','message':'车辆信息有误'}
                    return message
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

    def AskPrice_WD_MN(self,dic):
        while True:
            try:
                info=self.robots.findcarinfoWD(browser=self.browser,LicenseNo=dic['LicenseNo'])
                if info == False:
                    message={'isSuccess':'500','message':'车辆信息有误'}
                    return message
            except:
                pass





