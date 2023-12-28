from django.contrib import admin
from scan.models import ScanReports


class ScanReportsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "report_path")

    def user_info(self, obj):
        return obj.description


admin.site.register(ScanReports, ScanReportsAdmin)