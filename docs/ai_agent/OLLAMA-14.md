> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Refatoração da Interface de Usuário e Correção de Erros de Inicialização

## 🌍 Contexto

- **Aplicação Alvo**: Plataforma de geração de música Auralume.
- **Problema Técnico**: A aplicação está falhando ao iniciar devido a dois problemas de compatibilidade com a versão do Gradio utilizada:
    1.  O argumento `vertical_align` não é suportado no construtor `gr.Row`.
    2.  Os parâmetros `theme` e `css` estão sendo passados para `gr.Blocks` em vez do método `launch()`, o que gera um `UserWarning`.
- **Problema de Experiência do Usuário**: O feedback de progresso da geração é uma barra grande e mal posicionada, e a área de download aparece de forma confusa no fluxo do usuário.

## 🎯 Objetivo Principal

Corrigir os erros de inicialização da aplicação e refatorar a interface para melhorar a usabilidade, implementando as seguintes melhorias:

1.  **Correção de Erros Gradio**:
    - Mover os parâmetros `theme` e `css` do construtor `gr.Blocks()` para o método `interface.launch()`.
    - Remover o argumento `vertical_align` do construtor `gr.Row` e implementar o alinhamento vertical via CSS para garantir a compatibilidade.

2.  **Indicador de Progresso Otimizado**:
    - **Substituição**: Substituir a barra de progresso (`gr.Slider`) por um indicador de texto não interativo.
    - **Visual**: O indicador deve exibir um ícone de carregamento (ex: `🔄`) seguido pela porcentagem de progresso. O componente não deve ter bordas e sua altura deve ser a mesma de um botão padrão.
    - **Posicionamento**: O indicador de progresso deve ficar na **mesma linha** que o seletor "Pipeline Type", posicionado à direita.

3.  **Otimizar Layout do Menu Lateral**: Reposicionar o container "Download Files" para baixo do botão "Generate".

4.  **Garantir um Estado Limpo para Nova Geração**: Implementar uma lógica para que, ao iniciar uma nova geração, os resultados anteriores ("Download files" e "Master preview") sejam automaticamente ocultados.

---

## 🚀 Plano de Implementação

### Fase 1: Correção de Erros e Reorganização da UI

1.  **Análise de Código**: Identificar os arquivos `app.py` e `ui_theme.py`.
2.  **Corrigir Inicialização do Gradio (em `app.py`)**:
    - Na linha `with gr.Blocks(...)`, remover os argumentos `theme=auralume_theme` and `css=custom_css`.
    - Na chamada `interface.launch(...)`, adicionar os argumentos `theme=auralume_theme` e `css=custom_css`.
    - Na linha `with gr.Row(elem_id="pipeline-container", ...)` remover o argumento `vertical_align="center"`.
3.  **Ajustar Layout e Estilos**:
    - Em `app.py`, confirmar que um `gr.Row` contém o `pipeline_type_input` e o `progress_indicator`.
    - Em `ui_theme.py`, adicionar CSS à classe `#pipeline-container` para garantir o alinhamento vertical dos itens (ex: `align-items: center;`).
    - Garantir que a classe CSS para o indicador de progresso (`.progress-indicator`) remove a borda e o fundo e ajusta a altura e o alinhamento do texto.
4.  **Mover Container de Download**: Em `app.py`, mover a definição dos componentes `file_output` e `audio_preview` para o menu lateral, abaixo do `generate_btn`.

### Fase 2: Aprimoramento do Fluxo de Interação

1.  **Atualizar Lógica de Progresso**: Em `app.py`, modificar a função `_ui_update_progress` para formatar o status como uma string (ex: "🔄 Rendering... 42%") e passá-la para o `progress_indicator`.
2.  **Implementar Limpeza Automática**: Estender o evento de clique do `generate_btn` para que ele oculte e limpe os componentes `file_output` e `audio_preview` no início da geração.

---

## 🎯 Definição de Concluído

- A aplicação inicia sem nenhum erro ou `UserWarning`.
- O indicador de progresso é um campo de texto sem borda, com a altura de um botão, posicionado à direita do seletor "Pipeline Type".
- O indicador exibe um ícone de carregamento e a porcentagem de progresso durante a execução.
- O container "Download Files" está posicionado abaixo do botão "Generate".
- Clicar em "Generate" oculta imediatamente os resultados da geração anterior.
- Todas as diretrizes do arquivo `@/docs/ai_agent/OLLAMA.md` foram seguidas.
