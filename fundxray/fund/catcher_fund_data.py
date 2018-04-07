import urllib.request
import json

class CatchFundData():
    def __init__(self):
        self.code = ""
        self.org_url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=CODE&page=PAGE"
        self.url = ""
        self.page = 1
        return

    def set_fund_code(self, code):
        self.code = code
        self.url = self.org_url.replace("CODE", self.code)
        return

    def get_today_data(self):
        return

    def get_all_data():
        url = self.url.replace("PAGE", str(self.page))
        self.get_data(url)
        return

    def get_data_from_specify_date(self, date):
        return

    def get_next_page(self):
        self.page = self.page + 1
        url = self.url.replace("PAGE", str(self.page))
        self.get_data(url)
        return

    def get_datai(self, url):
        try:
            content = urllib.request.urlopen(self.url).read()
            j = json.loads(content)
            for t in j['data']:
                print(t)
        except:
            print("error")
        return
      



