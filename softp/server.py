import queue
import socket
import threading
import time
from common import *
from softp.common import *


class Networking:
    def __init__(self) -> None:
        self.socket = socket.socket()
        self.connections =  queue.Queue()
    
    def serve(self, address: Address):
        self.socket.bind((address.ip, address.port))
        self.socket.listen()
        while True:
            sock, addr = self.socket.accept()
            self.connections.put(Connection(sock, addr))
            print('accepted')

    def send(self, address: Address, data):
        self.socket.connect((address.ip, address.port))
        remaining_bytes = len(data)
        while remaining_bytes > 0:
            remaining_bytes -= self.socket.send(data)


    def close(self):
        self.socket.close()


    
class Request:
    connection: Connection
    header: Header
    data: bytes
    def __init__(self, connection: Connection, header: Header, data: bytes) -> None:
       self.connection = connection 
       self.header = header 
       self.data = data 

class Response:
    connection: Connection
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    def respond(self, header_parameters: dict, data: bytes = b''):
        packet = Packet(header_parameters, data)
        self.connection.sock.sendall(packet.to_bytes())
        self.connection.sock.close()


class Server:
    def __init__(self, address: Address) -> None:
        self.request_handlers = {}
        self.default_handler = {}
        self.server = Networking()
        self._address = address

    def handle_request(self, connection: Connection):
        MAX_RESPONSE_TIME = 5
        timeLimit = time() + MAX_RESPONSE_TIME
        message = b""

        # Slow, remember to change it. Decoding every time is pretty stupid. 💩💩💩💩💩💩💩💩💩
        while message.decode().find("\n\n") == -1 or time() >= timeLimit:
            message += connection.sock.recv(100)

        header = Header.deserialize(message.decode())

        k = message.decode().find("\n\n")
        content = b""
        if k+2 < len(message):
            content += message[k+2:]
        
        if "content-length" in header.attributes:
            while len(content) < int(header.attributes["content-length"]):
                content += connection.sock.recv(1000)
        request = Request(connection, header, content)
        response = Response(connection)
        self.request_handlers[header.attributes["action"]](request, response)
        

    def worker(self):
        while True:
            con = self.server.connections.get()
            self.handle_request(con)

    def run(self):
        t = threading.Thread(target= self.worker)
        t.start()
        self.server.serve(self._address)


    def setOnAction(self, action: str, handler):
        self.request_handlers[action] = handler




# def p(req: Request, res: Response):
#     print('he')
#     res.respond({'action': 'ok'})

# s = Server(Address('127.0.0.1', 3001))
# s.setOnAction('upload', p)

# s.run()