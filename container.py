# 쥬피터 컨테이너 관리하는 모듈 by Watson

# 라이브러리 선언을 위한 import
from os import system, listdir
import time
import socket
import subprocess
import re
import threading
import datetime
import json

# 타입힌트를 위한 import
from typing import Any, Dict, List

# 경로 관련된 변수들 선언
home_path: str = None  # user 홈 폴더
work_path: str = None  # 작업 경로


def get_ip_address() -> None:
    """
    HOST_IP 주소 확인하는 함수
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def command(command: str) -> str:
    """
    output값이 필요한 shell command 함수
    """
    output: IO[bytes] = subprocess.Popen(
        f"{command}", shell=True, stdout=subprocess.PIPE).stdout
    result: bytes = output.read()
    return result.decode()

# 이메일 컨테이너 확인하는 함수
# def check


# user 홈 폴더 경로 가져오기
home_path = command("echo $HOME").strip()

# 컨테이너 정보 담는 공유 디렉토리 만들기(코드가 길어져서 3줄로 표현하였음)
check_dir: List = listdir(home_path)  # 홈 디렉터리 가져오기
if "jupyter_management_storage" not in check_dir:  # 공유 디렉터리 없으면 만들고
    print("Not Ready: 공유 디렉터리 존재 하지 않음 -> 공유 디렉터리 생성")
    system(f"mkdir {home_path}/jupyter_management_storage")
else:  # 있으면 패쓰~
    print("OK: 경로에 공유 디렉터리가 존재합니다.")

# 컨테이너 정보 담는 디렉토리 경로 가져오기
work_path: str = f"{home_path}/jupyter_management_storage"


class Container:
    """
    컨테이너 한개를 객체로 관리하는 클래스
    * 컨테이너 없는 경우 컨테이너 생성
    * 똑같은 이름의 컨테이너가 존재하는 경우 정보 로딩
    """

    # 자동으로 컨테이너 생성하고 정보 저장
    # 호스트 포트는 8888번 기본값, 지정가능
    def __init__(self, container_name: str) -> None:
        self.container_id: str = None  # 컨테이너 id
        self.container_name: str = None  # 컨테이너 이름
        self.port: Dict = {  # 컨테이너 포트
            "hostPort": None,
            "conPort": None
        }

        # 해당이름의 컨테이너가 이미 생성되어있는 지 확인
        self.container_name = f'jupyter_{container_name}'
        check: str = command(
            f'docker ps -a -f "name={self.container_name}"').split()

        # 설정한 컨테이너 이름으로 컨테이너 만들고 자동 실행
        if self.container_name not in check:
            print(f'error: {self.container_name} not found\n')
            print(f'info: Container makeing\n')
            self.container_name = f"jupyter_{container_name}"  # 컨테이너 이름 설정

            # 컨테이너 포트 설정
            self.port['hostPort'] = 8888
            self.port['conPort'] = 8888

            # 컨테이너 생성
            self.init()

        # 컨테이너가 있다면 정보 가져오기
        else:
            print(f'info: {self.container_name} found\n')
            # 정보불러오기
            path: str = f"{work_path}/{self.container_name}"
            json_file = open(f'{path}/container_info.json', 'r')
            data: Dict = dict(json.loads(json_file.read()))

            # 컨테이너 정보 쓰기
            self.container_id = data['id']
            self.container_name = data['name']
            self.port['hostPort'] = data['hostPort']
            self.port['conPort'] = data['conPort']

    # 커스텀 도커 이미지 있는 지 체크 하는 함수(Private)

    def __check_image(self) -> None:
        check: str = command("docker images")  # 이미지 존재하는 지 확인

        # 존재하면 pass, 존재하지 않으면 docker image build
        if "image_watson_jupyter" not in check.split():
            print("Not Ready: 커스텀 도커 이미지가 존재하지 않음 -> 이미지 빌드 실행")
            system("docker build -t image_watson_jupyter:0.0.1 . -f jupyter.Dockerfile")
        else:
            print("OK: 커스텀 도커 이미지가 존재합니다.")

    def init(self) -> None:
        """
        컨테이너 생성할때 사용하는 함수
        """
        self.__check_image()  # 이미지 있는 지 체크

        # json파일 뺄때 쓰는 dict
        cnt_data: Dict = {
            "name": None,
            "id": None,
            "hostPort": None,
            "conPort": None
        }

        # 포트설정(기본 8888)
        host_port: int = self.port["hostPort"]  # host
        cont_port: int = self.port["conPort"]  # container

        # 사용중인 컨테이너 포트 확인 하기
        port_check: str = command("docker ps -a").split()
        while True:

            # 겹치는 포트 없으면 스탑 있으면 포트 1씩 더해보기
            if f":::{str(host_port)}->{str(cont_port)}/tcp" not in port_check:
                break

            # 존재하면 호스트 포트 1씩 증가시키기
            else:
                host_port += 1
        # 하나의 컨테이너의 정보를 담는 디렉터리 생성하기
        system(f"mkdir {work_path}/{self.container_name}")

        # 컨테이너 생성 하기
        docker_run_command: str = f"docker run -d -it " \
            f"-p {str(host_port)}:{str(cont_port)} " \
            f"--name {self.container_name} " \
            f"--hostname {self.container_name} " \
            f"-v {work_path}/{self.container_name}:/container_info image_watson_jupyter:0.0.1"

        # 컨테이너 ID 가져와서 저장하기
        self.container_id = command(docker_run_command).strip()
        # print(f"id: {self.container_id}")

        # 컨테이너 정보 json파일로 저장하기
        cnt_data['name'] = self.container_name
        cnt_data['id'] = self.container_id
        cnt_data['hostPort'] = host_port
        cnt_data['conPort'] = cont_port

        # 컨테이너 정보 export
        with open(f"{work_path}/{self.container_name}/container_info.json", "w") as json_file:
            json.dump(cnt_data, json_file)

    def start(self) -> None:
        """
        컨테이너 시작하는 함수
        """
        system(f"docker start {self.container_name} ")

    def stop(self) -> None:
        """
        컨테이너 정지 하는 함수
        """
        system(f"docker stop {self.container_name} ")

    def remove(self) -> None:
        """
        컨테이너 삭제 하는 함수
        """

        # 사용중일수도 있으므로 일단 멈춤
        system(f"docker stop {self.container_name}")
        print("(Success stopped)")

        # 하나의 컨테이너의 정보를 담는 디렉터리 제거하기
        system(f"rm -rf {work_path}/{self.container_name}")
        print("(Success Deleted Directory)")

        # 컨테이너 제거하기
        system(f"docker rm {self.container_name}")
        print(f"({self.container_name} removed)")

    def info(self, option: bool = False) -> Dict:
        """
        ## 컨테이너 정보 보여주는 함수
        * Option = True -> tuple형태로 리턴도 하고 print도 함
        * Option = Flase -> print로 정보만 보여줌 (기본값임)
        """
        host_port: str = self.port["hostPort"]  # host포트 가져오기

        # 컨테이너 정보가 담긴 Dict
        container_info: Dict = {
            "conId": self.container_id,
            "conName": self.container_name,
            "port": host_port
        }
        print(
            f"[Container Info]\nid: {self.container_id}\nname: {self.container_name}\nport: {host_port}")
        if option is True:
            return container_info

    def health(self) -> bool:
        """
        ## 컨테이너 상태 확인하는 클래스
        * 컨테이너 구동중인지 확인
        """

        # 명령어 실행해서 확인
        check: str = command(
            f'docker ps -a -f "name={self.container_name}" -f "status=running"').split()

        # 해당 컨테이너가 살아있는 지 확인
        # 살아있으면 True 리턴 죽었으면 False
        if self.container_name not in check:
            return False
        else:
            return True


class JupyterInfo:
    """
    컨테이너 내의 쥬피터 관련 된 정보 가져오는 클래스
    """

    def __init__(self, contiainer_info: Dict, ) -> None:

        # 컨테이너 정보 가져오기
        # key종류: conId, conName, port
        self.get_info: Dict = contiainer_info

        # 컨테이너 이름 저장
        self.container_name: str = contiainer_info['conName']

        # 커넥션 정보 dict 형태로 정의
        self.connection_info: Dict = {
            "conName": self.container_name,
            "conId": self.get_info['conId'],
            "address": get_ip_address(),
            "port": self.get_info['port'],
            "token": None
        }

    def info(self) -> None:
        """
        Jupyter 연결에 필요한 정보를 가져와 저장하는 함수
        """

        # 정규식 선언
        # regex_port: Any = re.compile(":[0-9]+") # 포트 정보 뽑는 정규식
        regex_token: Any = re.compile("=[0-9a-zA-Z]+")  # 토큰 정보 뽑는 정규식

        # port와 token 정보 가져오기
        time.sleep(2)  # 쥬피터 서버 구동을 기다리기 위해 2초 딜레이
        output: str = command(
            f"docker exec -it {self.container_name} jupyter notebook list")

        # port와 token 정보 connection_info 에 넣기
        # self.connection_info["port"] = regex_port.findall(output)[0][1:]
        self.connection_info["token"] = regex_token.findall(output)[0][1:]

        print(self.connection_info)

        # 파일써서 보관하기 (코드가 한줄로 길어지고 지저분 해서 따로 적었음)
        f = open(f"{work_path}/{self.container_name}/connection_info.txt", 'w')
        f.write(f"[{self.container_name} 컨테이너 접속방법]\n\n")
        f.write(f"Container ID: {self.connection_info['conId']}\n")
        f.write(f"Address: {self.connection_info['address']}\n")
        f.write(f"Port: {self.connection_info['port']}\n")
        f.write(f"Token: {self.connection_info['token']}\n")
        f.close()


def send_mail(container_name) -> None:
    """
    jupyter 접속에 필요한 정보를 이메일로 전송하는 함수
    """

    mail_container: str = "juMailServer"  # 메일컨테이너 이름

    # 메일에 들어갈 내용 정리
    # to: str = email
    # subject: str = f"Hello User! check {container_name} info"  # 제목
    # 접속정보가 담긴 디렉터리
    # txt_file: str = f"/jupyter_management_storage/{container_name}/connection_info.txt"

    # 메일 보낼 명령어 입력
    command: str = f"docker exec -it {mail_container} " \
        f"su root -c " \
        f"'echo {container_name} | /bin/bash ./sendmail.sh'"

    print(command)
    system(command)  # 해당 컨테이너에 대한 메일 전송


class Logger(threading.Thread):
    """
    로그 기록 하는 쓰레드 클래스
    """

    def __init__(self, container_name: str, display: bool = False) -> None:
        threading.Thread.__init__(self)
        self.container_name = "jupyter_" + container_name
        self.display = display  # 터미널상에 log를 띄울것인지 아닌지
        print(f"[logger thread start - {display}]")

    def run(self) -> None:
        """
        컨테이너 로그 기록 실행하는 함수
        * 컨테이너 종료되면 같이 종료됨
        """
        option: str = None  # 기록 옵션(터미널에 띄울것인지 아닌지)
        if self.display is True:
            option = "| tee"
        else:
            option = ">"
        system(
            f"docker logs -f {self.container_name} {option} {work_path}/{self.container_name}/log.txt")
        print("[logger thread end]")


# 테스트용
if __name__ == "__main__":
    print("------------container make && print info------------")
    jupyter_test1 = Container("test1")
    con_info = jupyter_test1.info(True)
    #print("\n\n------------jupyter info------------")
    #jupyter_info = JupyterInfo(con_info)
    #jupyter_info.info()
    print("\n\n------------print connection_info.txt------------")
    system(f"cat {work_path}/{con_info['conName']}/connection_info.txt")
    print("\n\n------------print connection_info.txt------------")
    print(f"container status: {jupyter_test1.health()}")
    #print("\n\n------------send mail connection info------------")
    #send_mail("jupyter_test1")
    # print("\n\n------------logging------------")
    # logger = Logger("test1")
    # logger.daemon = True
    # logger.start()
    # print("\n\n------------delete container------------")
    # jupyter_test1.remove()
