import os.path
from glob import glob
from Crypto.PublicKey import RSA
from blockchain.common.key import Key
from blockchain.common.hash import hash_to_hex
from blockchain.common.config import config
from blockchain.common.utils import text_to_bytes

class Crypto:
    def __init__(self):
        self.key_store_dir = config.get('key_store_dir')
        self.key_format    = config.get('key_format')
        self.key_size      = config.get('key_size')

    @staticmethod
    def validate_signature(data, public_key, signature):
        public_key = RSA.importKey(public_key)
        return Key(None, public_key, None, None).verify(data, signature)

    @staticmethod
    def validate_transaction(transaction):
        signature = transaction.signature
        public_key = text_to_bytes(transaction.public_key)
        transaction_details = text_to_bytes(transaction.get_details_for_signature())
        return Crypto.validate_signature(transaction_details, public_key, signature)

    def __get_address_for_key(self, key):
        return hash_to_hex(key.publickey().exportKey(self.key_format.upper()))

    def get_key(self, key_name):
        file_path = self.__get_key_file_path(key_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                key = RSA.importKey(f.read())
                address = self.__get_address_for_key(key)
                return Key(key_name, key, file_path, address)

    def get_key_by_address(self, key_address):
        for key in self.get_keys():
            if key.address == key_address:
                return key

    def get_keys(self):
        keys = []
        for file_path in glob(os.path.join(self.key_store_dir, '*.{}'.format(self.key_format))):
            with open(file_path, 'rb') as f:
                key_name = self.__get_key_name_from_file(f)
                keys.append(self.get_key(key_name))

        return keys

    def generate_key(self, key_name):
        if self.get_key(key_name):
            raise ValueError('a key called {} already exists'.format(key_name))

        key = RSA.generate(self.key_size)
        key_file_path = self.__get_key_file_path(key_name)
        with open(key_file_path, 'wb') as f:
            f.write(key.exportKey(self.key_format.upper()))

        return self.get_key(key_name)

    def __get_key_file_path(self, key_name):
        file_name = '{}.{}'.format(key_name, self.key_format)
        return os.path.join(self.key_store_dir, file_name)

    def __get_key_name_from_file(self, f):
        file_name_without_ext, _ = os.path.splitext(os.path.basename(f.name))
        return file_name_without_ext
