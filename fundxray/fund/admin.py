from django.contrib import admin
from fund.fund_fun import *
import datetime

# Register your models here.

from fund.models import *
from django.utils.html import *

class FundInfoAdmin(admin.ModelAdmin):
    def link1(self):
        return format_html('<a href="/show_detail/{}/1" target="_blank">历史数据</a>', self.code)

    def link2(self):
        return format_html('<a href="/show_detail/{}/2" target="_blank">一个月以来</a>', self.code)

    def link3(self):
        return format_html('<a href="/show_detail/{}/3" target="_blank">三个月以来</a>', self.code)

    def link4(self):
        return format_html('<a href="/show_detail/{}/4" target="_blank">半年以来</a>', self.code)

    def link5(self):
        return format_html('<a href="/show_detail/{}/5" target="_blank">一年以来</a>', self.code)

    list_display = ('name', 'code', 'company', 'type1', link1, link2, link3, link4, link5)
    search_fields = ('name', 'code', 'company')  # 搜索字段

class FundDealAdmin(admin.ModelAdmin):
    def name(self):
        return FundInfo.get_name_by_code(self.code)

    def link(self):
        return format_html('<a href="/show_income/{}" target="_blank">查看</a>', self.code)

    #get_code.admin_order_field = '-id'

    list_display = (name, 'code', 'date', 'value', link)

class FundManageAdmin(admin.ModelAdmin):
    def link_str(self):
        return format_html('<a href="{}" target="_blank">查看</a>', self.link)

    list_display = ('name', link_str, 'desc')

#class FundToManageAdmin(admin.ModelAdmin):
#    def fund_name(self):
#        return FundInfo.get_name_by_code(self.code)
#
#    list_display = (fund_name, 'manager', 'start_date', 'end_date')

class DevInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'record_time', 'content')

class FundValueDeal1Admin(admin.ModelAdmin):
    list_display = ('fund', 'month_income')

    def update(self, request, queryset):
        fund_update_income_all()
        for item in queryset:
            print(item.fund.name)
            print(fund_calc_income_week(item.fund.code))
            print(fund_calc_income_month(item.fund.code))
            print(fund_calc_income_6month(item.fund.code))
        pass

    actions = [update]

admin.site.register(FundInfo, FundInfoAdmin)
admin.site.register(FundDeal, FundDealAdmin)
admin.site.register(FundManager, FundManageAdmin)
admin.site.register(FundValueDeal1, FundValueDeal1Admin)
admin.site.register(DevInfo, DevInfoAdmin)
