# !/bin/bash
# MailServer Setting Script from docker

apt update
apt install -y software-properties-common rsyslog mailutils php-auth-sasl postfix certbot nano wget
wget https://raw.githubusercontent.com/dlehdgud2380/jupyter_container_management_system/beta/sendmail.sh
chmod 777 sendmail.sh
nano /etc/postfix/main.cf
nano /etc/postfix/sasl/sasl_passwd
postmap /etc/postfix/sasl/sasl_passwd
chown root:root /etc/postfix/sasl/sasl_passwd
chmod 600 /etc/postfix/sasl/sasl_passwd
service rsyslog start
service postfix restart
chfn -f "JCMS MailService" root
echo "Please visit https://myaccount.google.com/lesssecureapps and enable app access"