# !bin/bash
# MailServer container make script

docker run -it -d -p 587:587 -v $HOME/jupyter_management_storage:/jupyter_management_storage --name juMailServer --hostname juMailServer ubuntu:18.04
docker exec -it juMailServer /bin/bash