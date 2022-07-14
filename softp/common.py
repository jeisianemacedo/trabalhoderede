import hashlib
import os
import socket
from time import time


class Address:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

class Connection:
    sock: socket.socket
    def __init__(self, sock: socket, address: Address) -> None:
        self.sock = sock
        self.address = address

class Header:
    attributes: dict

    def __init__(self, attributes: dict = {}):
        self.attributes = attributes

    def serialize(self) -> bytes:
        serialized_data = []
        for parameter_name, parameter in self.attributes.items():
            serialized_data.append("{}:{}".format(parameter_name, parameter))
        serialized_data = '\n'.join(serialized_data)
        serialized_data += "\n\n"
        return bytes(serialized_data, 'utf-8')

    @staticmethod
    def deserialize(serialized_data: str):
        header_end = serialized_data.find("\n\n")
        if header_end == -1 :
            raise Exception("Header doesn't end in double linebreak '\\n\\n' ")
        header = serialized_data[:header_end]
        parameter_lines = header.split("\n")
        attributes = {}
        for parameter_line in parameter_lines:
            parameter_value_separator = parameter_line.find(":")
            if(parameter_value_separator == -1):
                raise Exception("Parameters should have a ':' separating its name and value: {}".format(parameter_line))
            parameter_name, parameter_value = parameter_line.split(":")
            attributes[parameter_name] = parameter_value
        return  Header(attributes)

    @staticmethod
    def createSerializedHeader(self, attributes: dict):
        pass

class Packet:
    header: Header
    content: bytes
    def __init__(self, header_parameters: dict, data: bytes = b"") -> None:
        self.header = Header(header_parameters)
        self.content = data
    
    def to_bytes(self):
        return self.header.serialize() + self.content

