from django.contrib import admin
from .models import Document, DocumentBasicForm


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'project', 'creator', 'created_at', 'comments', ]
    list_display_links = ['id', 'client']


class DocumentBasicFormAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'attach_name', 'created_at']
    list_display_links = ['id', 'title']


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentBasicForm, DocumentBasicFormAdmin)