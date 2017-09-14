#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium.webdriver.common.keys import Keys
import requests,datetime,base64,time,threading,re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from APP.TBRobotWarnDeal import WarnDeal
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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

#去除千分位
def DropDot(string):
    stringlist=string.split(',')
    newstring=''
    for i in stringlist:
        newstring+=''.join(i)
    return newstring

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
        CompulDateAlter(self.browser)
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
        dic={
            '国产':'0',
            '进口':'1',
        }
        self.browser.find_element_by_id('checkbox12').send_keys(Keys.SPACE)
        locality = Select(self.browser.find_element_by_id('locality'))
        locality.select_by_value(dic[self.detaillist['BLX']])  # 0国产，1进口
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

#获取报价信息
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

    def infodic(self,code,amount,value,name):
        dic={
            'prmName':name,
            'prmCode':code,
            'premiumType':amount,
            'prmValue':value.strip(),
        }
        return dic
    #交强险
    def JQX(self,info):
        value=self.browser.find_element_by_id('cipremium').text
        info.append(self.infodic('JQX', self.detaillist['JQX'], value,'交强险'))
        return info
    #车船税
    def CCS(self,info):
        value=self.browser.find_element_by_id('taxAmount').text
        info.append(self.infodic('CCS', self.detaillist['CCS'], DropDot(value),'车船税'))
        return info
    #车损险
    def CSX(self,info):
        value=self.quotetable.find_element_by_xpath("./tbody/tr[1]/td[5]").text
        info.append(self.infodic('CSX',self.detaillist['CSX'],value,'车损险'))
        return info
    #车损险不计免赔
    def CSX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[1]/td[6]").text
        info.append(self.infodic('CSX_BJMP', self.detaillist['CSX_BJMP'], value,'车损险不计免赔'))
        return info
    #第三方责任险
    def DSFZRX(self,info):
        value=self.quotetable.find_element_by_xpath("./tbody/tr[2]/td[5]").text
        info.append(self.infodic('DSFZRX', self.detaillist['DSFZRX'], value,'第三方责任险'))
        return info
    #第三方责任险不计免赔
    def DSFZRX_BJMP(self,info):
        value=self.quotetable.find_element_by_xpath("./tbody/tr[2]/td[6]").text
        info.append(self.infodic('DSFZRX_BJMP', self.detaillist['DSFZRX_BJMP'], value,'第三方责任险不计免赔'))
        return info
    #司机险
    def SJX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[3]/td[5]").text
        info.append(self.infodic('SJX', self.detaillist['SJX'], value,'司机险'))
        return info
    #司机险不计免赔
    def SJX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[3]/td[6]").text
        info.append(self.infodic('SJX_BJMP', self.detaillist['SJX_BJMP'], value,'司机险不计免赔'))
        return info
    #乘客险
    def CKX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[4]/td[5]").text
        info.append(self.infodic('CKX', self.detaillist['CKX'], value,'乘客险'))
        return info
    #乘客险不计免赔
    def CKX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[4]/td[6]").text
        info.append(self.infodic('CKX_BJMP', self.detaillist['CKX_BJMP'], value,'乘客险不计免赔'))
        return info
    #盗抢险
    def DQX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[5]/td[5]").text
        info.append(self.infodic('DQX', self.detaillist['DQX'], value,'盗抢险'))
        return info
    #盗抢险不计免赔
    def DQX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[5]/td[6]").text
        info.append(self.infodic('DQX_BJMP', self.detaillist['DQX_BJMP'], value,'盗抢险不计免赔'))
        return info
    #玻璃险
    def BLX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[7]/td[5]").text
        info.append(self.infodic('BLX', self.detaillist['BLX'], value,'玻璃险'))
        return info
    #自燃险
    def ZRX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[8]/td[5]").text
        info.append(self.infodic('ZRX', self.detaillist['ZRX'], value,'玻璃险不计免赔'))
        return info
    #自燃险不计免赔
    def ZRX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[8]/td[6]").text
        info.append(self.infodic('ZRX_BJMP', self.detaillist['ZRX_BJMP'], value,'自燃险不计免赔'))
        return info
    #刮痕险
    def GHX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[9]/td[5]").text
        info.append(self.infodic('GHX', self.detaillist['GHX'], value,'刮痕险'))
        return info
    #刮痕险不计免赔
    def GHX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[9]/td[6]").text
        info.append(self.infodic('GHX_BJMP', self.detaillist['GHX_BJMP'], value,'刮痕险不计免赔'))
        return info

    def SSX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[10]/td[5]").text
        info.append(self.infodic('SSX', self.detaillist['SSX'], value,'涉水险'))
        return info

    def SSX_BJMP(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[10]/td[6]").text
        info.append(self.infodic('SSX_BJMP', self.detaillist['SSX_BJMP'], value,'涉水险不计免赔'))
        return info
    #精神损害责任险
    def JSSHZRX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[13]/td[5]").text
        info.append(self.infodic('JSSHZRX', self.detaillist['JSSHZRX'], value,'精神损害责任险'))
        return info

    def ZDXLCX(self,info):
        value = self.quotetable.find_element_by_xpath("./tbody/tr[15]/td[5]").text
        info.append(self.infodic('ZDXLCX', self.detaillist['ZDXLCX'], value,'指定修理厂险'))
        return info

def TimeInfoDic():
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    nextday = now + datetime.timedelta(days=2)
    TimeInfo = {'now':now,
        'stBackEndDate': '%s-12-31' % (now.year - 1),
        'stBackStartDate': '%s-12-31' % (now.year - 1),
        'stLateFeeEndDate': tomorrow.strftime('%Y-%m-%d'),
        'stLateFeeStartDate': tomorrow.strftime('%Y-%m-%d'),
        'stStartDate': nextday.strftime('%Y-%m-%d 00:00'),
        'stEndDate': (nextday + datetime.timedelta(days=365)).strftime('%Y-%m-%d 00:00'),
        'stTaxStartDate': '%s-01-01' % now.year,
        'stTaxEndDate': '%s-12-31' % now.year, }
    return TimeInfo

#统一修改商业险时间为30天后
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
        deal.CommecialTimeAlter(result, dstr)

#修改交强险时间为30天后
def CompulDateAlter(browser):
    now = datetime.datetime.now()
    date = now + datetime.timedelta(days=30)
    dstr = date.strftime('%Y-%m-%d 00:00')
    startdate = browser.find_element_by_id('compulsoryStartDate')
    startdate.send_keys(Keys.SPACE)
    startdate.clear()
    startdate.send_keys(dstr)
    result = EC.alert_is_present()(browser)
    if result:
        deal = WarnDeal(browser)
        deal.CompusoryTimeAlter(result, dstr)

#根据座位数量改变车辆性质
def VehicleTypeSelect(browser):
    SeatCountNode = browser.find_element_by_name('seatCount')
    SeatCount = int(SeatCountNode.get_attribute('value'))
    vehicleTypeNode = Select(browser.find_element_by_id('vehicleType'))
    if SeatCount >= 6:
        count = [10, 20, 36, 1000]
        value = ['02', '03', '04', '05']
        for i in range(4):
            if SeatCount < count[i]:
                vehicleTypeNode.select_by_value(value[i])
                break

#根据车主姓名改变车辆用途
def Useage(browser):
    owner = browser.find_element_by_name('ownerName')
    ownername = owner.get_attribute('value')
    if len(ownername) > 5:
        useage = Select(browser.find_element_by_id('usage'))
        useage.select_by_value('301')  # 企业非营运车辆
        WebDriverWait(browser, 4, 0.5).until(lambda browser: browser.find_element_by_id('usageSubdivs'))
        useageSub = Select(browser.find_element_by_id('usageSubdivs'))
        useageSub.select_by_value('23')  # 企业客车，其他

#预核保流程
def YuHeBao(browser):
    def WindowClose(browser):
        browser.close()
    close=threading.Thread(target=WindowClose,args=(browser,))
    try:
        browser.find_element_by_id("linkInsure").click()
        time.sleep(2)
        WebDriverWait(browser, 4, 0.5).until(lambda browser: browser.find_element_by_id('next'))
        browser.find_element_by_id("next").click()
        time.sleep(2)
        WebDriverWait(browser, 4, 0.5).until(lambda browser: browser.find_element_by_id('next'))
        browser.find_element_by_id("next").click()
        time.sleep(2)
        WebDriverWait(browser, 4, 0.5).until(lambda browser: browser.find_element_by_id('insuranceInfoMobilePhone'))
        mobile=browser.find_element_by_id('insuranceInfoMobilePhone')
        mobile.clear()
        mobile.send_keys('13608815861')
        address=browser.find_element_by_name('address')
        address.clear()
        address.send_keys('中国上海')
        browser.find_element_by_id('yhb').click()
        while True:
            dialog = browser.find_element_by_id('questionDialog')
            warntext = dialog.find_element_by_xpath("./div[@class='float-content']/div[@id='questionTxt']").text
            if warntext:
                close.start()
                return warntext
            else:
                time.sleep(0.5)
    except:
        close.start()
        return '未获取到核保信息'



#交强险报价信息生成函数
def BJinformTax(info,ModelData,DetailData,taxtype):
    Timeinfo=TimeInfoDic()
    FinaInfo={'meta': {},'redata':{
        'commercial':False,
        'compulsory' : True,
        'compulsoryInsuransVo':{
            'aidingFund': '',
            'aidingFundProportion': '',
            'backAmount': '',
            'cipremium': None,
            'ecompensationRate': '',
            'exceedDaysCount': '',
            'insuranceQueryCode': '',
            'lateFee': '',
            'payableAmount': '',
            'reductionAmount': '',
            'stBackEndDate': Timeinfo['stBackEndDate'],  # 补缴止期
            'stBackStartDate': Timeinfo['stBackStartDate'],  # 补缴起期
            'stEndDate':Timeinfo['stEndDate'] ,  # 保险止期
            'stLateFeeEndDate': Timeinfo['stLateFeeEndDate'],  # 滞纳金止期
            'stLateFeeStartDate' :Timeinfo['stLateFeeStartDate'],#滞纳金起期
            'stStartDate':Timeinfo['stStartDate'],#保险起期
            'stTaxEndDate':Timeinfo['stTaxEndDate'],#车船税止期
            'stTaxStartDate':Timeinfo['stTaxStartDate'],#车船税起期
            'taxAmount':None,
            'taxBureauName':'',
            'taxPaidNo':'',
            'taxpayerName':info['result']['ownerName'],
            'taxpayerNo':'123321',
            'taxpayerSubstRecno':'',
            'taxpayerType':'2',#纳税人类型
            'taxType':taxtype,#纳税类型
            'taxVehicleType':TaxType(float(ModelData['result']['models'][0]['displacement'])),
            'totalWeight':'',
            'vehicleClaimType':''},
        'ecarvo':{
            'actualValue':int(ModelData['result']['models'][0]['purchaseValue'])*0.8,
            'address':'',
            'carModelRiskLevel':'',
            'carVIN':info['result']['carVIN'],
            'certNo':'123321',
            'certType':'2',
            'emptyWeight':ModelData['result']['models'][0]['fullWeight']+'.00',
            'engineCapacity':float(ModelData['result']['models'][0]['displacement']),
            'engineNo':info['result']['engineNo'],
            'factoryType':ModelData['result']['models'][0]['name'],
            'holderTelphone':'',
            'inType':'',
            'jqVehicleClaimType':'',
            'jyFuelType':ModelData['result']['models'][0]['jyFuelType'],
            'lastyearModelcode':'',
            'lastyearModeltype':'',
            'lastyearPurchaseprice':'',
            'loan':'0',
            'modelType':DetailData['result']['models'][0]['modelType'],
            'moldCharacterCode':DetailData['result']['models'][0]['moldCharacterCode'],
            'negotiatedValue':int(ModelData['result']['models'][0]['purchaseValue'])*0.8,
            'oriEngineCapacity':DetailData['result']['models'][0]['displacement'],
            'ownerName':info['result']['ownerName'],
            'ownerProp':'1',
            'plateColor':'1',
            'plateless':False,
            'plateNo':info['result']['plateNo'],
            'plateType':'02',
            'power':ModelData['result']['models'][0]['power'],
            'producingArea':DetailData['result']['models'][0]['producingArea'],
            'purchasePrice':DetailData['result']['models'][0]['purchaseValue'],
            'reductionType':'0',
            'seatCount':ModelData['result']['models'][0]['seatCount'],
            'shortcutCode':DetailData['result']['models'][0]['shortcutCode'],
            'specialVehicleIden':'',
            'stCertificationDate':'',
            'stChangeRegisterDate':'',
            'stInvoiceDate':'',
            'stRegisterDate':info['result']['stRegisterDate'],
            'syVehicleClaimType':'',
            'taxCustomerType':'1',
            'tonnage':'',
            'tpyRiskflagCode':ModelData['result']['models'][0]['tpyRiskflagCode'],
            'tpyRiskflagName':ModelData['result']['models'][0]['tpyRiskflagName'],
            'transferCompanyName':'',
            'usage':'101',
            'vehiclePowerJY':ModelData['result']['models'][0]['vehiclepowerjy'],
            'vehiclePurpose':ModelData['result']['models'][0]['kind'],
            'vehicleType':ModelData['result']['models'][0]['kind']},
        'insuredVo':{
            'certificateCode':'123321',
            'certificateType':'2',
            'name':info['result']['ownerName'],
            'relationship':'1'},
        'inType':None,
        'platformVo':{
            'benchmarkRiskPremium':DetailData['result']['models'][0]['pureRiskPremium'],
            'brand':DetailData['result']['models'][0]['modelType'],
            'brandCode':DetailData['result']['models'][0]['brandCode'],
            'carName':DetailData['result']['models'][0]['carName'],
            'configType':DetailData['result']['models'][0]['configType'],
            'modelCode':DetailData['result']['models'][0]['hyVehicleCode'],
            'noticeType':'',
            'pureRiskPremium':DetailData['result']['models'][0]['pureRiskPremium'],
            'pureRiskPremiumFlag':DetailData['result']['models'][0]['pureRiskPremiumFlag'],
            'series':DetailData['result']['models'][0]['series'],
            'seriesCode':''},
        'quotationNo':''}}
    return FinaInfo


#在交强险警告中寻找信息
def FindIfInCiWarn(Warn):
    message = Warn['message']['message']
    try:
        com = re.findall('该车已在(.+)存在有效保单记录', message)  # 有投保记录
        notax = re.findall('不能以纳税投保', message)#无纳税记录
        if notax:
            flag=False
            info = {'prm_end_time': '', 'insurer_com': '', }
            return info,flag
        elif com:
            flag=True
            dateput = re.findall('－(\d+)年(\d+)月(\d+)日', message)
            date = datetime.datetime(int(dateput[0][0]), int(dateput[0][1]), int(dateput[0][2]))
            info={'prm_end_time':date,'insurer_com':com,}
            return info,flag
    except:
        flag=True
        info={'prm_end_time':'','insurer_com':'',}
        return info,flag

#根据查询到的信息组建车辆信息查询返回json串
def CarinfoSHDic(car_data_database):
    return_message = {
            'status': 200,
            "brandNameBC": car_data_database['brand_name'],
            "carOwnerBC": car_data_database['car_owner'],
            "completeKerbMassNewBC": car_data_database['complete_kerb_mass'],
            "engineNoBC": car_data_database['engine_no'],
            "enrollDateBC": car_data_database['enroll_date'],
            "exhaustScaleBC": car_data_database['exhaust_scale'],
            "frameNoBC": car_data_database['frame_no'],
            "id": car_data_database['id'],
            "insurerCom": car_data_database['insurer_com'],
            "licenseNoBC": car_data_database['license_no'],
            "modelCodeBC": car_data_database['model_code'],
            "prmEndTime": car_data_database['prm_end_time'],
            "purchasePriceBC": car_data_database['purchase_price'],
            "purchasePriceLBBC": car_data_database['purchase_price_lb'],
            "searchSequenceNoBI": car_data_database['search_sequence_no'],
            "seatCountBC": car_data_database['seat_count'],
            }
    return return_message
