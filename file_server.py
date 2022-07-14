from urllib import response
from common.arguments import get_arguments
from common.file import get_file, save_file
from softp.common import Address
from softp.server import Request, Response, Server


server: Server= None
directory: str = './core'

def setup_server(ip: str, port: int):
    global server
    try:
        server = Server(Address(ip, port))
        setup_server_actions()
    except BaseException as e:
        #do something later, not just throw the same error pls
        raise e

def main():
    global directory
    args = get_arguments()
    p = 4444#CONFIG.PORT
    if hasattr(args, 'p') and args.p == True:
        p = int(args.p)
    if hasattr(args, 'dir') and args.dir == True:
        directory = int(args.dir)
    setup_server(ip='', port=p)
    server.run()


def on_upload(req: Request, res: Response):
    attr = req.header.attributes
    print(attr['name'])
    print(attr['hash'])
    res.respond({'action': 'ok'}, b'')
    save_file(directory, attr['name'], attr['hash'], req.data)
    # pass

def on_download(req: Request, res: Response):
    file = get_file(directory, req.header.attributes['name'])
    res.respond({'action': 'upload', 'content-length': file.content_length, 'hash': file.hash, 'name': file.name})

def setup_server_actions():
    server.setOnAction('upload', on_upload)
    server.setOnAction('download', on_download)
    # server.setOnAction('delete', on_delete)

if __name__ == '__main__':
    main()


