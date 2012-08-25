# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.contrib import admin
from dispute.models import Dispute

class DisputeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'ts_updated']

admin.site.register(Dispute, DisputeAdmin)