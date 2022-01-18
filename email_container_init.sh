# !bin/bash
# MailServer container make script

docker run -it -d -p 587:587 -v $HOME/jupyter_management_storage:/jupyter_management_storage --name juMailServer --hostname juMailServer ubuntu:18.04
docker exec juMailServer apt update 
docker exec juMailServer apt install -y wget
docker exec juMailServer wget https://raw.githubusercontent.com/dlehdgud2380/jupyter_container_management_system/beta/mailsetting.sh
docker exec juMailServer chmod 777 mailsetting.sh
docker exec -it juMailServer /bin/bash