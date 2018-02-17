from blockchain.common.network import Network
from blockchain.common.encoders import transaction_decode
from blockchain.common.encoders import bytes_to_text

def on_transaction(transaction_bytes):
    transaction_text = bytes_to_text(transaction_bytes)
    transaction = transaction_decode(transaction_text)
    print('New Transaction: {} from {} to {}'.format(transaction.amount, transaction.from_address, transaction.to_address))

if __name__ == '__main__':
    Network().receive_transaction(on_transaction)
