> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Implementação da Aba de Configurações na UI

## 🌍 Contexto

- **Aplicação Alvo**: O sistema de geração de música, que atualmente utiliza diversos parâmetros "hardcoded" (fixos no código).
- **Problema**: A falta de personalização impede que os usuários ajustem o processo de geração para obter resultados diferentes ou otimizar o desempenho. Parâmetros como BPM, tonalidade, duração dos "chunks" e temperatura do modelo estão inacessíveis.
- **Necessidade**: Externalizar esses parâmetros para um arquivo de configuração e expô-los na interface do usuário através de uma nova aba de "Configurações".

## 🎯 Objetivo Principal

Refatorar a aplicação para que todos os parâmetros de geração sejam carregados de um arquivo `config.json` como valores padrão. Implementar uma nova aba "Configurações" na interface Gradio, permitindo que os usuários visualizem e modifiquem esses parâmetros antes de iniciar a geração, dando-lhes controle total sobre o processo.

---

## 🚀 Plano de Implementação

1.  **Externalização dos Parâmetros**:
    - Identificar todos os parâmetros "hardcoded" relevantes no código (ex: `bpm`, `key`, `chunk_duration`, `model_size`, `temperature`).
    - Criar um arquivo `config.json` na raiz do projeto e popular com esses parâmetros e seus valores padrão.

2.  **Criação da Aba de Configurações (Frontend)**:
    - Na interface Gradio, adicionar uma nova `gr.Tab(label="Settings")`.
    - Dentro desta aba, criar componentes de UI correspondentes para cada parâmetro do `config.json`. Utilizar os componentes mais adequados para cada tipo de dado:
        - `gr.Slider` para valores numéricos como `temperature` ou `bpm`.
        - `gr.Dropdown` para valores de escolha limitada como `key` (tonalidade) ou `model_size`.
        - `gr.Textbox` para caminhos de diretório como `output_dir`.
    - Carregar os valores do `config.json` para definir o estado inicial de cada um desses componentes no momento em que a interface é iniciada.

3.  **Integração com o Backend**:
    - Criar uma função utilitária para carregar o `config.json` e fornecer os valores padrão para a aplicação.
    - Refatorar as funções de backend (ex: no `musicgen_engine.py`) para que aceitem os parâmetros de geração como argumentos, em vez de usar valores fixos.
    - Modificar a função que é acionada pelo botão "Gerar" para que ela colete os valores atuais dos componentes da aba "Configurações" e os passe para o backend.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando a estrutura do `config.json`, a lista de componentes da nova aba "Configurações" e como os valores da UI serão passados para a camada de serviço. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- Um arquivo `config.json` existe e contém todos os parâmetros de geração relevantes.
- A aplicação carrega os valores padrão deste arquivo na inicialização.
- Uma nova aba "Configurações" está presente na UI, populada com os componentes corretos e seus valores padrão.
- O usuário pode modificar os valores na aba "Configurações".
- O processo de geração utiliza os valores definidos pelo usuário na UI, substituindo os padrões.
- O fluxo de geração existente continua funcionando normalmente se as configurações não forem alteradas.
