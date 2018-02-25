import codecs

TEXT_ENCODING = 'UTF-8'

def text_to_bytes(text):
    return text.encode(TEXT_ENCODING)

def bytes_to_text(bytes):
    return bytes.decode(TEXT_ENCODING)

def bytes_to_hex(b):
    return str(codecs.encode(b, 'hex'))[2:-1]
