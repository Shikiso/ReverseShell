import threading
from Variables import all_threads

class Client:
    def __init__(self, IP, Port, conn, Name="Client"):
        self.IP = IP
        self.Port = Port
        self.Name = Name
        self.conn = conn

        self.LastError = ""

        self.LastResponse = ""
        self.Listen_for_response = False

        self.Running = True
    
    def send(self, text):
        try:
            self.conn.send(str.encode(text))
            return 0
        except Exception as e:
            self.LastError = str(e)
            return 1
    
    def recieve(self):
        try:
            response = str(self.conn.recv(1024), 'utf-8')
            self.LastResponse = response
            return 0
        except Exception as e:
            self.LastError = str(e)
    
    def close(self):
        self.Running = False
        self.conn.close()