from Crypto.Hash import SHA256
from blockchain.common.encoders import text_to_bytes

def hash(data):
    return SHA256.new(data).digest()

def hash_to_hex(data):
    return SHA256.new(data).hexdigest()

def hash_string_to_hex(text):
    return hash_to_hex(text_to_bytes(text))
