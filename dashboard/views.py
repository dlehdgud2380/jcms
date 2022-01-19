from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
import container
from .models import Container

# Create your views here.
def dashboard():
    pass

def container_list(request):
    """
    container 리스트 출력
    """
    container_list = Container.objects.order_by('id')
    container = {'container_list': container_list}
    return render(request, 'dashboard/container_list.html', container)

def detail(request, container_id):
    """
    container 정보 출력
    """
    container_all = Container.objects.order_by('id')
    container = Container.objects.get(ctnId=container_id)
    context = {
        'container': container,
        'container_list': container_all
    }
    return render(request, 'dashboard/container_detail.html', context)
