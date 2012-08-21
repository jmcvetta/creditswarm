from django.contrib import admin
from creditdispute.models import Dispute

class DisputeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'ts_updated', 'bureau', 'report_number']

admin.site.register(Dispute, DisputeAdmin)