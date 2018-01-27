import os.path
from glob import glob
from Crypto.PublicKey import RSA

class Crypto:
    def __init__(self, key_dir, key_format = 'pem', key_size = 1024):
        self.key_dir    = key_dir
        self.key_format = key_format.lower()
        self.key_size   = key_size

    def get_key(self, key_name):
        file_path = self.__get_key_file_path(key_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                return RSA.importKey(f.read())

    def get_keys(self):
        keys = {}
        for file_path in glob('*.{}'.format(self.key_format)):
            with open(file_path, 'rb') as f:
                key      = RSA.importKey(f.read())
                key_name = self.__get_key_name_from_file(f)
                keys[key_name] = key

        return keys

    def generate_key(self, key_name):
        if self.get_key(key_name):
            raise ValueError('a key called {} already exists'.format(key_name))

        key = RSA.generate(self.key_size)
        key_file_path = self.__get_key_file_path(key_name)
        with open(key_file_path, 'wb') as f:
            f.write(key.exportKey(self.key_format.upper()))

        return self.get_key(key_name), key_file_path

    def __get_key_file_path(self, key_name):
        file_name = '{}.{}'.format(key_name, self.key_format)
        return os.path.join(self.key_dir, file_name)

    def __get_key_name_from_file(self, f):
        file_name_without_ext, _ = os.path.splitext(f.name)
        return file_name_without_ext
