from so.memory.address_memory import AddressMemory
from so.memory.strategy import Strategy


class MemoryManager:
    def __init__(self, strategy, memory_size):
        self.strategy = strategy
        self.memory = [None] * memory_size

    def get_strategy(self):
        return self.strategy

    def get_memory_size(self):
        return len([block for block in self.memory if block is None])

    def write(self, process):
        if self.strategy == Strategy.FIRST_FIT:
            self.write_using_first_fit(process)
        elif self.strategy == Strategy.BEST_FIT:
            self.write_using_best_fit(process)
        elif self.strategy == Strategy.WORST_FIT:
            self.write_using_worst_fit(process)

    def write_using_first_fit(self, process):
        actual_size = 0
        for i in range(len(self.memory)):
            if self.memory[i] is None:
                self.memory[i] = process
                return
            else:
                if actual_size > 0:
                    start = i - actual_size
                    end = i - 1
                    address = AddressMemory(start, end)
                    if process.size_in_memory <= address.get_size():
                        self.insert_process_in_memory(process, address)
                        break
                actual_size = 0
        self.print_memory_status()

    def print_memory_status(self):
        for item in self.memory:
            print(item)
        print()

    def insert_process_in_memory(self, process, address):
        for i in range(address.start, address.end + 1):
            self.memory[i] = process.id

    def write_using_best_fit(self, process):
        best_fit_index = -1
        best_fit_size = float('inf')

        for i in range(len(self.memory)):
            if self.memory[i] is None:
                block_size = self.find_block_size(i)
                if process.size_in_memory <= block_size < best_fit_size:
                    best_fit_index = i
                    best_fit_size = block_size

        if best_fit_index != -1:
            self.memory[best_fit_index] = process

    def write_using_worst_fit(self, process):
        worst_fit_index = -1
        worst_fit_size = -1

        for i in range(len(self.memory)):
            if self.memory[i] is None:
                block_size = self.find_block_size(i)
                if block_size >= process.size_in_memory and block_size > worst_fit_size:
                    worst_fit_index = i
                    worst_fit_size = block_size

        if worst_fit_index != -1:
            self.memory[worst_fit_index] = process
        else:
            # Handle the case where no suitable space is found.
            pass

    def find_block_size(self, start_index):
        size = 0
        while start_index < len(self.memory) and self.memory[start_index] is None:
            size += 1
            start_index += 1
        return size
