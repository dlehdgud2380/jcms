from django.contrib import admin
from .models import Container

class DashBoardAdmin(admin.ModelAdmin):
    search_fields = ['container_name']

# Register your models here.
admin.site.register(Container, DashBoardAdmin)