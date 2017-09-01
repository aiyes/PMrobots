#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import datetime
import time
from selenium.webdriver.common.keys import Keys

class WarnDeal(object):
    def __init__(self,browser):
        self.browser=browser

    #车辆信息弹出框处理
    def CarIfWarn(self):
        starttime = datetime.datetime.now()
        while True:
            nowtime=datetime.datetime.now()
            delta=nowtime-starttime
            if delta.seconds<5:
                try:
                    ModIFT = self.browser.find_element_by_id('carTypeTable')
                    divtab = self.browser.find_element_by_id('carTypeDialog')
                    ModIFT.find_element_by_xpath('./tbody/tr[1]/td[1]/input').click()
                    divtab.find_element_by_class_name('confirm').click()
                    break
                except:
                    time.sleep(0.5)
                    continue
            return False

        while True:
            try:
                RiskTable = self.browser.find_element_by_id('riskInsuranceTable')
                dialog = self.browser.find_element_by_id('dialogTemplet')
                RiskTable.find_element_by_xpath('./tbody/tr[1]/td[1]/input').click()
                dialog.find_element_by_class_name('confirm').click()
                break
            except:
                time.sleep(0.5)
        return True

    #报价警告信息处理
    def Baojiawarn(self):
        while True:
            try:
                warn = self.browser.find_element_by_css_selector('html body div.loding_bj.noticeDialog div.float-content')
                warntext = warn.find_element_by_xpath('./div[1]').text#警告文字
                errordouble = re.findall('[错误].+[重复投保]', warntext)
                errornot = re.findall('NORMAL', warntext)  # 无错误
                if errordouble:#如果显示重复投保
                    self.warndouble(warn=warn,warntext=warntext)

                if errornot:
                    warn.find_element_by_xpath("//a[text()='关闭']").click()
                    break
            except Exception as e:
                time.sleep(0.5)


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





