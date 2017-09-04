#!/usr/bin/python
# -*- coding: UTF-8 -*-
from APP.TBRobots import Robot
import time
import threading

#------------------------------------------
#开机自动运行部分
class Run(object):
    def __init__(self):
        self.robots = Robot()
        self.browser, self.cookies = self.robots.login()
        self.sleeptime = 0
        sleeptime = 0
        t1 = threading.Thread(target=self.timesleep)
        t1.start()

    def timesleep(self):
        while True:
            while self.sleeptime <= 240:
                time.sleep(1)
                self.sleeptime += 1
                print(self.sleeptime)
            self.browser.refresh()
            self.sleeptime = 0

    def set_zero(self):
        self.sleeptime = 0
        return self.sleeptime

RB = Run()

#--------------------------------------------
#检查网页打开是否正确
def is_ok():
    global RB
    RB.browser.refresh()
    righturl='http://issue.cpic.com.cn/ecar/view/portal/page/quick_quotation/quick_quotation.html'
    while True:
        if righturl in RB.browser.current_url:
            break
        else:
            RB.robots.login()



class Method(object):
    def __init__(self):
        global RB
        self.run=RB
        self.robots=RB.robots
        self.cookies=RB.cookies
        self.browser=RB.browser

    def AskPrice_SH_MN(self,dic):
        self.run.set_zero()
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
        self.run.set_zero()
        while True:
            try:
                info=self.robots.findcarinfoWD(browser=self.browser,LicenseNo=dic['LicenseNo'])
                if info == False:
                    message={'isSuccess':'500','message':'车辆信息有误'}
                    return message
            except:
                pass





