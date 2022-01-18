# !/bin/bash
# Mail send script
# please input your email please and copy to email container

read -p "Input container name: " container
cat /jupyter_management_storage/${container}/connection_info.txt | mail -s "${container} info for connection" input@your.email