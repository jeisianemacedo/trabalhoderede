from common.arguments import get_arguments
from common.file import File
from softp.client import Client
from softp.common import Address

def send_to_server(server: dict, header: dict, data: bytes):
    c = Client()
    c.send(Address(server['address'], server['port']), header, data)
    return c.response

def upload_file(file_path: str):
    file = File(file_path)
    send_to_server({'address': '127.0.0.1', 'port': 3042}, {'action': 'upload', 'content-length': file.content_length, 'hash': file.hash, 'name': file.name, 'redundancy': '1'}, file.content)

def download_file():
    send_to_server({'address': '127.0.0.1', 'port': 3042}, {'action': 'download', 'name': 'a.txt'}, b'')


upload_file('a.txt')
download_file()