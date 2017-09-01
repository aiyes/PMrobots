#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import datetime
from selenium.webdriver.common.keys import Keys

class WarnDeal(object):
    def __init__(self,browser):
        self.browser=browser

    def Baojiawarn(self):
        while True:
            warn = self.browser.find_element_by_css_selector('html body div.loding_bj.noticeDialog div.float-content')
            warntext = warn.find_element_by_xpath('./div[1]').text#警告文字
            errordouble = re.findall('[错误].+[重复投保]', warntext)
            errornot = re.findall('NORMAL', warntext)  # 无错误
            if errordouble:#如果显示重复投保
                self.warndouble(warn=warn,warntext=warntext)

            if errornot:
                warn.find_element_by_xpath("//a[text()='关闭']").click()
                break


    def warndouble(self,warn,warntext):
        date = re.findall('(\d+)年(\d+)月(\d+)日', warntext)
        c = ''
        for i in date[1]:
            c = c + ' ' + i
        d = datetime.datetime.strptime(c, ' %Y %m %d')
        today = datetime.datetime.now()
        delta = d - today
        warn.find_element_by_xpath("//a[text()='关闭']").click()
        if delta.days >= 30:
            self.browser.find_element_by_id('compulsoryInput').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('premiumTrial').click()#不选择车强险后再进行报价





