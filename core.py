from unicodedata import name
from common.arguments import get_arguments
from softp.client import Client
from softp.common import Address
from softp.server import Request, Response, Server

server: Server= None
file_servers: list= [{'address': '127.0.0.1', 'port': 4444}]
files: dict = {}
def setup_server(ip: str, port: int):
    global server
    try:
        server = Server(Address(ip, port))
        setup_server_actions()
    except BaseException as e:
        #do something later, not just throw the same error pls
        raise e

def main():
    args = get_arguments()
    p = 3042#CONFIG.PORT
    if hasattr(args, 'p') and args.p == True:
        p = int(args.p)

    setup_server(ip='', port=p)
    server.run()

def get_best_servers(amount: int):
    if(amount > len(file_servers)):
        raise Exception("Not enough file servers!")
    return file_servers[:amount]

def add_server_to_file(hash: str, server = str):
    if hash not in files:
        files[hash] = []
    files[hash].append(server)


def send_to_server(server: dict, header: dict, data: bytes):
    c = Client()
    c.send(Address(server['address'], int(server['port'])), header, data)
    if(c.response.header.attributes['action'] == 'ok'):
        add_server_to_file(header['name'])
    return c.response

def get_server_that_has_file(name):
    if (name not in files) or len(files[name]) == 0:
        return None
    return files[name]

def on_upload(req: Request, res: Response):
    redundancy= int(req.header.attributes['redundancy'])
    servers = get_best_servers(redundancy)
    res.respond({'action': 'ok'}, b'')
    for fs in servers:
        awnser = send_to_server(fs, req.header.attributes, req.data)
    return

def on_download(req: Request, res: Response):
    server = get_server_that_has_file(req.header.attributes['name'])
    print(server)
    if (server == None):
        res.respond({'action': 'error'}, b'')
        return
    awnser = send_to_server(server, req.header, req.data)
    header = awnser.header.attributes.copy()
    header['action']= 'ok'
    res.respond(header_parameters=header, data= awnser.content)
        
    pass

def change_redundancy(req: Request, res: Response):
    new_redundancy = req.header.attributes["redundancy"]
    name = req.header.attributes['name']
    redundancy_diff = len(files[name]) - new_redundancy
    if redundancy_diff > 0:
        for i in range(redundancy_diff):
            server_id = files[name].pop()
            header = req.header.attributes.copy()
            header['action']= 'delete'
            awnser = send_to_server(file_servers[server_id], header, req.data)
    else:
        if redundancy_diff > len(file_servers):
            res.respond({'action': 'bad'})
            return
        servers_that_doesnt_have_file = []
        for fs_id in range(file_servers):
            if fs_id not in files[name]:
                servers_that_doesnt_have_file.insert(fs_id)
        for fs_id in servers_that_doesnt_have_file:
            awnser = send_to_server(file_servers[server_id], req.header, req.data)

def delete(req: Request, res: Response):
   for s_id in files[hash]:
            header = req.header.attributes.copy()
            header['action']= 'delete'
            awnser = send_to_server(file_servers[s_id], header, req.data) 
            files[hash].pop()

def setup_server_actions():
    server.setOnAction('upload', on_upload)
    server.setOnAction('download', on_download)
    server.setOnAction('change_redundancy', change_redundancy)
    server.setOnAction('delete', delete)
    # server.setOnAction('ls', lambda e : e)

if __name__ == '__main__':
    main()



