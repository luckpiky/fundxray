#coding=utf-8

import urllib.request
import json
#import demjson
from fund.models import *

FundType = ['股票型', '混合型', '债券型', '指数型', 'ETF', 'QDII', 'LOF', '货币型']

class Catcher:
    def __init__(self):
        self.url = ''
        return

    def set_url(self, url):
        self.url = url
        return

class FundListCatcherEastmoney():
    def __init__(self):
        self.base_url = ''

    def set_baseurl(self, url):
        self.base_url = url

    def parse_fund_line(self, line):
        line = line.replace('[', '')
        line = line.replace('\"', '')

        t1 = line.split(',')

        #print t1

        return t1[0], t1[2], t1[3]

    def parse_fund_list(self, data):
        fund_list = []
        print("len:", len(data))
        t1 = data.find('[[')
        if -1 == t1:
            return []
        t1 = t1 + 1
        while True:
            if '[' != data[t1:t1+1]:
                break 

            t2 = data[t1:].find(']')
            if -1 == t2:
                break
            t2 = t2 + t1
            item = data[t1:t2+1]
            code, name, type1 = self.parse_fund_line(item)
            fund_list.append([code, name, type1])
            t1 = t2 + 2
        return fund_list


    def parse_fund_for_eastmoney2(self, line):
        line = line.replace('[', '')
        line = line.replace('\"', '')

        t1 = line.split(',')
        return t1[0], t1[1]



    def parse_fund_list2(self, data):
        fund_item_list = []
        t1_s = 'datas:['
        t1 = data.find(t1_s) + len(t1_s)
        if -1 == t1:
            return
        while True:
            if '[' != data[t1:t1+1]:
                break 

            t2 = data[t1:].find(']')
            if -1 == t2:
                break
            t2 = t2 + t1
            item = data[t1:t2+1]
            code, name = parse_fund_for_eastmoney(item)
            fund_item_list.append([code, name])
            t1 = t2 + 2

    def read_data(self): 
        #MyFundType = [['股票型', '2'], ['混合型', '3'], ['债券型', '13'], ['指数型', '5'], ['ETF', '11'], ['QDII', '6'], ['LOF', ''], ['货币型', '']]
        client = urllib.request.urlopen('http://fund.eastmoney.com/js/fundcode_search.js')
        content = client.read()
        #print("get data:",content)
        content = content.decode("utf-8")
        fundlist = self.parse_fund_list(content)
        return fundlist
	

def update_fund_from_eastmoney():
    fund_catcher = FundListCatcherEastmoney()
    fund_catcher.set_baseurl('http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&page=1,10000&lx=')
    #fund_list = fund_catcher.parse_fund_list(data)
    fundlist = fund_catcher.read_data()
    print("get data, len:",len(fundlist))

    for funditem in fundlist:
        print("find item:", funditem)
        t = FundInfo.objects.filter(code=funditem[0])
        if len(t) > 0:
            continue

        print(funditem[0],funditem[1])
        fund = FundInfo()
        fund.code = funditem[0]
        fund.name = funditem[1]
        fund.type1 = funditem[2]
        fund.company = ' '
        fund.save() 




#update_fund_from_eastmoney()


#catcher = FundListCatcherEastmoney()
#catcher.update


#url = 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&json=x&ps=10&p=1'
#$#url = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&page=1' 



#parse_fund_list_for_eastmoney(content)



