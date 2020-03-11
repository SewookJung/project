from django.contrib import admin
from .models import Dept, Client, Product, ProductModel


class DeptAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'updept_id', 'depth', 'created_at']
    list_display_links = ['id', 'name']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'similiar_word', 'created_at']
    list_display_links = ['id', 'name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'makers', 'created_at']
    list_display_links = ['id', 'name']


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product_id', 'created_at']
    list_display_links = ['id', 'name']


admin.site.register(Dept, DeptAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductModel, ProductModelAdmin)
