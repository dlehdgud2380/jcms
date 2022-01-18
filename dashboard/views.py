from django.shortcuts import render
from django.http import HttpResponse
import container
from .models import Dashboard

# Create your views here.
def dashboard(request):
    """
    container 리스트 출력
    """
    container_list = Dashboard.objects.order_by('container_id')
    container = {'container_list': container_list}
    return render(request, 'dashboard/container_list.html', container)