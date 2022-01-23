from marshal import loads
from typing import Dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.serializers import serialize
from container import Container as ctn, JupyterInfo, get_ip_address, send_mail, Logger
import json
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

    # 해당컨테이너가 담긴 레코드 가져오기
    db_container = Container.objects.get(ctnId=container_id)

    # 이건 컨테이너 리스트 가져오는 것
    container_all = Container.objects.order_by('id')

    context = {
        'container': db_container,
        'container_list': container_all
    }
    return render(request, 'dashboard/container_detail.html', context)

@csrf_exempt
def make_container(request) -> HttpResponseRedirect:
    """
    ### container 만드는 함수
    endpoint: 'dashboard/make/'
    function: POST
    """

    # DB에 넣을 데이터 정의
    ctn_name: str = None
    ctn_id: str = None
    ctn_health: bool = None
    ctn_port: str = None
    ctn_ip: str = None
    jupyter_token: str = None
    client_name: str = None

    '''
    response: Dict= {
        "info": None,
        "data": None
    }

    # request요청별 처리
    if request.method != 'POST':
        response['info'] = 'Error'
        response['data'] = f"Can't response using {request.method}"
    else:
        response['info'] = 'SUCCESS'
        response['data'] = request.POST
    '''

    # 컨테이너 생성 또는 연결
    container = ctn(
        request.POST.get("containerName"), port=request.POST.get("containerPort")
    )
    container_info: Dict = container.info()
    jupyter_server = JupyterInfo(container_info)

    # DB에 저장할 데이터 세팅
    ctn_name = container_info['conName']
    ctn_id = container_info['conId']
    ctn_health = container.health()
    ctn_port = container_info['port']
    ctn_ip = container_info['conIp']
    client_name = request.POST.get("clientName")

    # 쥬피터 토큰 가져오기
    jupyter_token = jupyter_server.info()['token']
    
    # 데이터베이스 반영
    Container.objects.create(
        name=ctn_name,
        ctnId=ctn_id,
        health=ctn_health,
        port=ctn_port,
        ip=ctn_ip,
        jupyterToken=jupyter_token,
        clientName=client_name
    )

    # 접속정보 파일로 저장
    jupyter_server.save_info()

    #return JsonResponse(response)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def del_container(request) -> HttpResponseRedirect:
    """
    ### container 제거하는 함수
    endpoint: 'dashboard/remove/'
    function: POST
    """
    # 제거에 필요한 변수 미리선언
    ctn_name: str = request.POST.get("containerName")

    # 해당 컨테이너에 대해 DB검색
    db_container = Container.objects.get(name=ctn_name)

    # 컨테이너 연결
    container = ctn(db_container)

    # 컨테이너 제거 수행
    db_container.delete() # DB내에 있는 컨테이너 레코드 삭제
    container.remove() # 컨테이너 제거

    return HttpResponseRedirect("http://localhost:8000/dashboard/")

@csrf_exempt
def power_container(request) -> HttpResponseRedirect:
    """
    ### container 파워 관리 함수
    endpoint: 'dashboard/power/'
    function: POST
    """

    # 상태관리에 필요한 변수 미리선언
    ctn_name: str = request.POST.get("containerName")

    # 해당 컨테이너에 대해 DB검색
    db_container = Container.objects.get(name=ctn_name)

    # 컨테이너 연결
    container = ctn(db_container)
    container_info: Dict = container.info()

    # 받아온 HTTP.POST값에 따라서 컨테이너 상태조정
    # 컨테이너를 OFF 할 경우
    if request.POST.get("containerHealth") == 'True':
        container.stop()
        db_container.health = False
        db_container.jupyterToken = "None"
        db_container.save()
    # 컨테이너를 ON 할 경우
    else:
        container.start()
        jupyter_server = JupyterInfo(container_info)
        db_container.health = True
        db_container.jupyterToken = jupyter_server.info()['token']
        db_container.save()

        # 접속정보 파일로 저장
        jupyter_server.save_info()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def email(request) -> HttpResponseRedirect:
    """
    ### container 접속 관련 메일 보내는 함수
    endpoint: 'dashboard/email/'
    function: POST
    """

    # 필요한 변수 미리선언
    ctn_name: str = request.POST.get("containerName")

    # 현재 컨테이너 접속 방법에 대한 이메일 전송
    send_mail(ctn_name)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def log(request) -> JsonResponse:
    """
    ### container 로그 보내주는 함수
    endpoint: 'dashboard/log/'
    function: GET
    """

    print(request.GET.get("ctnName"))

    # 필요한 변수 미리선언
    ctn_name: str = request.GET.get("ctnName")

    logger = Logger(ctn_name)
    logger.record()
    log: str = logger.load()

    
    response_data: Dict = {
        "status": "OK",
        "log": log
    }

    return JsonResponse(response_data)
