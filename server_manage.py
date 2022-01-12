# 쥬피터 컨테이너 관리 파이썬 스크립트 by Watson

from os import system, chdir, getcwd, listdir
from typing import Dict, List
import subprocess
import re

# 경로 관련된 변수들 선언
home_path: str = None # user 홈 폴더
work_path: str = None # 작업 경로

# output값이 필요한 shell command 함수
def command(command: str) -> str:
    output: _io.BufferedReader = subprocess.Popen(
        f"{command}", shell=True, stdout=subprocess.PIPE).stdout
    result: bytes = output.read()
    return result.decode()

# 커스텀 도커 이미지 있는 지 체크 하는 함수
def check_image() -> None:
    # 이미지 존재하는 지 확인
    image_check: str = command("docker images")

    # 존재하면 pass, 존재하지 않으면 docker image build
    if "image_watson_jupyter" not in image_check.split() :
        print("Not Ready: 커스텀 도커 이미지가 존재하지 않음 -> 이미지 빌드 실행")
        system("docker build -t image_watson_jupyter:0.0.1 .")
    else:
        print("OK: 커스텀 도커 이미지가 존재합니다.")

# user 홈 폴더 경로 가져오기
home_path = command("echo $HOME").strip()

# 컨테이너 정보 담는 공유 디렉토리 만들기(코드가 길어져서 3줄로 표현하였음)
check_dir: List = listdir(home_path) # 홈 디렉터리 가져오기
if "jupyter_management_storage" not in check_dir: # 공유 디렉터리 없으면 만들고
    print("Not Ready: 공유 디렉터리 존재 하지 않음 -> 공유 디렉터리 생성")
    system(f"mkdir {home_path}/jupyter_management_storage")
else: # 있으면 패쓰~
    print("OK: 경로에 공유 디렉터리가 존재합니다.")
    pass

# 컨테이너 정보 담는 디렉토리 경로 가져오기
work_path = f"{home_path}/jupyter_management_storage"

# 컨테이너 생성할때 사용하는 함수
def init_container() -> None:
    # 이미지 있는 지 체크
    check_image()

    # 생성할 컨테이너 네임 입력하기
    container_name: str = input("새로 만들 주피터 컨테이너명 입력: jupyter_")

    # 호스트 포트설정
    host_port: int = 8888

    # 사용중인 컨테이너 포트 확인 하기
    port_check: str = command("docker ps -a").split()
    
    while True:
        # 겹치는 포트 없으면 스탑 있으면 포트 1씩 더해보기 
        if str(host_port) not in port_check:
            break  
        else: 
            host_port += 1

    # 하나의 컨테이너의 정보를 담는 디렉터리 생성하기
    system(f"mkdir {work_path}/{container_name}")
        
    # 컨테이너 생성 하기
    system(f"docker run -d -it -p {host_port}:8888 --name jupyter_{container_name} --hostname jupyter_{container_name} -v {work_path}/{container_name}:/container_info image_watson_jupyter:0.0.1")
        
# 컨테이너 시작하는 함수
def start_container() -> None:
    pass

# log 저장하는 함수
def get_log() -> None:
    pass

# 연결에 필요한 정보를 컨테이너쪽으로 요청하여 이메일로 보낼 수 있도록 하는 함수
def send_email(container_name: str) -> None:
    get_connection_info: str = command(f"docker exec -it {container_name} jupyter notebook list")
    print(get_connection_info)

# 쥬피터 컨테이너로부터 가져온 데이터를 가공하여 만드는 함수
def init_info(filename: str) -> None:
    pass

if __name__ == "__main__" : 
    init_container()
    #send_email("jupyter_test1")