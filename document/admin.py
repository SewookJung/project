from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'project', 'creator', 'created_at', 'comments', ]
    list_display_links = ['id', 'client']


admin.site.register(Document, DocumentAdmin)