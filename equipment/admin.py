from django.contrib import admin
from .models import Equipment, EquipmentHistory, EquipmentAttachment, Stock, StockAttachment


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'mnfacture', 'product',
                    'product_model', 'serial', 'manager', 'location', 'install_date', 'comments']
    list_display_links = ['id', 'client']


class EquipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment', 'member',
                    'status', 'comments', 'created_at']
    list_display_links = ['id', 'equipment']


class EquipmentAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'attach_name',
                    'content_size', 'content_type', 'created_at']
    list_display_links = ['id', ]


class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_model', 'mnfacture',
                    'serial', 'location', 'receive_date', 'status', 'comments']
    list_display_links = ['id', 'product_model']


class StockAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'attach_name',
                    'content_size', 'content_type', 'created_at']
    list_display_links = ['id']


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentHistory, EquipmentHistoryAdmin)
admin.site.register(EquipmentAttachment, EquipmentAttachmentAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockAttachment, StockAttachmentAdmin)
