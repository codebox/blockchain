from blockchain.common.crypto import Crypto
from blockchain.common.crypto import config

class Blockchain:
    def __init__(self):
        self.blocks = []

        self.difficulty        = config.get('difficulty')
        self.block_size        = config.get('block_size')
        self.block_reward      = config.get('block_reward')
        self.block_reward_from = config.get('block_reward_from')

        self.address_balances = {}

    def get_last_block_id(self):
        return self.blocks[-1].id

    def remove_last_block(self):
        last_block = self.blocks.pop()
        for transaction in last_block.transactions:
            from_address = transaction.from_address
            to_address   = transaction.to_address
            amount       = transaction.amount

            self.address_balances[from_address] += amount
            self.address_balances[to_address]   -= amount

    def add_block(self, new_block):
        if len(self.blocks) == 0:
            if new_block.id == config.get('genesis_block_id'):
                self.blocks.append(new_block)
                return
            else:
                raise ValueError('First block to be added must be the genesis block with id {}'.format(config.get('genesis_block_id')))

        if self.get_last_block_id() != new_block.previous_block_id:
            raise ValueError('Refused to add new block, previous_block_id {} does not match actual previous block {}'
                             .format(new_block.previous_block_id, self.get_last_block_id()))

        if not new_block.is_mineable():
            raise ValueError('Refused to add new block, block is not mineable')

        #TODO check block difficulty

        address_balances = dict(self.address_balances)
        transaction_index = 0
        transaction_ids_for_new_block = set()

        for transaction in new_block.transactions:
            if not Crypto.validate_transaction(transaction):
                raise ValueError('Invalid transaction in new block (bad signature): {}'.format(transaction))

            if self.has_transaction(transaction):
                raise ValueError('Transaction with id {} already exists within the blockchain'.format(transaction.id))

            if transaction.id in transaction_ids_for_new_block:
                raise ValueError('Duplicate transaction in new block, id: {}'.format(transaction.id))

            transaction_ids_for_new_block.add(transaction.id)

            from_address = transaction.from_address
            to_address   = transaction.to_address
            amount       = transaction.amount

            current_from_address_balance = address_balances.get(from_address) or 0
            current_to_address_balance   = address_balances.get(to_address) or 0

            if transaction_index == len(new_block.transactions) - 1:
                # Validate mining reward transaction
                if from_address != self.block_reward_from:
                    raise ValueError('Invalid final transaction in block, from-address must be {} but was {}'
                                     .format(self.block_reward_from, from_address))

                if amount != self.block_reward:
                    raise ValueError('Invalid final transaction in block, amount must be {} but was {}'
                                     .format(self.block_reward, amount))

            else:
                if current_from_address_balance < amount:
                    raise ValueError('Invalid transaction in new block (address {} balance {} insufficient for amount {})'
                                     .format(from_address, current_from_address_balance, amount))

            address_balances[from_address] = current_from_address_balance - amount
            address_balances[to_address]   = current_to_address_balance + amount

            transaction_index += 1

        self.blocks.append(new_block)
        self.address_balances = address_balances

    def get_blocks_following(self, root_block_id):
        root_block_index = None

        if not root_block_id:
            root_block_index = 0

        else:
            try:
                root_block_index = next(index + 1 for index,block in enumerate(self.blocks) if block.id == root_block_id)
            except StopIteration:
                return None

        return [] if root_block_index is None else self.blocks[root_block_index:]

    def get_balance_for_address(self, address):
        return self.address_balances.get(address) or 0

    def has_transaction(self, transaction):
        return any(map(lambda b : b.has_transaction(transaction), self.blocks))
