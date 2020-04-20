from django.contrib import admin
from .models import Equipment, EquipmentAttachment


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'mnfacture', 'product',
                    'product_model', 'serial', 'install_member', 'location', 'install_date', 'comments']
    list_display_links = ['id', 'client']


class EquipmentAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'attach_name',
                    'content_size', 'content_type', 'created_at']
    list_display_links = ['id', ]


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentAttachment, EquipmentAttachmentAdmin)
