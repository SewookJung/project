from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'client', 'mnfacture', 'product', 'created_at', 'comments']
    list_display_links = ['id', 'title']


admin.site.register(Project, ProjectAdmin)