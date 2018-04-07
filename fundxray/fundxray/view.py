from django.shortcuts import *
from django.template import *
from fund.models import *
import datetime
import os
from dateutil.relativedelta import relativedelta


def get_last_date(day):
    if day == None:
        return datetime.date.today()
    return day - datetime.timedelta(days=1)

def list1(request):

    today = get_last_date(None)
    last_day = get_last_date(today)
    print(today)
    print(last_day)
    day = None
    while(True):
        day = get_last_date(day)
        #lst = FundValue.objects.order_by("-ljjz")[:10]
        lst = FundValue.objects.filter(date=day).order_by("-ljjz")[:10]
        if None == list or len(lst) == 0:
            print(day, 'no data')
            continue
        print(day, 'has data')
        break
    #lst = FundValue.objects.all()[:10]
    print("------------:", len(lst))

    last_month_year = datetime.date.today().year
    last_month = datetime.date.today().month
    if last_month == 1:
        last_month = 12
        last_month_year = last_month_year - 1
    else:
        last_month = last_month - 1

    firstday = datetime.date(year=last_month_year, month=last_month, day=1)
    print(firstday)
    lst2 = FundValueCalc.objects.filter(date=firstday, type=1).order_by("-increases")[:100]


    #if len(lst) > 10:
    #    lst = lst[0:10]
    #lst = ['aa', 'bb']
    data = {'tops':lst, "tops2":lst2}
    return render_to_response('list1.html', data)

def get_count_by_date(fund_data, date, count):
    for item in fund_data:
        if item.date == date:
            count = item.value + count
    return count

def get_cost_count_by_date(fund_data, date):
    for item in fund_data:
        if item.date == date:
            return item.value
    return 0

def show_detail(request, code, date_type):
    fund_name = FundInfo.get_name_by_code(code)

    now = datetime.date.today()
    type = ""

    date = None
    if date_type == "1":
        date = None  #历史以来
        type = "历史以来"
    elif date_type == "2":
        date = now - datetime.timedelta(days = 30)  #一个月以来
        type = "一个月以来"
    elif date_type == "3":
        date = now - datetime.timedelta(days = 90)  # 三个月以来
        type = "三个月以来"
    elif date_type == "4":
        date = now - datetime.timedelta(days = 180)  # 6个月以来
        type = "半年以来"
    elif date_type == "5":
        date = now - datetime.timedelta(days = 360)  # 12个月以来
        type = "一年以来"

    print(date)

    jjjg = FundValue.get_jg_list_from_date_by_code(code, date).order_by('date')

    ljjz = -1
    zddf = 0 #最大跌幅
    zdzf = 0 #最大涨幅
    doudong = 0 #抖动
    last_rate = 0
    for item in jjjg:
        if -1 == ljjz:
            ljjz = item.ljjz
        item.incr_rate = round((item.ljjz - ljjz) * 100 / item.jjjz, 3)
        rate = round(item.incr_rate - last_rate, 3)

        last_rate = item.incr_rate

        if rate > zdzf:
            zdzf = rate
        elif rate < zddf:
            zddf = rate

        abs_rate = abs(rate)
        if abs_rate > doudong:
            doudong = abs_rate

    data = {'code': code, 'name':fund_name, 'jjjg':jjjg, 'zdzf':zdzf, 'zddf':zddf, 'shouyilv':last_rate, 'type':type}

    context = RequestContext(request)
    return  render(request, 'show_detail.html',  data)

def show_income(request, code):
    fund_name = FundInfo.get_name_by_code(code)
    fund_data = FundDeal.get_lst_by_code(code)
    from_date = fund_data[0].date
    jjjg = FundValue.get_jg_list_from_date_by_code(code, from_date).order_by('date')

    count_totle = 0
    cost = 0
    ljjz = -1
    index = 0
    for item in jjjg:

        if item.jjjz == 0:
            continue

        cost_count = get_count_by_date(fund_data, item.date, 0)
        count_totle = count_totle + cost_count
        cost = cost_count * item.jjjz + cost
        item.count =  count_totle
        item.cost_count = cost_count
        item.cost = cost

        if -1 == ljjz:
            ljjz = item.ljjz

        item.value = item.jjjz * item.count
        item.income = item.value - item.cost
        item.income_rate = round(item.income * 100 / item.cost, 3)
        item.incr_rate = round((item.ljjz - ljjz) * 100 / item.jjjz, 3)
        item.index = index
        index = index + 1

    #print(STATIC_URL)

    data = {'code': code, 'name':fund_name, 'data':fund_data, 'jjjg':jjjg}
    context = RequestContext(request)
    return  render(request, 'show_income.html',  data)

    #return render(request, 'show_income.html', data)