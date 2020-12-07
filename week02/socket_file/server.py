#!/usr/bin/env python

'''
func description:
    运行服务端，提供本端文件的查询和下载.

example:
    python xxx.py
'''

import os
import hashlib
import socket,os,time

HOST = '0.0.0.0'
PORT = 9998

def ftp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( (HOST, PORT) )
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print("new conn:",addr)
        while True:
            print("等待新指令")
            data = conn.recv(1024)
            if not data:
                print("客户端已断开")
                break
            cmd,filename = data.decode().split()
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

    s.close()

# main
if __name__ == '__main__':
    ftp_server()
