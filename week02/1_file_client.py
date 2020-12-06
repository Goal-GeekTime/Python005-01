#!/usr/bin/env python
import os
import sys
import socket
import hashlib


'''
   # 使用方式
   >>: get filename
'''


client = socket.socket()
client.connect(('127.0.0.1', 9999))

while True:
    cmd = input(">>:").strip()
    if len(cmd) == 0:
        continue
    # 设定退出条件
    if data == 'exit':
        break
    if cmd.startswith("get"):
        client.send(cmd.encode())
        server_response = client.recv(1024)
        if server_response.decode() == '404':
            print("The file found does not exist!")
            continue
        print("servr response:", server_response)
        client.send(b"ready to recv file")
        file_total_size = int(server_response.decode())
        received_size = 0
        filename = cmd.split()[1]
        fname,fextension = os.path.splitext(filename)
        f = open(fname + "_new" + fextension, "wb")
        m = hashlib.md5()
        while received_size < file_total_size:
            if file_total_size - received_size > 1024:  ## 要收不止一次
                size = 1024
            else:                                       ## 最后剩多少收多少
                size = file_total_size - received_size
                print("last receive:", size)
            data = client.recv(size)
            received_size += len(data)
            m.update(data)
            f.write(data)
            # print(file_total_size,received_size)
        else:
            new_file_md5 = m.hexdigest()
            print("file recv done", received_size, file_total_size)
            f.close()
        server_file_md5 = client.recv(1024)
        print("server file md5:", server_file_md5)
        print("client file md5:", new_file_md5)
client.close()
