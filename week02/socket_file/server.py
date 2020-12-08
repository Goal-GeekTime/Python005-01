#!/usr/bin/env python

"""
func description:
    服务端，提供本端文件列表的查询和下载.

example:
    python xxx.py
"""

import os
import time
import hashlib
import socket

HOST = '0.0.0.0'
PORT = 9999

def ftp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( (HOST, PORT) )
    s.listen(1)
    print('服务端已经开始运行：')

    while True:
        conn, addr = s.accept()
        print("new conn:",addr)
        while True:
            print("等待新指令")
            data = conn.recv(1024)
            print(data)
            if not data:
                print("客户端已断开")
                break
            try:
                cmd,filename = data.decode().split()
            except ValueError as e:
                cmd = data.decode().split()
                filename = None
            # 查询Server端文件列表：'ls'.
            if not filename:
                cmd_res=os.popen(data.decode()).read()
                print("before send data:", len(cmd_res))
                if len(cmd_res) == 0:
                    cmd_res = "command has no output..."
                conn.send(str(len(cmd_res.encode())).encode("utf-8"))  ## 统计字节

                # time.sleep(0.5)                                       ## 解决粘包
                client_ack = conn.recv(1024)

                conn.send(cmd_res.encode('utf-8'))
                print("send done")
            # 从 Server 端下载文件：'get filename'.
            else:
                if os.path.isfile(filename):
                    f = open(filename,"rb")
                    m = hashlib.md5()
                    file_size = os.stat(filename).st_size
                    conn.send( str(file_size).encode() )    # send file size
                    conn.recv(1024)                         # wait for ack
                    for line in f:
                        m.update(line)
                        conn.send(line)
                    print("file md5", m.hexdigest())
                    f.close()
                    conn.send(m.hexdigest().encode())       # send md5
                else:
                    print("The file: %s is not found" % filename)
                    conn.send('404'.encode())
                print("send done")
    # 关闭套接字
    s.close()

# main
if __name__ == '__main__':
    ftp_server()
