#!/usr/bin/env python
import os
import sys
import socket
import hashlib

'''
func description:
    运行客户端，通过ls查看服务端文件内容，通过 "get filename" 下载服务端文件到本地. 

example:
    python xxx.py
    >>: get filename
'''

HOST = '0.0.0.0'
PORT = 9998

def ftp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        cmd = input(">>:").strip()
        # 未输入任何内容，跳过本次循环，继续等待
        if len(cmd) == 0:
            continue
        # 设定退出条件
        if cmd == 'exit':
            break
        # get filename. 客户端下载某个文件
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
            print("basepath: ", os.path.abspath('.'))
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


# main
if __name__ == '__main__':
    ftp_client()
