import urllib.request
import json
from fund.models import *
import traceback
import datetime
import time

class CatchFundData():
    def __init__(self):
        self.code = ""
        self.org_url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=CODE&page=PAGE"
        #self.org_url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=CODE&datefrom=2017-09-20&dateto=2017-09-30&page=PAGE"
        self.url = ""
        self.page = 1
        self.sleep_time = 0
        self.update = False
        return

    def set_sleep_time(self, time):
        self.sleep_time = time
        return

    def set_update(self, update):
        self.update = update
        return

    def save_data(self, data):
        jjjz = float(data['jjjz'])
        ljjz = float(data['ljjz'])
        #print(data['fbrq'], jjjz)


        date = datetime.datetime.strptime(data['fbrq'], "%Y-%m-%d %H:%M:%S")
        objs = FundValue.objects.filter(date=date, code=self.code)
        if None != objs and len(objs) > 0:
            #print('find,', objs[0].date, objs[0].code)
            if True == self.update and (objs[0].jjjz != jjjz or objs[0].ljjz != ljjz):
                print("update:", self.code, date, "old:", objs[0].jjjz, objs[0].ljjz, "new:", jjjz, ljjz)
                objs[0].jjjz = jjjz
                objs[0].ljjz = ljjz
                objs[0].save()
            return

        value = FundValue()
        value.code = self.code
        value.date = datetime.datetime.strptime(data['fbrq'], "%Y-%m-%d %H:%M:%S")
        #print(value.date)

        value.jjjz = float(data['jjjz'])
        value.ljjz = float(data['ljjz'])
        value.save()
        print('save---', value.code, value.date, value.jjjz, value.ljjz)
        #FundValue.objects.get(code=self.code, )

    def set_fund_code(self, code):
        self.code = code
        self.url = self.org_url.replace("CODE", self.code)
        return

    def get_today_data(self):
        return

    def get_all_data(self):
        url = self.url.replace("PAGE", str(self.page))
        cnt = self.get_data(url)
        return cnt

    def get_data_from_specify_date(self, date):
        return

    def get_next_page(self):
        self.page = self.page + 1
        url = self.url.replace("PAGE", str(self.page))
        print(url)
        cnt = self.get_data(url)
        return cnt 

    def get_data(self, url):
        cnt = 0
        try:
            content = urllib.request.urlopen(url).read()
            #print("get content, len:", len(content))
            j = json.loads(content)
            print("parse json", j['result']['data'])
            for t in j['result']['data']['data']:
                #print(t)
                self.save_data(t)
                cnt = cnt + 1
                if self.sleep_time > 0:
                    time.sleep(self.sleep_time)
        except Exception as e:
            print("error:", traceback.print_exc())
            print(url)
        return cnt
      

def catch_fund_data(code, next, update):
    catcher = CatchFundData()
    catcher.set_fund_code(code)
    #catcher.set_sleep_time(1)
    if True == update:
        catcher.set_update(True)
    cnt = catcher.get_all_data()    
    while(cnt > 0 and next):
        cnt = catcher.get_next_page()


def catch_all_fund_data(update):
    #catch_fund_data('000001')
    #return

    funds = FundInfo.objects.all()
    for fund in funds:
        print("read fund:", fund.code)
        catch_fund_data(fund.code, True, update)
        time.sleep(15)

def catch_all_fund_data_daily(update):
    cnt = 0
    funds = FundInfo.objects.all().order_by("-code")
    while(True):
        for fund in funds:
            print("read fund:", fund.code, fund.name)
            catch_fund_data(fund.code, False, update)
            #catch_fund_data("710002", False, update)
            if cnt % 10 == 0:
                time.sleep(10)
            cnt = cnt + 1
        time.sleep(1000)
