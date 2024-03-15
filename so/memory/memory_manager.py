
from so.memory.address_memory import AddressMemory
from so.memory.strategy import Strategy


class MemoryManager:
    def __init__(self, memory_size: int = 128):
        self.strategy = None
        self.memory = [None] * memory_size
        self.allocated_processes = {}

    def set_strategy(self, strategy):
        self.strategy = strategy

    def allocate(self, process_id, size_in_memory):
        start_index = None
        # Tentativas de alocação
        if self.strategy == Strategy.FIRST_FIT:
            start_index = self.allocate_using_first_fit(process_id, size_in_memory)
        elif self.strategy == Strategy.BEST_FIT:
            start_index = self.allocate_using_best_fit(process_id, size_in_memory)
        elif self.strategy == Strategy.WORST_FIT:
            start_index = self.allocate_using_worst_fit(process_id, size_in_memory)

        if start_index is not None and start_index != -1:  # Se a alocação foi bem-sucedida
            # Aqui, a alocação foi bem-sucedida e você registra o processo
            end_index = start_index + size_in_memory - 1
            self.allocated_processes[process_id] = AddressMemory(start_index, end_index)
            for i in range(start_index, end_index + 1):
                self.memory[i] = process_id
            print(f"Processo {process_id} alocado.")
            return True
        else:
            print(f"Falha ao alocar memória para o processo {process_id}.")
            return False

    def is_space_free(self, start, size):
        return all(self.memory[i] is None for i in range(start, min(start + size, len(self.memory))))

    def calculate_free_block_size(self, start):
        free_size = 0
        while start + free_size < len(self.memory) and self.memory[start + free_size] is None:
            free_size += 1
        return free_size

    def find_best_fit_block(self, process_id, size):
        best_fit_index = -1
        best_fit_size = float('inf')
        current_index = 0

        while current_index < len(self.memory):
            if self.is_space_free(current_index, size):
                free_size = self.calculate_free_block_size(current_index)
                if size <= free_size < best_fit_size:
                    best_fit_index = current_index
                    best_fit_size = free_size
            current_index += 1 if self.memory[current_index] is None else self.calculate_free_block_size(
                current_index)
        return best_fit_index

    def find_worst_fit_block(self, process_id, size_in_memory):
        worst_fit_index = -1
        worst_fit_size = 0

        current_start_index = None
        for i in range(len(self.memory) + 1):
            if i == len(self.memory) or self.memory[i] is not None:
                if current_start_index is not None:
                    current_block_size = i - current_start_index
                    if current_block_size >= size_in_memory and current_block_size > worst_fit_size:
                        worst_fit_index = current_start_index
                        worst_fit_size = current_block_size
                    current_start_index = None
            else:
                if current_start_index is None:
                    current_start_index = i

        return worst_fit_index

    def find_first_fit(self, size):
        free_space = 0
        for i, block in enumerate(self.memory):
            if block is None:
                free_space += 1
                if free_space == size:
                    return i - size + 1
            else:
                free_space = 0
        return -1

    def deallocate(self, process_id):
        if process_id in self.allocated_processes:
            address_memory = self.allocated_processes[process_id]
            for i in range(address_memory.get_start(), address_memory.get_end() + 1):
                self.memory[i] = None  # Limpa a memória ocupada pelo processo
            del self.allocated_processes[process_id]  # Remove do registro de processos alocados
            print(f"Memória desalocada para o processo {process_id}.")
            return True
        else:
            print(f"Nenhuma memória alocada encontrada para o processo {process_id}.")
            return False

    def print_memory_status(self):
        print(self.memory)

    def handle_memory_overflow(self, process_id, size_in_memory):
        print(f"Erro: Estouro de memória ao tentar alocar {size_in_memory} unidades para o processo '{process_id}'.")

    def allocate_using_first_fit(self, process_id, size_in_memory):
        index = self.find_first_fit(size_in_memory)
        if index != -1:  # Se encontrou um espaço adequado
            # Aloca o processo no espaço encontrado
            for i in range(index, index + size_in_memory):
                self.memory[i] = process_id
            return index  # Retorna o índice de início da alocação
        else:
            self.handle_memory_overflow(process_id, size_in_memory)
            return None  # Falha na alocação, retorna None

    def allocate_using_best_fit(self, process_id, size_in_memory):
        best_fit_index = -1
        best_fit_size = float('inf')
        free_space = 0
        start_index = None

        for i, block in enumerate(self.memory + [None]):  # Adiciona None para lidar com o fim da lista
            if block is None:
                if start_index is None:
                    start_index = i
                free_space += 1
            if block is not None or i == len(self.memory):
                if free_space >= size_in_memory and free_space < best_fit_size:
                    best_fit_index = start_index
                    best_fit_size = free_space
                start_index = None
                free_space = 0

        return best_fit_index

    def allocate_using_worst_fit(self, process_id, size_in_memory):
        worst_fit_index = -1
        worst_fit_size = 0
        free_spaces = []

        current_start_index = None
        for i, block in enumerate(self.memory + [None]):
            if block is None:
                if current_start_index is None:
                    current_start_index = i
            else:
                if current_start_index is not None:
                    block_size = i - current_start_index
                    free_spaces.append((current_start_index, block_size))
                    current_start_index = None

        if current_start_index is not None:
            block_size = len(self.memory) - current_start_index
            free_spaces.append((current_start_index, block_size))

        for start_index, size in free_spaces:
            if size >= size_in_memory and size > worst_fit_size:
                worst_fit_index = start_index
                worst_fit_size = size

        return worst_fit_index