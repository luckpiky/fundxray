from fund.models import *
import datetime
import os

#获取指定时间段的收益率：这个时间段的累计净值差 * 100 / 起始基金净值
def fund_calc_income(fund_code, start_date, end_date):
    data = FundValue.objects.filter(code=fund_code, date__gte=start_date, date__lte=end_date)
    if len(data) == 0:
        return -9999,end_date
    data = data.order_by('date')
    last_index = len(data) - 1
    income = (data[last_index].ljjz - data[0].ljjz) * 100.00 / data[0].jjjz
    income = round(income , 3) #取小数点后三位
    return income,data[last_index].date

#获取最近1周的收益率
def fund_calc_income_week(fund_code):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    return fund_calc_income(fund_code, start_date, end_date)

#获取最近1个月的收益率
def fund_calc_income_month(fund_code):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)
    return fund_calc_income(fund_code, start_date, end_date)

#获取最近3个月的收益率
def fund_calc_income_3month(fund_code):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=90)
    return fund_calc_income(fund_code, start_date, end_date)

#获取最近6个月的收益率
def fund_calc_income_6month(fund_code):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=180)
    return fund_calc_income(fund_code, start_date, end_date)

#获取最近12个月的收益率
def fund_calc_income_year(fund_code):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)
    return fund_calc_income(fund_code, start_date, end_date)

def fund_calc_income_all(obj):
    obj.month_income, obj.update_time = fund_calc_income_month(obj.fund.code)
    obj.save()
    print('updated', obj.fund.name, obj.update_time, 'month_income:',obj.month_income)


def fund_update_income_all():
    #更新表中的收益情况
    data = FundValueDeal1.objects.all()
    for item in data:
        fund_calc_income_all(item)

    #查看那个基金没有记录在表中，没有的话记录一下
    funds = FundInfo.objects.all()
    for fund in funds:
        obj = FundValueDeal1.objects.filter(fund__id=fund.id)
        if None == obj or 0 == len(obj):
            obj = FundValueDeal1()
            obj.fund = fund
            fund_calc_income_all(obj)
            print('added', fund.name)





