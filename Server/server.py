import socket

class Server:
    def __init__(self, Host="127.0.0.1", Port=3000):
        self.Host = Host
        self.Port = Port
        try:
            self.s = socket.socket()
        except socket.error as e:
            print("Socket creation error: " + str(e))

        self.LastError = ""
    
    def socket_bind(self):
        try:
            print("Binding socket to port: " + str(self.Port))
            self.s.bind((self.Host, self.Port))
            self.s.listen(5)
            print("Binded!")
            return 0
        except socket.error as e:
            self.LastError = str(e)
            return 1
    
    def socket_accept(self):
        try:
            conn, address = self.s.accept()
            print("Connection has been established! IP: " + address[0] + " | Port: " + str(address[1]))
            return conn, address
        except OSError:
            return None, None
    
    def socket_close(self):
        self.s.close()

