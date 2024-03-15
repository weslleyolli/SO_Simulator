from so.cpu.cpu_manager import CpuManager
from so.memory.memory_manager import MemoryManager
from so.memory.strategy import Strategy
from so.so_pack.process import Process
from so.so_pack.system_call_type import SystemCallType

class SystemOperation:
    mm = MemoryManager(Strategy.FIRST_FIT, 128)  # Exemplo: Estratégia e tamanho de memória definidos aqui
    cm = CpuManager()
    schedule = None

    @classmethod
    def get_mm(cls):
        return cls.mm

    @classmethod
    def set_mm(cls, memory_manage):
        cls.mm = memory_manage

    @classmethod
    def get_cm(cls):
        return cls.cm

    @classmethod
    def set_cm(cls, cpu_manager):
        cls.cm = cpu_manager

    @classmethod
    def get_schedule(cls):
        return cls.schedule

    @classmethod
    def set_schedule(cls, scheduler):
        cls.schedule = scheduler

    @classmethod
    def system_call(cls, call_type, process=None):
        if call_type == SystemCallType.CREATE_PROCESS:
            if process:
                allocation_success = cls.mm.allocate(process.get_id(), process.get_size_in_memory())
                if allocation_success:
                    # Adicione o processo ao escalonador ou CPU manager conforme necessário
                    print(f"Memória alocada para o processo {process.get_id()} com sucesso.")
                    return True
                else:
                    print("Falha ao alocar memória para o novo processo.")
                return False
            else:
                print("Processo não fornecido para criação.")
                return False

        elif call_type == SystemCallType.WRITE_PROCESS:
            # Implemente a lógica para escrita (atualização) do processo
            pass

        elif call_type == SystemCallType.DELETE_PROCESS:
            if process:
                cls.mm.deallocate(process.get_id())
                # Remova o processo do escalonador ou CPU manager conforme necessário
                print(f"Processo {process.get_id()} deletado.")
            else:
                print("Processo não especificado para exclusão.")