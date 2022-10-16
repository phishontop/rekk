import socket
import time
import threading
import random


class serverError(Exception):
    #this will raise an error if class Server has been misused
    pass



class Server:

    def __init__(self, host="127.0.0.1", port=6969):
        self.host = host
        self.port = port
        self.messages = {
            "ping": "pong",
            "hello": "hello there arg1"
        }

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if isinstance(value, int) or isinstance(value, str):
            self._port = int(value)
        else:
            raise serverError("port must be an int")

    def response(self, data):
        parsedData = data.decode().split(",")
        result = self.messages.get(parsedData[0], "command doesn't exist try again")
        if callable(result):
            parsedData.pop(0)
            result = result(*parsedData)
        else:
            parsedResult = result.split(" ")
            for word in parsedResult:
                if "arg" in word:
                    result = result.replace(
                        word,
                        parsedData[int(word.split("arg")[1])]
                    )
        
        print(f"Got: {data}, Pushing: {result}, Type: {type(result)}")
        return str(result).encode()

    def connection(self, conn, addr):
        print(f"Connected by {addr}")
        start = time.perf_counter()*1000
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(self.response(data))

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()
        while True:
            conn, adr = sock.accept()
            threading.Thread(target=self.connection, args=(conn, adr,)).start()

server = Server()
server.run()