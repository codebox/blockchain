class Key:
    K = ''

    def __init__(self, name, key, key_file_path, address):
        self.name          = name
        self.key           = key
        self.key_file_path = key_file_path
        self.address       = address

    def __prepare_data_for_signing(self, data):
        if isinstance(data, str):
            return data.encode('UTF-8')
        return data

    def sign(self, unsigned_data):
        return self.key.sign(self.__prepare_data_for_signing(unsigned_data), Key.K)[0]

    def verify(self, unsigned_data, signature):
        return self.key.verify(self.__prepare_data_for_signing(unsigned_data), (signature, Key.K))

    def __repr__(self):
        return '{} {}'.format(self.name, self.address)