from blockchain.common.config import config
from blockchain.common.block import Block

class Blockchain:
    def __init__(self):
        self.blocks = []

    def get_last_block_id(self):
        return self.blocks[-1].id

    def add_block(self, new_block):
        if self.get_last_block_id() == new_block.previous_block_id:
            self.blocks.append(new_block)
        else:
            print('Refused to add new block, previous_block_id does not match') #TODO error

    def get_balance_for_address(self, address):
        return 100 # TODO
