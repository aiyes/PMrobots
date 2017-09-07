#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import datetime
import time
from selenium.webdriver.common.keys import Keys
from tenacity import retry,stop_after_attempt,wait_fixed



class WarnDeal(object):
    def __init__(self,browser):
        self.browser=browser


    #车辆信息弹出框处理
    def CarIfWarn(self):
        @retry(stop=stop_after_attempt(10), wait=wait_fixed(0.5))
        def CarIfwarnfirst(browser):
            ModIFT = browser.find_element_by_id('carTypeTable')
            divtab = browser.find_element_by_id('carTypeDialog')
            ModIFT.find_element_by_xpath('./tbody/tr[1]/td[1]/input').click()
            divtab.find_element_by_class_name('confirm').click()

        @retry(stop=stop_after_attempt(10), wait=wait_fixed(0.5))
        def CarIfwarnSecond(browser):
            RiskTable = browser.find_element_by_id('riskInsuranceTable')
            dialog = browser.find_element_by_id('dialogTemplet')
            RiskTable.find_element_by_xpath('./tbody/tr[1]/td[1]/input').click()
            dialog.find_element_by_class_name('confirm').click()

        try:
            CarIfwarnfirst(browser=self.browser)
        except:
            return False

        try:
            CarIfwarnSecond(browser=self.browser)
        except:
            return False
        return True

    #报价警告信息处理
    @retry(stop=stop_after_attempt(10), wait=wait_fixed(0.5))
    def Baojiawarn(self):
        #报价警告
        flag='1'#1正常，2需要人工处理，3失败
        for i in range(10):
            try:
                warn = self.browser.find_element_by_css_selector('html body div.loding_bj.noticeDialog div.float-content')
                warntext = warn.find_element_by_xpath('./div[1]').text  # 警告文字
                errordouble = re.findall('错误.+重复投保', warntext)#重复投保
                errortax = re.findall('未找到.+完税记录', warntext)#未找到完税记录
                errornot = re.findall('NORMAL', warntext)  # 无错误

                if errordouble:#如果显示重复投保
                    self.warndouble(warn=warn,warntext=warntext)
                if errortax:#如果显示税收有问题
                    self.warntax(warn=warn)
                    flag='2'
                if errornot:#如果无错误
                    warn.find_element_by_xpath("//a[text()='关闭']").click()
                    return flag
            except:
                time.sleep(0.5)
        return '3'





    #商业险日期格式错误处理
    def CommecialTimeAlter(self,result,dstr):
        if result.text=='不合法的日期格式或者日期超出限定范围,需要撤销吗?':
            result.accept()
        enddate = self.browser.find_element_by_id('commercialEndDate')
        enddate.send_keys(Keys.SPACE)
        startdate=self.browser.find_element_by_id('commercialStartDate')
        startdate.clear()
        startdate.send_keys(dstr)

    #交强险日期格式错误处理
    def CompusoryTimeAlter(self,result,dstr):
        if result.text=='不合法的日期格式或者日期超出限定范围,需要撤销吗?':
            result.accept()
        enddate = self.browser.find_element_by_name('stEndDate')
        enddate.send_keys(Keys.SPACE)
        startdate=self.browser.find_element_by_id('compulsoryStartDate')
        startdate.clear()
        startdate.send_keys(dstr)


    #处理交强险重复投保
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

    def warntax(self,warn):
        warn.find_element_by_xpath("//a[text()='关闭']").click()
        self.browser.find_element_by_id('compulsoryInput').send_keys(Keys.SPACE)
        self.browser.find_element_by_id('premiumTrial').click()







