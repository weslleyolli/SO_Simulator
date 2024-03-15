import uuid

class Process:
    def __init__(self, size_in_memory):
        self.id = str(uuid.uuid4())
        self.size_in_memory = size_in_memory  # O tamanho é agora passado como um argumento
        self.address_in_memory = None  # Alocado pelo MemoryManager ao alocar o processo

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