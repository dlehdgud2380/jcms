from typing import Dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from django.http import JsonResponse
import container
from .models import Container

# Create your views here.
def container_list(request) -> HttpResponse:
    """
    ### container 리스트 출력 함수
    1. endpoint: 'dashboard/'
    2. function: GET
    """
    container_list = Container.objects.order_by('id')
    container = {'container_list': container_list}
    return render(request, 'dashboard/container_list.html', container)

def detail(request, container_id) -> HttpResponse:
    """
    ### container 정보 출력 출력 함수
    1. endpoint: 'dashboard/{container_id}'
    2. function: GET
    """
    
    container_all = Container.objects.order_by('id')
    container = Container.objects.get(ctnId=container_id)
    context = {
        'container': container,
        'container_list': container_all
    }
    return render(request, 'dashboard/container_detail.html', context)

@csrf_exempt
def make_container(request) -> JsonResponse:
    """
    ### container 만드는 함수
    1. endpoint: 'dashboard/make'
    2. function: POST
    """

    response: Dict= {
        "info": "success",
        "data": request.POST
    }

    return JsonResponse(response)
