from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'product',
                    'member', 'client_manager', 'sales_type', 'support_comment', 'support_date', 'comments', 'created_at', 'update_at']
    list_display_links = ['id', 'client']


admin.site.register(Report, ReportAdmin)
