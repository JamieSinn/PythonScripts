#!/bin/bash
sh /root/addwebuser.sh $1
sh /root/addphpfpm.sh $1
sh /root/addnginxsite.sh $1
