#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests,time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from APP.TBRobotBackControl import Method_ASK_TB,Method_Get_TB,ImageCode
import copy



url='http://issue.cpic.com.cn/ecar/view/portal/page/common/login.html'
testcert='530302199406170354'

class Robot(object):
    def __init__(self,url=url,cert=testcert):
        self.url=url
        self.cert=cert
        self.browser = webdriver.Chrome()


    def login(self):
        '''
        # profile
        fp = webdriver.FirefoxProfile()
        fp.set_preference('browser.download.folderList', 2)
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.dir', './yourfolder/')
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/jpeg')'''

        # browser
        self.browser.get(self.url)
        while True:
            if self.browser.current_url=='http://issue.cpic.com.cn/ecar/view/portal/page/common/login.html':
                self.SendLogMess(self.browser)#登录
            else:
                break


        self.browser.find_element_by_id('loginBtn').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('bg-white').click()
        time.sleep(2)
        # getcookie
        cookie = [item["name"] + "=" + item["value"] for item in self.browser.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        return self.browser,cookiestr

    #登录信息
    def SendLogMess(self,browser):
        cookie = [item["name"] + "=" + item["value"] for item in self.browser.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        #code = input('please input verifycode:')
        code=ImageCode(cookiestr=cookiestr)
        username=browser.find_element_by_id('j_username')
        username.clear()
        username.send_keys('w_n008')
        passwd=browser.find_element_by_id('_password')
        passwd.clear()
        passwd.send_keys('Cpic123456')
        browser.find_element_by_id('verifyCode').send_keys(code)
        browser.find_element_by_id('j_login').click()
        time.sleep(2)

    def findcarinfoSH(self,browser,LicenseNo):
        #传车牌号
        while True:
            try:
                license=browser.find_element_by_id('plateNo')
                license.clear()
                license.send_keys(LicenseNo)
                break
            except:
                time.sleep(0.5)

        browser.find_element_by_id('motorcycleTypeSearch').click()
        #两步查询

        while True:
            try:
                divtab = browser.find_element_by_id('carTypeDialog')
                divtab.find_element_by_name('carInfomation').click()
                divtab.find_element_by_class_name('confirm').click()
                break
            except:
                time.sleep(0.5)

        dialog=browser.find_element_by_id('dialogTemplet')
        while True:
            try:
                dialog.find_element_by_name('riskInfomation').click()
                dialog.find_element_by_class_name('confirm').click()
                break
            except:
                time.sleep(0.5)

    def Baojia(self,browser,dic):
        dic1=copy.deepcopy(dic)
        dic2=copy.deepcopy(dic)#复制两份分别作为查询和获得表单用
        certype=Select(browser.find_element_by_id('certType'))#选择证件类型为身份证
        certype.select_by_value('1')
        #传身份证号
        browser.find_element_by_id('certNo').send_keys(self.cert)
        el = browser.find_element_by_xpath("//input[@insured-name='certificateCode']")
        el.clear()
        el.send_keys(self.cert)
        #取消交强险报价
        browser.find_element_by_id('compulsoryInput').send_keys(Keys.SPACE)
        ASK=Method_ASK_TB(browser=browser,dic=dic1)
        ASK.Askprice()
        browser.find_element_by_id('premiumTrial').click()#报价
        while True:
            try:
                warn = browser.find_element_by_class_name('float-content')
                warn.find_element_by_xpath("//a[text()='关闭']").click()#关闭警告
                break
            except:
                time.sleep(0.5)
        GET=Method_Get_TB(browser=browser,dic=dic2)
        detail=GET.GetPremium()
        info={
            'flag':200,
            'detaillist':detail
        }
        return info



#==========================测试代码========================================================
data={'ciInsurerCom':'YGBX','LicenseNo':'沪GC6653','detaillist':{'SJX':'30000','CSX':'1','DSFZRX':'200000','DSFZRX_BJMP':'1','SSX':'1','SSX_BJMP':'1','BLX':'1','CSX_BJMP':'1'}}
'''
RB=Robot()
br,cookies=RB.login()
time.sleep(2)
while True:
    br.refresh()
    time.sleep(30)

while True:
    flag=input('flag:')
    dic=data
    LicenseNo=dic['LicenseNo']
    info=RB.findcarinfoSH(browser=br,LicenseNo=LicenseNo)
    baojia=RB.Baojia(browser=br,dic=dic)
    print(baojia)'''



















