# 쥬피터 컨테이너 관리하는 모듈 by Watson

# 라이브러리 선언을 위한 import
from os import system, chdir, getcwd, listdir
import socket
import subprocess
import re

# 타입힌트를 위한 import
from typing import Any, Dict, List

# 경로 관련된 변수들 선언
home_path: str = None # user 홈 폴더
work_path: str = None # 작업 경로

# HOST_IP 주소 확인하는 함수
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# output값이 필요한 shell command 함수
def command(command: str) -> str:
    output: _io.BufferedReader = subprocess.Popen(
        f"{command}", shell=True, stdout=subprocess.PIPE).stdout
    result: bytes = output.read()
    return result.decode()

# user 홈 폴더 경로 가져오기
home_path = command("echo $HOME").strip()

# 컨테이너 정보 담는 공유 디렉토리 만들기(코드가 길어져서 3줄로 표현하였음)
check_dir: List = listdir(home_path) # 홈 디렉터리 가져오기
if "jupyter_management_storage" not in check_dir: # 공유 디렉터리 없으면 만들고
    print("Not Ready: 공유 디렉터리 존재 하지 않음 -> 공유 디렉터리 생성")
    system(f"mkdir {home_path}/jupyter_management_storage")
else: # 있으면 패쓰~
    print("OK: 경로에 공유 디렉터리가 존재합니다.")

# 컨테이너 정보 담는 디렉토리 경로 가져오기
work_path: str = f"{home_path}/jupyter_management_storage"


# 컨테이너 관리하는 클래스
class Container:
    
    # 자동으로 컨테이너 생성하게
    def __init__ (self) -> None:


    # 커스텀 도커 이미지 있는 지 체크 하는 함수
    def check_image(self) -> None:
        # 이미지 존재하는 지 확인
        image_check: str = command("docker images")

        # 존재하면 pass, 존재하지 않으면 docker image build
        if "image_watson_jupyter" not in image_check.split() :
            print("Not Ready: 커스텀 도커 이미지가 존재하지 않음 -> 이미지 빌드 실행")
            system("docker build -t image_watson_jupyter:0.0.1 . -f jupyter.Dockerfile")
        else:
            print("OK: 커스텀 도커 이미지가 존재합니다.")

    # 컨테이너 생성할때 사용하는 함수
    def init(self) -> None:
        # 이미지 있는 지 체크
        self.check_image()

        # 생성할 컨테이너 네임 입력하기
        container_name: str = input("새로 만들 주피터 컨테이너명 입력: jupyter_")

        # 포트설정(기본 8888)
        host_port: int = 8888 # host
        cont_port: int = 8888 # container

        # 사용중인 컨테이너 포트 확인 하기
        port_check: str = command("docker ps -a").split()
        while True:
            # 겹치는 포트 없으면 스탑 있으면 포트 1씩 더해보기 
            if f":::{str(host_port)}->{cont_port}/tcp" not in port_check:
                break
            # 존재하면 호스트 포트 1씩 증가시키기
            else:
                host_port += 1

        # 하나의 컨테이너의 정보를 담는 디렉터리 생성하기
        system(f"mkdir {work_path}/jupyter_{container_name}")
            
        # 컨테이너 생성 하기
        #print(f"docker run -d -it -p {host_port}:{cont_port} --name jupyter_{container_name} --hostname jupyter_{container_name} -v {work_path}/{container_name}:/container_info image_watson_jupyter:0.0.1")
        system(f"docker run -d -it -p {host_port}:8888 --name jupyter_{container_name} --hostname jupyter_{container_name} -v {work_path}/{container_name}:/container_info image_watson_jupyter:0.0.1")

    # 컨테이너 시작하는 함수
    def start(self, container_name: str) -> None:
        # 컨테이너 시작
        system(f"docker stop {container_name} ")

    # 컨테이너 종료 하는 함수
    def stop(self, container_name: str) -> None:
        # 컨테이너 제거하기
        system(f"docker stop {container_name} ")

    # 컨테이너 삭제 하는 함수
    def remove(self, container_name: str) -> None:
        # 하나의 컨테이너의 정보를 담는 디렉터리 제거하기
        system(f"rm {work_path}/{container_name}")
        # 컨테이너 제거하기
        system(f"docker rm {container_name} ")

# 쥬피터 관련 된 정보 가져오는 클래스
class JupyterInfo:

    # log를 뽑아내는 함수
    def log(self) -> None:
        pass

    # Jupyter 연결에 필요한 정보를 가져와 저장하는 함수
    def connection_info(self, container_name: str) -> None:

        # 커넥션 정보 dict 형태로 정의
        connection_info: Dict = {
            "address" : get_ip_address(),
            "port" : None,
            "token" : None
        }

        # 정규식 선언
        regex_port: Any = re.compile(":[0-9]+") # 포트 정보 뽑는 정규식
        regex_token: Any = re.compile("=[0-9a-zA-Z]+") # 토큰 정보 뽑는 정규식

        # port와 token 정보 가져오기
        output: str = command(f"docker exec -it {container_name} jupyter notebook list")

        # port와 token 정보 connection_info 에 넣기
        connection_info["port"] = regex_port.findall(output)[0][1:]
        connection_info["token"] = regex_token.findall(output)[0][1:]

        print(connection_info)

        # 파일써서 보관하기 (코드가 한줄로 길어지고 지저분 해서 따로 적었음)
        f = open(f"{work_path}/{container_name}/connection_info.txt", 'w')
        f.write(f"[{container_name} 접속방법]\n\n")
        f.write(f"Address: {connection_info['address']}\n")
        f.write(f"Port: {connection_info['port']}\n")
        f.write(f"Token: {connection_info['token']}\n")
        f.close()
    
    # 연결에 필요한 정보를 컨테이너쪽으로 요청하여 이메일로 보낼 수 있도록 하는 함수
    def send_email() -> None:
        pass
        



# 테스트용
if __name__ == "__main__" :
    jupyter_container = Container()
    #jupyter_info = JupyterInfo()
    jupyter_container.init()
    #jupyter_info.connection_info("jupyter_test1")