from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.container_list, name='list'),
    path('make/', views.make_container, name='make'),
    path('remove/', views.del_container, name='remove'),
    path('power/', views.power_container, name='power'),
    path('email/', views.email, name='email'),
    path('<str:container_id>/', views.detail, name='detail'),
]
