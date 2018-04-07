from django.db import models

# Create your models here.
class FundInfo(models.Model):
    name = models.CharField(max_length = 64)
    code = models.CharField(max_length = 32)
    company = models.CharField(max_length = 64)
    type1 = models.CharField(max_length = 64)

    def __str__(self):
        return self.name

    def get_name_by_code(code):
        fund_name = ''
        try:
            objs = FundInfo.objects.filter(code=code)
            fund_name = objs[0].name
        except:
            pass

        return fund_name

class FundValue(models.Model):
    code = models.CharField(max_length = 32)
    jjjz = models.FloatField()
    ljjz = models.FloatField()
    date = models.DateField()
    
    def __str__(self):
        #return self.code
        return str(self.code) + str(self.date)

    def get_jg_list_from_date_by_code(code, date):
        if None == date:
            objs = FundValue.objects.filter(code=code)
        else:
            objs = FundValue.objects.filter(code=code, date__gte=date)
        return objs

class FundValueCalc(models.Model):
    code = models.CharField(max_length = 32)
    date = models.DateField()
    increases = models.FloatField()
    jitter = models.FloatField()
    type = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.code) + str(self.date)


class FundDeal(models.Model):
    code = models.CharField(max_length = 32)
    date = models.DateField()
    value = models.FloatField()

    def get_lst_by_code(code):
        objs = FundDeal.objects.filter(code=code).order_by('date')
        return objs

    def __unicode__(self):
        return str(self.code) + str(self.date) + str(self.value)

class FundManager(models.Model):
    name = models.CharField(max_length = 32)
    link = models.CharField(max_length = 512)
    desc = models.TextField()

    def __str__(self):
        return self.name

class FundToManager(models.Model):
    code = models.CharField(max_length = 32)
    manager = models.ForeignKey(FundManager)
    start_date = models.DateField()
    end_date = models.DateField()
    desc = models.CharField(max_length = 512)

    def __str__(self):
        return str(self.code)+self.name


#计算基金的重要参数
class FundValueDeal1(models.Model):
    fund = models.ForeignKey(FundInfo)
    update_time = models.DateField()
    month_income = models.FloatField()  #最近一个月的收益率


class DevInfo(models.Model):
    title = models.CharField(max_length = 64)
    record_time = models.DateField()
    content = models.TextField()

    def __str__(self):
        return self.title
