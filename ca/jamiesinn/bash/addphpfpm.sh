#!/bin/sh
FILE="/etc/php5/fpm/pool.d/$1.conf"

/bin/cat <<EOM >$FILE
[$1]
user = $1 
group = $1 
listen = /var/run/php5-fpm-$1.sock 
listen.owner = www-data 
listen.group = www-data 
php_admin_value[disable_functions] = exec,passthru,shell_exec,system 
php_admin_flag[allow_url_fopen] = off 
pm = dynamic 
pm.max_children = 5 
pm.start_servers = 2 
pm.min_spare_servers = 1 
pm.max_spare_servers = 3
chdir = /
EOM
#echo "File: $FILE has contents:"
#echo `cat $FILE`
