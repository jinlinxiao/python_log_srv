#!/bin/sh

# add crontab to keep log_srv is in server
# crontab -e
# */1 * * * * cd /Users/jinlinxiao/PyCode/log_srv/srv; sh monitor.sh >> /Users/jinlinxiao/cron_test.log
#


name="UDPLogServer.py"

p_n=`ps -ef|grep ${name}|grep -v 'grep'|awk '{print $2}'|wc -l`

if [[ ${p_n} -lt 1 ]]; then
    sh start.sh
fi
