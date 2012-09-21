# Copyright (c) 2012 Jason McVetta.

from django.contrib import admin
from case.models import Case
from case.models import Account
from case.models import Inquiry

def make_draft(modeladmin, request, queryset):
    queryset.update(status='D')
make_draft.short_description = 'Set case status to "Draft"'

class CaseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'status', 'agency', 'report_number', 'ts_updated']
    list_filter = ['status']
    actions = [make_draft]

class AccountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'case', 'creditor', 'account_number']

class InquiryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'case', 'company_name', 'date']

admin.site.register(Case, CaseAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Inquiry, InquiryAdmin)