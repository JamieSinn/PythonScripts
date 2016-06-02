#!/bin/sh
FILE="/etc/nginx/sites-available/$1"
/bin/cat <<EOM >$FILE
server {
    listen 80;
    server name _$1;
    return 301 https://$host$request_uri;
}
server {
    listen 443;
    ssl on;
    ssl_certificate /root/cloudflarecert_$1.pem;
    ssl_certificate_key /root/cloudflarekey_$1.pem;
    root /usr/share/nginx/sites/$1;
    index index.php index.html index.htm;
    server_name $1;
    location / {
        try_files \$uri \$uri/ =404;
    }
    location ~ \.php$ {
        try_files \$uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/var/run/php5-fpm-$1.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOM


mkdir /usr/share/nginx/sites/$1
ln -s /etc/nginx/sites-available/$1 /etc/nginx/sites-enabled/$1
