import socket


class Client:

    def __init__(self, host="127.0.0.1", port=6969):
        self.host = host
        self.port = port
        self.sock = self.connect()
    
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def send(self, data):
        self.sock.sendall(data.encode())
        data = self.sock.recv(1024)
        return data

client = Client()
while True:
    command = input("Enter Command -> ")
    if command == "q":
        break
    response = client.send(command)
    print(response)

