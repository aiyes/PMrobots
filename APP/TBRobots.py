#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from APP.TBRobotBackControl import Method_ASK_TB,Method_Get_TB,ImageCode
from APP.TBRobotWarnDeal import WarnDeal
from APP.TBrobotSqlhelper import Car
import copy,requests,json
import datetime


url='http://issue.cpic.com.cn/ecar/view/portal/page/common/login.html'
testcert='530302199406170354'

class Robot(object):
    def __init__(self,url=url,cert=testcert):
        self.url=url
        self.cert=cert
        self.driverpath="C:/Python34/chromedriver.exe"
        self.browser = webdriver.Chrome(self.driverpath)

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
        code=input('please input code')
        #code=ImageCode(cookiestr=cookiestr)#第三方接口自动识别验证码
        username=browser.find_element_by_id('j_username')
        username.clear()
        username.send_keys('w_n008')
        passwd=browser.find_element_by_id('_password')
        passwd.clear()
        passwd.send_keys('Cpic123456')
        browser.find_element_by_id('verifyCode').send_keys(code)
        browser.find_element_by_id('j_login').click()
        time.sleep(2)

    #沪牌车信息传入
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

        warn=WarnDeal(browser)
        info=warn.CarIfWarn()
        print(info)
        return info

    #外地车信息传入
    def findcarinfoWD(self, browser, LicenseNo):
        SearchCar=Car(LicentseNo=LicenseNo)
        Carinfo=SearchCar.SearchInDatebase()
        print(Carinfo)
        #填写车辆信息
        ownername = browser.find_element_by_name('ownerName')
        ownername.send_keys(Carinfo['car_owner'])
        license = browser.find_element_by_id('plateNo')
        license.clear()
        license.send_keys(LicenseNo)
        carvin = browser.find_element_by_id('carVIN')
        carvin.clear()
        carvin.send_keys(Carinfo['frame_no'])
        engineNo = browser.find_element_by_id('engineNo')
        engineNo.send_keys(Carinfo['engine_no'])
        registerDate = browser.find_element_by_id('stRegisterDate')
        registerDate.send_keys(Carinfo['enroll_date'].strftime('%Y-%m-%d'))

        browser.find_element_by_id('VINSearch').click()
        warn=WarnDeal(browser)
        info=warn.CarIfWarn()
        print(info)
        return info

    #报价函数
    def Baojia(self,browser,dic):
        dic1=copy.deepcopy(dic)
        dic2=copy.deepcopy(dic)#复制两份分别作为查询和获得表单用
        certype=Select(browser.find_element_by_id('certType'))#选择证件类型为身份证
        certype.select_by_value('1')
        browser.find_element_by_id('certNo').send_keys(self.cert)#传身份证号
        el = browser.find_element_by_xpath("//input[@insured-name='certificateCode']")
        el.clear()
        el.send_keys(self.cert)
        browser.find_element_by_id('compulsoryInput').send_keys(Keys.SPACE)#取消交强险报价
        ASK=Method_ASK_TB(browser=browser,dic=dic1)
        ASK.Askprice()
        browser.find_element_by_id('premiumTrial').click()#报价
        while True:
            try:
                deal=WarnDeal(browser)
                deal.Baojiawarn()
                break
            except:
                time.sleep(0.5)
        GET=Method_Get_TB(browser=browser,dic=dic2)
        detail=GET.GetPremium()
        info={
            'isSuccess':200,
            'detaillist':detail
        }
        return info

    #上海车辆信息查询
    def CarinfoSH(self,cookies,LicenseNo):
        header = {
            'Host': 'issue.cpic.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://issue.cpic.com.cn/ecar/view/portal/page/quick_quotation/quick_quotation.html',
            'Content-Length': '107',
            'Cookie': cookies,
            'Connection': 'keep-alive',}
        url = 'http://issue.cpic.com.cn/ecar/quickoffer/queryPureriskAndVehicleInfoByMotorcycleTypeSearch'
        data = {"meta": {},
                "redata": {"plateNo": LicenseNo, "plateType": "02", "carVIN": "", "engineNo": "", "stRegisterDate": ""}}

        req=requests.post(url=url,data=json.dumps(data),headers=header)
        info=req.json()
        print(info)
        #数据接力
        data2 = {"meta": {}, "redata": {"searchFlag": "1", "carVIN": "", "moldCharacterCode": info['result']['moldCharacterCode']}}
        url2='http://issue.cpic.com.cn/ecar/quickoffer/queryVehicleInfoByVin'
        mo = requests.post(url=url2, data=json.dumps(data2), headers=header)

        return mo.json()






#==========================测试代码========================================================
'''
data={'carNo': '沪B9C858', 'details': {'DSFZRX': '500000', 'DSFZRX_BJMP': '500000', 'CSX_BJMP': 'true', 'JQX': 'true', 'CSX': 'true', 'CCS': 'true'}, 'ciInsurerCom': '太平洋保险'}

RB=Robot()
br,cookies=RB.login()
time.sleep(2)


while True:
    flag=input('flag:')
    dic=data
    LicenseNo=dic['carNo']
    info=RB.CarinfoSH(cookies=cookies,LicenseNo=LicenseNo)
    print(info)


    info=RB.findcarinfoSH(browser=br,LicenseNo=LicenseNo)
    baojia=RB.Baojia(browser=br,dic=dic)
    print(baojia)
'''


















