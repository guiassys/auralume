> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Implementação de Streaming de Logs Dinâmico na UI

## 🌍 Contexto

- **Aplicação Alvo**: A interface web existente construída com Gradio.
- **Problema**: A UI exibe logs apenas no final do processo, sem fornecer feedback em tempo real sobre o progresso da geração da música. O usuário não tem visibilidade das etapas de execução, dos parâmetros utilizados ou do tempo de processamento.
- **Necessidade**: Implementar um mecanismo de streaming para que os logs de execução apareçam dinamicamente na interface, simulando um terminal ao vivo.

## 🎯 Objetivo Principal

Evoluir o sistema para suportar observabilidade em tempo real, transmitindo os logs do backend para a interface Gradio à medida que são gerados. O objetivo é melhorar a experiência do usuário, fornecendo visibilidade clara sobre o status do processamento, os parâmetros de entrada e o tempo total de execução.

---

## 🚀 Plano de Implementação

1.  **Criação de um Mecanismo de Streaming de Logs**:
    - Implementar um `LogEmitter` ou um gerenciador de logs centralizado que utilize um gerador (`yield`) ou uma fila (`queue.Queue`) para capturar e transmitir mensagens de log de diferentes partes da aplicação (serviço, orquestrador, pipeline).

2.  **Adaptação da Camada de Serviço**:
    - Modificar o `MusicGenerationService` para que, em vez de retornar apenas o resultado final, ele se torne um gerador (`yield`).
    - A função irá "yieldar" mensagens de log formatadas (ex: `[INFO] Gerando chunk 1/4...`) durante a execução e, por último, o caminho do arquivo de áudio gerado.

3.  **Integração com a Interface (Gradio)**:
    - Ajustar o `gr.Textbox` que funciona como console de log na UI para que ele receba e exiba o fluxo de mensagens "yieldadas" pelo serviço.
    - No início do processo, os primeiros logs a serem exibidos devem ser os parâmetros de entrada (duração, prompt, etc.).
    - Ao final, o último log a ser exibido deve ser o tempo total de processamento (ex: `Tempo total de processamento: 00:01:48`).

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando como o `LogEmitter` será implementado e como a camada de serviço e a interface Gradio serão adaptadas para suportar o streaming com geradores (`yield`). Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- Os logs de execução aparecem em tempo real no console da interface Gradio.
- A UI exibe os parâmetros de entrada no início do processo.
- A UI exibe o tempo total de processamento no final.
- A interface permanece responsiva durante o streaming de logs.
- A funcionalidade de geração de música e o download do arquivo permanecem intactos.
