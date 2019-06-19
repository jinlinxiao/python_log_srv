## python_log_srv
Start a udp server, receive msg from client api, then write log with log level. different system write in different log file  
在服务端启动一个UDP Server，用于接收消息，然后按不同的系统和日志级别，写日志文件


### 服务器基本要求
log_srv基于python2.7开发，故服务器必须要支持python 2.7，有python2.7 命令

### 使用说明
1. 启动Server端  
  - 将 srv 目录 移到 服务器
  - 修改 config.py  
      修改侦听的端口 PORT，默认为8888,必要时，还需要修改HOST，默认为0.0.0.0
  - sh start.sh启动server
  - cat nohup.out看是否有异常
  - 执行 ps -ef|grep UDPLogServer.py 检查进程是否存在

**扩展：**  
   可以在 config.py 中定义系统log文件前缀，默认使用前缀为 app  
   可以对各接入log_srv的系统自定义日志格式和日志级别

2. Client端接入
  - 将 api 目录下的 UDPLogApi.py复制到所在工程目录  
  - 配置 Api文件中的常量：  
  HOST, PORT ——  server端侦听的IP和端口  
  
  LogClient的三个成员属性可以在init时改变，以下是属性的默认值和功能说明  
  ```
  SystemName = 'app'  # 当前系统的名称  
  Console = False     # 是否在控制台打印日志，默认不开启
  SendServer = True   # 是否发往服务器端，默认开启
  ```
  UseColor仅在LogApi.py中使用  
  ```
  UseColor = False    # 是否使用colorama 在pytest中没有效果，默认不开启
  ```
  - 在文件中发送日志给server端  
    参见 ```use_client_sample.py``` 示例

**不使用colorama**  
  在colorama模块安装困难时，使用LogApiNoColorama.py为API文件
