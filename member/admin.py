from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'member_id', 'name',  'rank', 'dept',  'status']
    list_display_links = ['id', 'member_id']


admin.site.register(Member, MemberAdmin)
