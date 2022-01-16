from django.contrib import admin
from .models import Dashboard

# Register your models here.
class DashBoardAdmin(admin.ModelAdmin):
    search_fields = ['container_name']


admin.site.register(Dashboard)