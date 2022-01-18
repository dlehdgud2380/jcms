from django.contrib import admin
from .models import Dashboard
from .models import User

# Register your models here.
admin.site.register(Dashboard)
admin.site.register(User)