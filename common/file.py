import hashlib
import os


class File:
    name: str
    hash: str
    path: str
    content_length: int
    content: bytes

    def __init__(self, file_path: str) -> None:
        self.content_length = os.path.getsize(file_path)
        self.hash = self._get_md5(file_path)
        self.name = os.path.basename(file_path)
        self.path = file_path
        self.file_descriptor = open(file_path, 'rb')
        self.content = self.file_descriptor.read()

    def _get_md5(self, filename, blocksize=2**20):
        m = hashlib.md5()
        with open(filename , "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        return m.hexdigest()

    def whole_data(self):
        return self.content


def save_file(path: str, name: str, hash: str, content: bytes):
    fullpath = os.path.join(path, name)
    with open(fullpath, 'wb') as fp:
        fp.write(content)

def delete_file(path: str, name: str):
    fullpath = os.path.join(path, name)
    os.remove(fullpath)

def get_file(path: str, name: str):
    fullpath = os.path.join(path, name)
    return File(fullpath)