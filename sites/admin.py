from django.contrib import admin
from .models import Project, Document, DocumentAttachment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'client', 'product', 'model',
                    'status', 'created_at', 'update_at', 'comments']
    list_display_links = ['id', 'title']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id',  'project', 'member',
                    'kind', 'created_at', 'comments']
    list_display_links = ['id', 'project']


class DocumentAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id',  'document', 'attach_name',
                    'content_size', 'content_type', 'check_code', 'created_at']
    list_display_links = ['id', 'document']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentAttachment, DocumentAttachmentAdmin)
