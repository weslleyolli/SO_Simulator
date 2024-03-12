import uuid
import random

class Process:
    def __init__(self):
        self.id = str(uuid.uuid4())
        given_list = [1, 2, 4, 5, 8, 10, 20, 50, 100]
        self.size_in_memory = random.choice(given_list)

    def get_id(self):
        return self.id

    def get_size_in_memory(self):
        return self.size_in_memory

    def set_size_in_memory(self, size):
        self.size_in_memory = size

    def get_address_in_memory(self):
        return self.address_in_memory

    def set_address_in_memory(self, address):
        self.address_in_memory = address