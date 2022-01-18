# !/bin/bash
# Mail send script

read -p "Input container name: " container
cat /jupyter_management_storage/${container}/connection_info.txt | mail -s "${container} info for connection" dlehdgud2380@gmail.com
