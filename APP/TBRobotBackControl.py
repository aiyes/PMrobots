#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium.webdriver.common.keys import Keys
import requests,datetime,base64
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from APP.TBRobotWarnDeal import WarnDeal
from selenium.webdriver.support import expected_conditions as EC

#----------------------------------------------------------------
#机器人后台功能
#----------------------------------------------------------------

#自动验证码识别接口
def ImageCode(cookiestr):
    header = {
        'Host': 'issue.cpic.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': cookiestr,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    url2 = 'http://issue.cpic.com.cn/ecar/auth/getCaptchaImage'
    capt = requests.get(url2, headers=header)
    # im = Image.open(io.BytesIO(capt.content))
    base64_data = base64.b64encode(capt.content)
    url2 = 'http://api.jisuapi.com/captcha/recognize'
    data2 = {'appkey': 'd5a9798f00f84bfc',
             'type': 'en4',
             'pic': base64_data}
    req2 = requests.post(url=url2, data=data2)
    info = req2.json()
    return str(info['result']['code'])

#根据排量选择车辆排量选择税务车辆类型
def TaxType(num):
    table=[1.0,1.6,2.0,2.5,3.0,4.0,100.0]
    tablevalue=['K01','K02','K03','K04', 'K05', 'K06','K07']
    for i in range(len(table)):
        if table[i]>=num:
            return tablevalue[i]


class Method_ASK_TB(object):
    def __init__(self,browser,dic):
        self.browser=browser
        self.detaillist=dic['details']

    def Askprice(self):
        #车损险必选
        self.CSX()
        for item in self.detaillist:
            try:
                eval('self.{}'.format(item))()
            except:
                continue
    #交强险
    def JQX(self):
        self.browser.find_element_by_id('compulsoryInput').send_keys(Keys.SPACE)
        capacity = float(self.browser.find_element_by_id('engineCapacity').get_attribute('value'))
        TVType = Select(self.browser.find_element_by_name('taxVehicleType'))
        TVType.select_by_value(TaxType(capacity))
    #车船税
    def CCS(self):pass
    #车损险
    def CSX(self):
        if 'CSX_BJMP' in self.detaillist:
            self.browser.find_element_by_id('checkbox3').send_keys(Keys.SPACE)
            self.detaillist.pop('CSX_BJMP')
        else:
            self.browser.find_element_by_id('checkbox3').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox4').send_keys(Keys.SPACE)
        self.detaillist.pop('CSX')
    def CSX_BJMP(self):pass
    #第三方责任险
    def DSFZRX(self):
        if 'DSFZRX_BJMP'in self.detaillist:self.browser.find_element_by_id('checkbox5').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox5').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox6').send_keys(Keys.SPACE)
        ThirdInAmount = Select(self.browser.find_element_by_id('thirdInsuranceAmount'))
        ThirdInAmount.select_by_value(self.detaillist['DSFZRX'])
    def DSFZRX_BJMP(self):pass
    #司机险
    def SJX(self):
        SJAmount = self.browser.find_element_by_id('pLI')
        SJAmount.clear()
        SJAmount.send_keys(self.detaillist['SJX'])
        if 'SJX_BJMP' in self.detaillist:
            self.browser.find_element_by_id('checkbox7').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox7').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox77').send_keys(Keys.SPACE)
    def SJX_BJMP(self):pass
    #乘客险
    def CKX(self):
        self.browser.find_element_by_id('seatPrice').send_keys(self.detaillist['CKX'])
        if 'CKX_BJMP' in self.detaillist:
            self.browser.find_element_by_id('checkbox8').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox8').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox88').send_keys(Keys.SPACE)
    def CKX_BJMP(self):pass
    #盗抢险
    def DQX(self):
        if 'DQX_BJMP' in self.detaillist:
            self.browser.find_element_by_id('checkbox10').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox10').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox11').send_keys(Keys.SPACE)
    def DQX_BJMP(self):pass
    #玻璃险
    def BLX(self):
        self.browser.find_element_by_id('checkbox12').send_keys(Keys.SPACE)
        locality = Select(self.browser.find_element_by_id('locality'))
        locality.select_by_value(self.detaillist['BLX'])  # 0国产，1进口
    #自燃险
    def ZRX(self):
        if 'ZRX_BJMP' in self.detaillist:
            self.browser.find_element_by_id('checkbox14').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox14').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox15').send_keys(Keys.SPACE)
    def ZRX_BJMP(self):pass
    #刮痕险
    def GHX(self):
        if 'GHX_BJMP'in self.detaillist:
            self.browser.find_element_by_id('checkbox16').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox16').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox17').send_keys(Keys.SPACE)
        HHAmount = Select(self.browser.find_element_by_name('birthday'))
        HHAmount.select_by_value(self.detaillist['GHX'])
    def GHX_BJMP(self):pass
    #涉水险
    def SSX(self):
        if 'SSX_BJMP' in self.detaillist:
            self.browser.find_element_by_id('checkbox18').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox18').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox19').send_keys(Keys.SPACE)
    def SSX_BJMP(self):pass
    #精神损害保险
    def JSSHZRX(self):
        if 'JSSHZRX_BJMP' in self.detaillist:
            self.browser.find_element_by_id('checkbox24').send_keys(Keys.SPACE)
        else:
            self.browser.find_element_by_id('checkbox24').send_keys(Keys.SPACE)
            self.browser.find_element_by_id('checkbox25').send_keys(Keys.SPACE)
        JSAmount = Select(self.browser.find_element_by_xpath("//table[@id='quoteInsuranceTable']/tbody/tr[13]/td[3]/select"))
        JSAmount.select_by_value(self.detaillist['JSSHZRX'])  # 10000,20000,30000,40000,50000
    #指定修理厂险
    def ZDXLCX(self):
        self.browser.find_element_by_id('checkbox28').send_keys(Keys.SPACE)
        self.browser.find_element_by_id('rate').send_keys(self.detaillist['ZDXLCX'])  # 0.1-0.3

class Method_Get_TB(object):
    def __init__(self,browser,dic):
        self.browser=browser
        self.quotetable = browser.find_element_by_id('quoteInsuranceTable')
        self.detaillist=dic['details']

    def GetPremium(self):
        info=[]
        for item in self.detaillist:
            try:
                eval('self.{}'.format(item))(info)
            except:
                continue
        return info

    def infodic(self,name,amount,value):
        dic={
            'prmCode':name,
            'premiumType':amount,
            'prmValue':value,
        }
        return dic
    #交强险
    def JQX(self,info):
        value=self.browser.find_element_by_id('cipremium').text
        info.append(self.infodic('JQX', self.detaillist['JQX'], value))
        return info
    #车船税
    def CCS(self,info):
        value=self.browser.find_element_by_id('taxAmount').text
        info.append(self.infodic('CCS', self.detaillist['CCS'], value))
        return info
    #车损险
    def CSX(self,info):
        value=self.quotetable.find_element_by_xpath("./tbody/tr[1]/td[5]").text
        info.append(self.infodic('CSX',self.detaillist['CSX'],value))
        return info
    #车损险不计免赔
    def CSX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[1]/td[6]").text
        info.append(self.infodic('CSX_BJMP', self.detaillist['CSX_BJMP'], value))
        return info
    #第三方责任险
    def DSFZRX(self,info):
        value=self.quotetable.find_element_by_xpath("./tbody/tr[2]/td[5]").text
        info.append(self.infodic('DSFZRX', self.detaillist['DSFZRX'], value))
        return info
    #第三方责任险不计免赔
    def DSFZRX_BJMP(self,info):
        value=self.quotetable.find_element_by_xpath("./tbody/tr[2]/td[6]").text
        info.append(self.infodic('DSFZRX_BJMP', self.detaillist['DSFZRX_BJMP'], value))
        return info
    #司机险
    def SJX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[3]/td[5]").text
        info.append(self.infodic('SJX', self.detaillist['SJX'], value))
        return info
    #司机险不计免赔
    def SJX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[3]/td[6]").text
        info.append(self.infodic('SJX_BJMP', self.detaillist['SJX_BJMP'], value))
        return info
    #乘客险
    def CKX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[4]/td[5]").text
        info.append(self.infodic('CKX', self.detaillist['CKX'], value))
        return info
    #乘客险不计免赔
    def CKX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[4]/td[6]").text
        info.append(self.infodic('CKX_BJMP', self.detaillist['CKX_BJMP'], value))
        return info
    #盗抢险
    def DQX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[5]/td[5]").text
        info.append(self.infodic('DQX', self.detaillist['DQX'], value))
        return info
    #盗抢险不计免赔
    def DQX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[5]/td[6]").text
        info.append(self.infodic('DQX_BJMP', self.detaillist['DQX_BJMP'], value))
        return info
    #玻璃险
    def BLX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[7]/td[5]").text
        info.append(self.infodic('BLX', self.detaillist['BLX'], value))
        return info
    #自燃险
    def ZRX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[8]/td[5]").text
        info.append(self.infodic('ZRX', self.detaillist['ZRX'], value))
        return info
    #自燃险不计免赔
    def ZRX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[8]/td[6]").text
        info.append(self.infodic('ZRX_BJMP', self.detaillist['ZRX_BJMP'], value))
        return info
    #刮痕险
    def GHX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[9]/td[5]").text
        info.append(self.infodic('GHX', self.detaillist['GHX'], value))
        return info
    #刮痕险不计免赔
    def GHX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[9]/td[6]").text
        info.append(self.infodic('GHX_BJMP', self.detaillist['GHX_BJMP'], value))
        return info

    def SSX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[10]/td[5]").text
        info.append(self.infodic('SSX', self.detaillist['SSX'], value))
        return info

    def SSX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[10]/td[6]").text
        info.append(self.infodic('SSX_BJMP', self.detaillist['SSX_BJMP'], value))
        return info

    def JSSHZRX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[13]/td[5]").text
        info.append(self.infodic('JSSHZRX', self.detaillist['JSSHZRX'], value))
        return info

    def ZDXLCX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[15]/td[5]").text
        info.append(self.infodic('ZDXLCX', self.detaillist['ZDXLCX'], value))
        return info

def CommecialDateAlter(browser):
    now = datetime.datetime.now()
    date = now + datetime.timedelta(days=30)
    dstr = date.strftime('%Y-%m-%d 00:00')
    startdate = browser.find_element_by_id('commercialStartDate')
    startdate.send_keys(Keys.SPACE)
    startdate.clear()
    startdate.send_keys(dstr)
    result = EC.alert_is_present()(browser)
    if result:
        deal = WarnDeal(browser)
        deal.TimeAlter(result, dstr)





