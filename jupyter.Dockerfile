#주피터 서버용 도커파일 작성 by Watson

# 1. 우분투 설치
FROM ubuntu:18.04

# 2. 메타데이터
LABEL "writeby" = "Watson"
LABEL "purpose" = "Initial Jupyter Notebook Server"

# 3. 패키지 설치
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install jupyter notebook

# 4. WORKDIR 변경
WORKDIR /root

# 5. 포트개방
EXPOSE 8888

# 4. 패키지 설치 후 쥬피터 노트북 실행
CMD ["/bin/bash"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root"]