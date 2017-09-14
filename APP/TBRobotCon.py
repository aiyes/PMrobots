#!/usr/bin/python
# -*- coding: UTF-8 -*-
from APP.TBRobots import Robot
from selenium import webdriver
import time
import threading
import requests,re,queue
from APP.TBconfig import sleeptime,drivepath,quoteurl
from APP.TBrobotSqlhelper import Car
from APP.TBRobotBackControl import CarinfoSHDic

#------------------------------------------
#开机自动运行部分
class Run(object):
    def __init__(self):
        self.drivepath=drivepath
        self.quoteurl=quoteurl
        self.robots = Robot()
        self.browser, self.cookies ,self.cookiestr= self.robots.login()
        self.ultilizetime=sleeptime
        self.sleeptime = 0
        t1 = threading.Thread(target=self.timesleep)
        self.windowpool=self.WindowQue()
        self.windowpool.put(self.browser)#将第一个窗口也加入池子
        t1.start()

    def timesleep(self):
        print(self.sleeptime)
        while True:
            while self.sleeptime <= self.ultilizetime:
                time.sleep(1)
                self.sleeptime += 1
                if self.sleeptime%60==0:
                    print(self.sleeptime)
            self.browser.refresh()
            self.is_ok()
            self.sleeptime = 0

    def is_ok(self):
        righturl = 'http://issue.cpic.com.cn/ecar/view/portal/page/quick_quotation/quick_quotation.html'
        while True:
            if righturl in self.browser.current_url:
                break
            else:
                self.browser, self.cookies, self.cookiestr =self.robots.login()

    def set_zero(self):
        self.sleeptime = 0
        return self.sleeptime

    def WindowQue(self):
        windowpool=queue.Queue(maxsize=4)
        def openwindow(drivepath,quoteurl,cookies,windowpool):
            browser = webdriver.Chrome(drivepath)
            browser.get(quoteurl)
            browser.delete_all_cookies()
            for cookie in cookies:
                browser.add_cookie(cookie)
            browser.get(quoteurl)
            windowpool.put(browser)

        for i in range(3):
            t1=threading.Thread(target=openwindow,args=(self.drivepath,self.quoteurl,
                                    self.cookies,windowpool))
            t1.start()
        return windowpool


RB = Run()

#--------------------------------------------
#检查网页打开是否正确
def is_ok():
    global RB
    righturl='http://issue.cpic.com.cn/ecar/view/portal/page/quick_quotation/quick_quotation.html'
    head = {'Host': 'issue.cpic.com.cn',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie': RB.cookiestr}
    while True:
        req = requests.get(url=righturl, headers=head)
        s = re.findall('立即登录', req.text)
        if s:
            print('接口检验错误，重新登录中....')
            RB.browser, RB.cookies, RB.cookiestr=RB.login()
        else:
            print('接口正常，开始工作')
            break

#关闭窗口
def windowclose(browser):
    browser.close()

#询价方法
class Method(object):
    def __init__(self):
        global RB
        self.run=RB
        self.robots=RB.robots
        self.cookies=RB.cookies
        self.browser=RB.browser
        self.cookiestr=RB.cookiestr
        self.windowpool=RB.windowpool

    def CarInfoFind(self,LicenseNo):
        self.run.set_zero()
        car = Car(LicentseNo=LicenseNo)
        carinDB = car.SearchInDatebase()
        if carinDB:
            message=CarinfoSHDic(car_data_database=carinDB)
            return message
        else:
            carinJK=self.robots.CarinfoSH(cookiestr=self.cookiestr,LicenseNo=LicenseNo)
            car.InsertCarInfo(dic=carinJK)
            carinDB=car.SearchInDatebase()
            message=CarinfoSHDic(car_data_database=carinDB)
            return message

    def AskPrice_SH_MN(self,dic):
        self.run.set_zero()
        trytimes=0
        while True:
            try:
                info,browser = self.robots.findcarinfoSH(windowpool=self.windowpool, LicenseNo=dic['carNo'])
                if info==False:
                    message={'isSuccess':'450','message':'车辆信息有误'}
                    return message
                baojia = self.robots.Baojia(browser=browser, dic=dic,windowpool=self.windowpool)
                return baojia
            except:
                if trytimes<3:
                    trytimes += 1
                    if self.browser.current_url=='http://issue.cpic.com.cn/ecar/view/portal/page/quick_quotation/quick_quotation.html':
                        self.browser.refresh()
                    else:
                        self.browser,self.cookies=self.robots.login()
                else:
                    message = {'isSuccess': '500', 'message': '服务器异常'}
                    return message

    def AskPrice_WD_MN(self,dic):
        self.run.set_zero()
        while True:
            try:
                info=self.robots.findcarinfoWD(browser=self.browser,LicenseNo=dic['LicenseNo'])
                if info == False:
                    message={'isSuccess':'450','message':'车辆信息有误'}
                    return message
            except:
                pass





