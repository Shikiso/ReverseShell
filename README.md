# ReverseShell
A reverse shell I wrote to help when testing on multiple devices. The script works on both Windows and Linux (haven't tried MAC).
The server accepts multiple connections and lets you select which one you want a shell for.

To use the server just run main.py to use default host and port (localhost, 1234) to use your own add your host and port after main.py.
e.g python main.py 192.168.1.11 4000
Then run the 'listen' command to start accepting connections.
After that you can list them by running 'list' they are number 0-...
To select a client run 'select' followed by the number asigned to the client.
When a client is selected you can run 'shell' to gain a shell or 'close' to close the connection.
Use 'close all' to close the connection on all clients.
'exit' to exit out of shell or program.

To use the client just run client.py followed with the host and port.
e.g. python client.py 192.168.1.11 4000
After that it'll do the rest. It tries to connect every 5 seconds.
