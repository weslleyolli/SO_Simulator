from so.cpu.cpu_manager import CpuManager
from so.memory.memory_manager import MemoryManager
from so.memory.strategy import Strategy
from so.so_pack.process import Process
from so.so_pack.system_call_type import SystemCallType

class SystemOperation:
    mm = None
    cm = None
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
    def system_call(cls, type, process=None):
        if type == SystemCallType.WRITE_PROCESS:
            # Implemente a lógica de escrita aqui
            pass
        elif type == SystemCallType.DELETE_PROCESS:
            # Implemente a lógica de exclusão aqui
            pass
        elif type == SystemCallType.CREATE_PROCESS:
            if cls.cm is None:
                cls.cm = CpuManager()
            if cls.mm is None:
                cls.mm = MemoryManager(Strategy.FIRST_FIT)
            return Process()

        return None