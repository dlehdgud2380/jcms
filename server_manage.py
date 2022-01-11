# 쥬피터 컨테이너 관리 파이썬 스크립트 by Watson

from os import system, chdir, getcwd
from typing import Dict, List
import subprocess
import re

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
    if image_check not in "image_watson_jupyter" :
        system("docker build -t image_watson_jupyter:0.0.1 .")
    else:
        pass

# user 홈 폴더 경로 가져오기
home_path: str = command("echo $HOME")

# 컨테이너 정보 담는 공유 디렉토리 만들기(코드가 길어져서 3줄로 표현하였음)
system(f"mkdir {home_path.strip()} jupyter_management_storage")
system(f"mkdir {home_path.strip()} jupyter_management_storage/connection")
system(f"mkdir {home_path.strip()} jupyter_management_storage/log")

# 컨테이너 정보 담는 디렉토리 경로 
work_path: str = f"{home_path.strip()}/jupyter_management_storage"

# 컨테이너 생성할때 사용하는 함수
def init_container() -> None:
    # 이미지 있는 지 체크
    image_check()

    # 생성할 컨테이너 네임 입력하기
    container_name: str = input("input container name: jupyter_")

    # 사용중인 컨테이너 포트 확인 하기
    port_check: str = command("docker ps -a")
    print(port_check)
    
    # 컨테이너 생성 하기
    # system(f"docker run -d -it -p {host_port}:{cont_port} --name jupyter_{container_name} --hostname jupyter_{container_name} image_watson_jupyter:0.0.1")
        
# 컨테이너 시작하는 함수
def start_container() -> None:
    pass

# log 저장하는 함수

# 생성된 정보를 이메일 컨테이너를 통해서 보낼 수 있도록 하는 함수
def send_email() -> None:
    pass

# 쥬피터 컨테이너로부터 가져온 데이터를 가공하여 만드는 함수
def init_info(filename: str) -> None:
    pass

if __name__ == "__main__" : 
    check_image()