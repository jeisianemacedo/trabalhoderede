import socket
import time
from common import *
from softp.common import *


class ClientRequest:
    connection: Connection
    response_data: bytes
    response_header: Header 
    def __init__(self, address: Address) -> None:
        sock = socket.socket()
        sock.connect((address.ip, address.port))
        self.connection = Connection(sock= sock, address= address)
        pass
    
    def send(self, header_parameters: dict, data: bytes = b""):
        packet = Packet(header_parameters, data)
        self.connection.sock.sendall(packet.to_bytes())
        self._wait_response()

    def _wait_response(self):
        MAX_RESPONSE_TIME = 5
        timeLimit = time() + MAX_RESPONSE_TIME
        message = b""

        # Slow, remember to change it. Decoding every time is pretty stupid. 💩💩💩💩💩💩💩💩💩
        while message.decode().find("\n\n") == -1 or time() >= timeLimit:
            message += self.connection.sock.recv(100)
        
        #💩💩💩💩💩💩💩 so I remember to remove and refactor this shit before doing the last commit.
        print(message.decode())
        #💩💩💩💩💩💩💩

        header = Header.deserialize(message.decode())

        k = message.decode().find("\n\n")
        content = b""
        if k+2 < len(message):
            content += message[k+2:]

        if "content-length" in header.attributes:
            while len(content) < header.attributes["content-length"]:
                content += self.connection.sock.recv(100)
        
        self.response_data = content
        self.response_header = header.attributes
        self.connection.sock.close()




class Client:
    address: Address
    response: Packet
    
    def __init__(self) -> None:
        pass

    # def uploadFile(self, address: Address, file: File, redundancy: int):
    #     cr = ClientRequest(address)
    #     cr.send({
    #         'action': 'upload', 
    #         'name': file.name, 
    #         'hash': file.hash,
    #         'redundancy': redundancy,
    #         'content-length': file.content_length
    #     }, file.whole_data())
    #     self.response = Packet(cr.response_header, cr.response_data)

    def send(self, address: Address, header_options: dict, data: bytes):
        cr = ClientRequest(address)
        cr.send(header_options, data)
        self.response = Packet(cr.response_header, cr.response_data)
    
    # def downloadFile(self, file_name: str):
    #     pass
    
    # def changeRedundancy(self, file_name: str, redundancy: int):
    #     pass
    
    # def check_file_status(self, file_name: str):
    #     pass


# c = Client(Address('127.0.0.1', 3001))
# c.uploadFile(File('a.txt'), 1)


