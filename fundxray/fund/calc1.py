from fund.models import *
import datetime
import calendar

def get_start_end_day_of_month(year, month):
    firstday = datetime.date(year=year, month=month, day=1)
    monthdays = calendar.monthrange(year,month)[1]
    lastday = datetime.date(year=year, month=month, day=monthdays)
    return firstday,lastday


def calc_incr_jitter_in_range_days(firstday, lastday, code):
    lst = FundValue.objects.filter(date__gte=firstday, date__lte=lastday, code__exact=code).order_by("date")
    if None == lst or len(lst) == 0:
        return None, None

    first_value = lst[0]
    last_value = lst[len(lst)-1]
    incr = (last_value.ljjz - first_value.ljjz) * 100 / first_value.jjjz
    jitter = 0.0
    value = 0.0
    value2 = 0.0

    for t in lst:
        if value == 0:
            value = t.ljjz
            value2 = t.jjjz
        if t.ljjz > value:
            incr_percent = (t.ljjz - value) * 100 / value2
        else: 
            incr_percent = (value - t.ljjz) * 100 / value2
        if incr_percent > jitter:
            jitter = incr_percent
        value = t.ljjz
        value2 = t.jjjz
        #print(t.date, t.ljjz)

    return incr, jitter

def save_calc_result(code, type, firstday, incr, jitter):
    t = FundValueCalc()
    t.code = code
    t.type = type
    t.date = firstday
    t.increases = incr
    t.jitter = jitter
    t.save()
    return

def calc_all_incr_jitter_of_month(year, month):
    lst = FundInfo.objects.all()
    if None == lst:
        return

    firstday, lastday = get_start_end_day_of_month(year, month)
    #incr, jitter = calc_incr_jitter_in_range_days(firstday, lastday, '150234')
    #print(firstday, incr, jitter)

    for item in lst:
        lst2 = FundValueCalc.objects.filter(code=item.code, type=1, date=firstday).all()
        if None == lst2:
            continue
        incr, jitter = calc_incr_jitter_in_range_days(firstday, lastday, item.code)
        print(item.name, item.code, firstday, incr, jitter)

        if None == incr or None == jitter:
            continue
 
        save_calc_result(item.code, 1, firstday, incr, jitter)
    return



