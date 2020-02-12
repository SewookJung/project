from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'member_id',
                    'member_name', 'member_dept', 'member_rank', 'member_status']
    list_display_links = ['id', 'member_id', 'member_name']


admin.site.register(Member, MemberAdmin)

# Register your models here.
