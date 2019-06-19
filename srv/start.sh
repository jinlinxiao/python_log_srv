#!/bin/sh

name="UDPLogServer.py"

sh stop.sh

sleep 1

nohup python2.7 ${name} &

ps -ef|grep ${name}
