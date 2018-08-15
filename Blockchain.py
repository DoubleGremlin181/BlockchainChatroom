import hashlib

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode("utf-8") +
                   str(self.timestamp).encode("utf-8") +
                   str(self.data).encode("utf-8") +
                   str(self.previous_hash).encode("utf-8"))
        return sha.hexdigest()

def create_genesis_block(timestamp):
    return Block(0, timestamp, "Genesis Block", "0")

def create_new_block(last_block, timestamp, data):
    this_index = last_block.index + 1
    this_timestamp = timestamp
    this_data = data
    this_previous_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_previous_hash)
