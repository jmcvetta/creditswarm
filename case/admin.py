# Copyright (c) 2012 Jason McVetta.

from django.contrib import admin
from case.models import Case
from case.models import Account
from case.models import Inquiry

class CaseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'ts_updated']

class AccountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'case', 'creditor', 'account_number']

class InquiryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'case', 'company_name', 'date']

admin.site.register(Case, CaseAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Inquiry, InquiryAdmin)