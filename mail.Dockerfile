#메일 서버용 도커파일 작성 by Watson

# 1. 우분투 설치
FROM ubuntu:18.04

# 2. 메타데이터
LABEL "writeby" = "Watson"
LABEL "purpose" = "Initial Jupyter Notebook Server"

# 3. 패키지 설치 (사용자가 직접 설정해줘야함)
RUN apt update
RUN apt install -y software-properties-common rsyslog mailutils php-auth-sasl postfix certbot nano
RUN nano /etc/postfix/main.cf
RUN nano /etc/postfix/sasl/sasl_passwd
RUN postmap /etc/postfix/sasl/sasl_passwd
RUN chown root:root /etc/postfix/sasl/sasl_passwd
RUN chmod 600 /etc/postfix/sasl/sasl_passwd
RUN sudo service postfix restart
RUN chfn -f "JCMS MailService" root

# 미완성
