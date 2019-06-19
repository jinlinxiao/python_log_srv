#!/bin/sh

name="UDPLogServer.py"

ps -ef|grep ${name}|grep -v 'grep'

p_n=`ps -ef|grep ${name}|grep -v 'grep'|awk '{print $2}'`
echo "kill "${p_n}
ps -ef|grep ${name}|grep -v 'grep'|awk '{print $2}'|xargs kill -9

ps -ef|grep ${name}|grep -v 'grep'

echo "stopped"
