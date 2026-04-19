> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Criação de Interface Web com Gradio

## 🌍 Contexto

- **Aplicação Alvo**: O sistema de geração de música já refatorado para um pipeline com LangChain, executado via CLI.
- **Necessidade**: Criar uma interface web amigável para que usuários não-técnicos possam utilizar a ferramenta sem usar a linha de comando.
- **Tecnologia**: A interface deve ser construída utilizando a biblioteca Gradio.

## 🎯 Objetivo Principal

Desenvolver uma interface web com Gradio que sirva como uma camada visual (frontend) para o pipeline de geração de música existente. A interface deve permitir ao usuário inserir os parâmetros, iniciar a geração e fazer o download do resultado, sem alterar a lógica de negócio do pipeline.

---

## 🚀 Plano de Implementação

1.  **Criação da Camada de Serviço**:
    - Desenvolver uma função de serviço (ex: `generate_music_service`) que receba os parâmetros da interface (`nome_da_musica`, `duracao`, `prompt`) e orquestre a chamada ao pipeline LangChain existente.
    - Esta função será responsável por salvar o arquivo de saída em um diretório pré-definido (ex: `/outputs`) e retornar o caminho do arquivo.

2.  **Desenvolvimento da Interface com Gradio**:
    - Utilizar `gradio.Blocks` para estruturar a UI.
    - **Componentes do Formulário**:
        - `gr.Textbox` para "Nome da música".
        - `gr.Dropdown` para "Duração" com opções (30, 60, 90, 180 segundos).
        - `gr.Textbox` para o "Estilo musical" (prompt).
        - `gr.Button` para "Gerar música".
    - **Componentes de Saída**:
        - Um componente de status para indicar que a música está sendo gerada (ex: `gr.Label("Gerando...")`).
        - Um componente de `gr.File` para o download, que ficará visível apenas após a conclusão.

3.  **Integração e Execução**:
    - O botão "Gerar música" acionará a função de serviço.
    - A interface deve permanecer responsiva durante a geração (execução não-bloqueante).
    - Após a conclusão, o caminho do arquivo retornado pelo serviço será usado para habilitar o download.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando a estrutura de arquivos (ex: `web/app.py`, `services/music_service.py`) e como a UI do Gradio irá interagir com a camada de serviço. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- A aplicação web com Gradio está funcional e pode ser executada localmente.
- O formulário captura os inputs do usuário e os passa corretamente para o pipeline.
- O usuário recebe feedback visual durante o processamento.
- O arquivo de música gerado pode ser baixado diretamente pela interface.
- A execução original via CLI permanece funcional.
