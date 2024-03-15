# Simulador de Gerenciamento de Memória

Este documento (`README.md`) fornece uma visão geral do simulador de gerenciamento de memória desenvolvido para simular a alocação e desalocação de processos em um ambiente controlado. Abaixo, detalhamos os testes realizados para validar as funcionalidades do simulador, enfocando a alocação de memória com diferentes estratégias e a gestão de erros.

## Testes Realizados

Para garantir a eficácia do simulador no gerenciamento de memória, realizamos uma série de testes documentados aqui. Estes testes visam verificar a funcionalidade de alocação e desalocação de memória, bem como a gestão de erros e a implementação das estratégias de alocação Worst Fit e Best Fit. A seguir, a sequência dos testes realizados:

Para inicializar o simulador basta executar o arquivo "main.py" 

### Passo a Passo dos Testes

1. **Adicionar Processo P1**
   - Ação: Adicionamos um processo `P1` com `20` unidades de memória.
   
2. **Adicionar Processo P2**
   - Ação: Adicionamos um processo `P2` com `38` unidades de memória.
   
3. **Adicionar Processo P3**
   - Ação: Adicionamos um processo `P3` com `38` unidades de memória.
   
4. **Adicionar Processo P4**
   - Ação: Adicionamos um processo `P4` com `20` unidades de memória.
   
5. **Deletar Processo P2**
   - Ação: Procedemos com a exclusão do processo `P2` do simulador.
   
6. **Adicionar Processo P5 com Erro**
   - Ação: Tentativa de adicionar um processo `P5` com `40` unidades de memória.
   - Resultado: A adição falhou, e uma mensagem de erro foi exibida no log, indicando a impossibilidade de alocação devido à insuficiência de memória disponível.
   
7. **Adicionar Processo P6 com Estratégia de Alocação**
   - Ação: Adicionamos um processo `P6` com `8` unidades de memória, utilizando a estratégia de alocação Worst Fit ou Best Fit, conforme configurado.
   - Observação: A seleção da estratégia de alocação depende da configuração prévia do simulador.

### Documentação de Logs

Cada ação realizada durante os testes é documentada como logs, permitindo uma análise detalhada do comportamento do simulador em diferentes cenários de alocação e desalocação de memória. Estes logs servem como uma ferramenta valiosa para o diagnóstico de problemas e para a validação das funcionalidades implementadas.
