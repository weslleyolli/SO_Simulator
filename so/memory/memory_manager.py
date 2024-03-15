from so.memory.address_memory import AddressMemory
from so.memory.strategy import Strategy


class MemoryManager:
    BLUE = '\033[34m'
    RED = '\033[31m'
    NORMAL = '\033[m'
    def __init__(self, memory_size: int = 128, default_strategy=Strategy.FIRST_FIT):
        # Inicializa o gerenciador de memória com um tamanho de memória definido, estratégia de alocação padrão
        # e estruturas de dados para acompanhar a alocação.
        self.strategy = default_strategy
        self.memory = [None] * memory_size # Representa a memória como uma lista, inicialmente vazia (None).
        self.allocated_processes = {} # Dicionário para mapear processos alocados às suas posições de memória.

    def set_strategy(self, strategy):
        # Define a estratégia de alocação de memória.
        self.strategy = strategy

    def allocate(self, process_id, size_in_memory):
        # Tenta alocar memória para um processo com base na estratégia de alocação selecionada.
        start_index = None
        if self.strategy == Strategy.FIRST_FIT:
            start_index = self.allocate_using_first_fit(process_id, size_in_memory)
        elif self.strategy == Strategy.BEST_FIT:
            start_index = self.allocate_using_best_fit(process_id, size_in_memory)
        elif self.strategy == Strategy.WORST_FIT:
            start_index = self.allocate_using_worst_fit(process_id, size_in_memory)

        if start_index is not None and start_index != -1:
            # Se a alocação for bem-sucedida, registra o processo e atualiza a memória.
            end_index = start_index + size_in_memory - 1
            self.allocated_processes[process_id] = AddressMemory(start_index, end_index)
            for i in range(start_index, end_index + 1):
                self.memory[i] = process_id
            print(f"{MemoryManager.BLUE}Processo alocado na posição {start_index}.")
            return True
        else:
            print(f"{MemoryManager.RED}Falha ao alocar memória para o processo {process_id}.")
            return False

    def is_space_free(self, start, size):
        # Verifica se um bloco de memória está livre a partir de um índice de início e um tamanho especificados.
        return all(self.memory[i] is None for i in range(start, min(start + size, len(self.memory))))

    def calculate_free_block_size(self, start):
        # Calcula o tamanho de um bloco de memória livre a partir de um índice de início.
        free_size = 0
        while start + free_size < len(self.memory) and self.memory[start + free_size] is None:
            free_size += 1
        return free_size

    def find_best_fit_block(self, process_id, size):
        # Inicializa as variáveis para acompanhar o melhor índice de início de bloco (best_fit_index)
        best_fit_index = -1
        best_fit_size = float('inf') # o tamanho do melhor bloco (best_fit_size). O tamanho é inicializado com infinito
        current_index = 0
        # Itera sobre a memória para encontrar o melhor bloco de ajuste.
        while current_index < len(self.memory):
            if self.is_space_free(current_index, size):
                # Calcula o tamanho do bloco de memória livre atual.
                free_size = self.calculate_free_block_size(current_index)
                # Se o tamanho do bloco livre atual é suficiente para o processo e menor que o melhor
                # tamanho de bloco encontrado até agora, atualiza as variáveis best_fit_index
                # best_fit_size com as informações do bloco atual.
                if size <= free_size < best_fit_size:
                    best_fit_index = current_index
                    best_fit_size = free_size
            current_index += 1 if self.memory[current_index] is None else self.calculate_free_block_size(
                current_index)
            # Retorna o índice do melhor bloco de ajuste encontrado. Se nenhum bloco for encontrado,
            # retorna -1, indicando falha em encontrar um bloco adequado.
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
        # Desaloca a memória previamente alocada para um processo, liberando o espaço correspondente.
        if process_id in self.allocated_processes:
            address_memory = self.allocated_processes[process_id]
            for i in range(address_memory.get_start(), address_memory.get_end() + 1):
                self.memory[i] = None
            del self.allocated_processes[process_id]
            print(f"{MemoryManager.BLUE}Memória desalocada para o processo {process_id}.")
            return True
        else:
            print(f"{MemoryManager.RED}Nenhuma memória alocada encontrada para o processo {process_id}.")
            return False

    def print_memory_status(self):
        # Imprime o estado atual da memória, mostrando quais blocos estão alocados ou livres.
        print(self.memory)

    def handle_memory_overflow(self, process_id, size_in_memory):
        # Este método é chamado quando não há espaço suficiente disponível na memória para alocar um processo
        print(f"{MemoryManager.RED}Erro: Estouro de memória ao tentar alocar {size_in_memory} unidades para o processo '{process_id}'.")

    def allocate_using_first_fit(self, process_id, size_in_memory)\
        # FIRST FIT procura o primeiro bloco de memória livre grande o suficiente para acomodar o processo.:
        index = self.find_first_fit(size_in_memory) # Encontra o primeiro bloco adequado.
        if index != -1: # Se um bloco foi encontrado...
            for i in range(index, index + size_in_memory): # Aloca memória para o processo.
                self.memory[i] = process_id
            return index # Retorna o índice inicial do bloco de memória alocado.
        else:
            self.handle_memory_overflow(process_id, size_in_memory)
            return None

    def allocate_using_best_fit(self, process_id, size_in_memory):
        # Implementa a estratégia de "melhor ajuste", procurando o menor bloco de memória
        # livre que pode acomodar o processo, minimizando o desperdício de memória.
        best_fit_index = -1
        best_fit_size = float('inf')
        free_space = 0
        start_index = None
        # Percorre a memória para encontrar o bloco de melhor ajuste.
        for i, block in enumerate(self.memory + [None]): # Adiciona None ao final para lidar com o último bloco.
            if block is None: # Se encontrar espaço livre...
                if start_index is None: # E se for o início de um novo bloco livre...
                    start_index = i # Registra o índice inicial
                free_space += 1 # Incrementa o contador de espaço livre.
            if block is not None or i == len(self.memory):
                if free_space >= size_in_memory and free_space < best_fit_size: # Se o bloco atual for adequado...
                    best_fit_index = start_index # Atualiza o melhor índice.
                    best_fit_size = free_space # Atualiza o tamanho do melhor bloco.
                start_index = None # Reseta o índice inicial para o próximo bloco livre.
                free_space = 0 # Reseta o contador de espaço livre.

        return best_fit_index # Retorna o índice do melhor bloco encontrado.

    def allocate_using_worst_fit(self, process_id, size_in_memory):
        # Implementa a estratégia de "pior ajuste", procurando o maior bloco de memória livre disponível
        worst_fit_index = -1
        worst_fit_size = 0
        free_spaces = [] # Lista para armazenar os blocos livres encontrados.

        current_start_index = None
        # Percorre a memória para identificar todos os blocos livres.
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
        # Avalia cada bloco livre para encontrar o "pior ajuste".
        for start_index, size in free_spaces:
            if size >= size_in_memory and size > worst_fit_size:
                worst_fit_index = start_index
                worst_fit_size = size

        return worst_fit_index # Retorna o índice do maior bloco livre encontrado.