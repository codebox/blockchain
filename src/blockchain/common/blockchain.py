from blockchain.common.config import config
from blockchain.common.block import Block
import logging

class Blockchain:
    def __init__(self):
        self.blocks = []

    def get_last_block_id(self):
        return self.blocks[-1].id

    def add_block(self, new_block):
        if self.get_last_block_id() == new_block.previous_block_id:
            self.blocks.append(new_block) #TODO verify
        else:
            logging.error('Refused to add new block, previous_block_id does not match') #TODO raise error

    def get_blocks_following(self, root_block_id):
        root_block_index = None

        if not root_block_id:
            root_block_index = 0

        else:
            try:
                root_block_index = next(index + 1 for index,block in enumerate(self.blocks) if block.id == root_block_id)
            except StopIteration:
                pass # we don't have the block that was requested

        return [] if root_block_index is None else self.blocks[root_block_index:]


    def get_balance_for_address(self, address):
        return 100 # TODO
