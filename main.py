
from so.memory.memory_manager import MemoryManager, Strategy
from so.so_pack.process import Process


def main():
    memory_manager = MemoryManager(128)

    while True:
        print("\nMenu Principal:")
        print("1 - Escolher Estratégia de Alocação de Memória")
        print("2 - Criar Processo")
        print("3 - Deletar Processo")
        print("4 - Sair")
        choice = input("Escolha uma opção (1/2/3/4): ")

        if choice == '1':
            print("\nEscolha a Estratégia de Alocação de Memória:")
            print("1 - First Fit")
            print("2 - Best Fit")
            print("3 - Worst Fit")
            strategy_choice = input("Escolha uma estratégia (1/2/3): ")

            if strategy_choice == '1':
                memory_manager.set_strategy(Strategy.FIRST_FIT)
                print("Estratégia First Fit selecionada.")
            elif strategy_choice == '2':
                memory_manager.set_strategy(Strategy.BEST_FIT)
                print("Estratégia Best Fit selecionada.")
            elif strategy_choice == '3':
                memory_manager.set_strategy(Strategy.WORST_FIT)
                print("Estratégia Worst Fit selecionada.")
            else:
                print("Opção inválida. Por favor, escolha 1, 2 ou 3.")


        elif choice == '2':
            if not memory_manager:
                print("Por favor, selecione uma estratégia de alocação primeiro.")
                continue

            size_in_memory = int(input("Informe o tamanho do processo: "))
            process = Process(size_in_memory)
            success = memory_manager.allocate(process.get_id(), process.get_size_in_memory())
            if success:
                print(
                    f"Processo criado com ID: {process.get_id()} e tamanho de memória: {process.get_size_in_memory()}")
            else:
                print("Erro ao criar processo.")

            memory_manager.print_memory_status()

        elif choice == '3':
            if not memory_manager:
                print("Por favor, selecione uma estratégia de alocação primeiro.")
                continue

            process_id = input("Informe o ID do processo a ser deletado: ")
            success = memory_manager.deallocate(process_id)
            if success:
                print(f"Processo com ID: {process_id} deletado.")
            else:
                print(f"Processo com ID: {process_id} não encontrado.")

        elif choice == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Por favor, escolha entre 1, 2, 3 ou 4.")


if __name__ == "__main__":
    main()