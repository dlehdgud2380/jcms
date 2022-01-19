from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.container_list, name='list'),
    path('<str:container_id>/', views.detail, name='detail'),
]
