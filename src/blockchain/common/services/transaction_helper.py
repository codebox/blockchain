from blockchain.common.transaction import Transaction
from blockchain.common.hash import hash_string_to_hex
import time

def build_transaction(from_address, amount, to_address, key):
    transaction = Transaction(from_address, amount, to_address, key.get_public_key())
    transaction.timestamp = int(time.time() * 1000)

    transaction_data_to_sign = transaction.get_details_for_signature()
    transaction.signature = key.sign(transaction_data_to_sign)
    transaction.id = hash_string_to_hex(str(transaction.signature))

    return transaction

