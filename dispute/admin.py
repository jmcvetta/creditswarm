# Copyright (c) 2012 Jason McVetta.

from django.contrib import admin
from dispute.models import Dispute
from dispute.models import Account
from dispute.models import Inquiry

class DisputeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'ts_updated']

class AccountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'dispute', 'creditor', 'account_number']

class InquiryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'dispute', 'company_name', 'date']

admin.site.register(Dispute, DisputeAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Inquiry, InquiryAdmin)