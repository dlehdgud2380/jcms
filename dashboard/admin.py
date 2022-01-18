from django.contrib import admin
from .models import Dashboard

class DashBoardAdmin(admin.ModelAdmin):
    search_fields = ['container_name']

# Register your models here.
admin.site.register(Dashboard, DashBoardAdmin)