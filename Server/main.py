import sys
from server import Server
import threading
from Client import Client

class main:
    def __init__(self, Host='127.0.0.1', Port=1234):
        self.Host = Host
        self.Port = Port

        self.current_conn = None
        self.connected = []

        self.Running = True

        self.server = Server(Host, Port)
        if self.server.socket_bind():
            print(self.server.LastError)
            exit()
        
        self.run()
        
    def accept_connections(self):
        while self.Running:
            conn, addr = self.server.socket_accept()
            if conn and addr:
                newClient = Client(addr[0], addr[1], conn, "Client" + str(len(self.connected)))
                self.connected.append(newClient)
    
    def close_connection(self):
        client = self.connected[self.current_conn]
        client.close()
        self.connected.pop(self.current_conn)
        print("Disconnected client {} number {}.".format(client.Name, self.current_conn))

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
                threading.Thread(target=self.accept_connections).start()
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
                try:
                    conn = args[0]
                    try:
                        if int(conn) <= len(self.connected):
                            self.current_conn = int(conn)
                            print("Selected number {}!".format(conn))
                        else:
                            print("Please eneter a valid connection!")
                    except ValueError:
                        print("Please enter the number asigned to the connection.")
                        continue
                except IndexError:
                    print("Selected last connected!")
                    self.current_conn = -1
            
            elif user_input == "shell":
                client = self.connected[self.current_conn]
                while True:
                    client.recieve()
                    print(client.LastResponse, end="")
                    cmd = input("")
                    if cmd == "exit":
                        client.send(cmd)
                        break
                    if (len(str.encode(cmd))) > 0:
                        client.send(cmd)
            
            elif user_input == "close":
                if self.current_conn != None:
                    self.close_connection()
                    self.current_conn = None
                elif args:
                    if args[0] == "all":
                        for _ in range(len(self.connected)):
                            self.current_conn = 0
                            self.close_connection()
                else:
                    print("Please select a client!\nYou can use 'all' to close all connections. e.g 'close all'")


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