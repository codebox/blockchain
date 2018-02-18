from blockchain.common.network import Network
from blockchain.common.encoders import transaction_decode
from blockchain.common.encoders import bytes_to_text
from blockchain.common.crypto import Crypto
from blockchain.common.encoders import text_to_bytes

def validate_transaction(transaction):
    signature = transaction.signature
    public_key = text_to_bytes(transaction.public_key)
    transaction_details = text_to_bytes(transaction.get_details_for_signature())
    return Crypto.validate_signature(transaction_details, public_key, signature)

def on_transaction(transaction_bytes):
    transaction_text = bytes_to_text(transaction_bytes)
    transaction = transaction_decode(transaction_text)
    print('New Transaction: {} from {} to {}'.format(transaction.amount, transaction.from_address, transaction.to_address))
    print('Valid signature' if validate_transaction(transaction) else 'Invalid signature')

if __name__ == '__main__':
    Network().receive_transaction(on_transaction)
