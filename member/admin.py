from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'name', 'dept',  'status']
    list_display_links = ['member_id', 'name']


admin.site.register(Member, MemberAdmin)
