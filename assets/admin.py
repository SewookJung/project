from django.contrib import admin
from .models import Asset, Assetrent


class AssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'member_name',
                    'mnfacture', 'model', 'cpu', 'memory', 'harddisk', 'closed', 'comments']
    list_display_links = ['id', 'member_name']

class AssetrentAdmin(admin.ModelAdmin):
    list_display = ['id', 'asset',
                    'created', 'stdate', 'eddate', 'member_id', 'return_date', 'comments']
    list_display_links = ['id', 'asset']


admin.site.register(Asset, AssetAdmin)
admin.site.register(Assetrent, AssetrentAdmin)
