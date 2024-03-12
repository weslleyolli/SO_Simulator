
from so.memory.memory_manager import MemoryManager, Strategy
from so.so_pack.process import Process
from so.so_pack.system_call_type import SystemCallType
from so.cpu.cpu_manager import CpuManager
from so.schedule.schedule import Schedule
from so.so_pack.system_operation import SystemOperation


memory_size = 100
mm = MemoryManager(Strategy.FIRST_FIT, memory_size)
current_memory_size = mm.get_memory_size()
current_strategy = mm.get_strategy()
cm = CpuManager()
schedule = Schedule()
SystemOperation.set_mm(mm)
SystemOperation.set_cm(cm)
SystemOperation.set_schedule(schedule)

# Lista para armazenar os tamanhos dos processos
process_sizes = []

# Função para imprimir os tamanhos dos processos
def print_process_sizes():
    print("Process Sizes:", process_sizes)

def print_total_memory_used():
    total_memory_used = sum(process_sizes)
    print(f"Total Memory Used: {total_memory_used}")

def check_memory_overflow():
    total_memory_used = sum(process_sizes)
    return total_memory_used > memory_size

# Mostrar o tamanho da memoria
print(f"Memory Size: {memory_size}")

# Criar e adicionar o primeiro processo
process1 = Process()
mm.write(process1)
process_sizes.append(process1.get_size_in_memory())
print(f"Process created: {process1.get_id()}, Size: {process1.get_size_in_memory()}")
print_process_sizes()
print_total_memory_used()

# Criar e adicionar o segundo processo
process2 = Process()
mm.write(process2)
process_sizes.append(process2.get_size_in_memory())
print(f"Process created: {process2.get_id()}, Size: {process2.get_size_in_memory()}")
print_process_sizes()
print_total_memory_used()
print(f"Current Strategy Used: {current_strategy}")

if check_memory_overflow():
    print("Memory overflow detected. Handle the situation accordingly.")