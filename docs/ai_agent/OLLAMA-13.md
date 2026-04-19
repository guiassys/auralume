> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Implementação de Seleção de Pipeline (Simples/Avançado) e Tamanho do Modelo

## 🌍 Contexto

- **Aplicação Alvo**: A interface web com Gradio e o backend de geração de música.
- **Problema**: A interface atual, embora poderosa, pode ser complexa para usuários que desejam uma geração rápida baseada apenas em um prompt de estilo. Além disso, o tamanho do modelo de IA é um parâmetro fixo no `config.json`, sem controle direto pelo usuário.
- **Necessidade**: Introduzir um fluxo de geração "Simples" que exija apenas um prompt, e ao mesmo tempo, dar aos usuários do fluxo "Avançado" o controle sobre o tamanho do modelo a ser utilizado.

## 🎯 Objetivo Principal

Implementar duas novas funcionalidades na interface e no backend:
1.  **Seleção de Tamanho do Modelo**: Permitir que o usuário escolha o tamanho do modelo de IA (ex: "small", "medium", "large") a ser usado no processo de geração.
2.  **Seleção de Tipo de Pipeline**: Oferecer uma opção entre um fluxo "Avançado" (o comportamento atual, com todos os parâmetros) e um "Simples", que oculta todos os campos exceto o "Style Prompt" e utiliza um pipeline de backend simplificado.

---

## 🚀 Plano de Implementação

### Fase 1: Implementação do Seletor de Tamanho do Modelo

1.  **Interface (Frontend)**:
    - Na aba "Configurações", adicionar um componente `gr.Dropdown` com o rótulo "Tamanho do modelo".
    - As opções para este dropdown devem ser carregadas do `config.json` (ex: `["small", "medium", "large"]`).
    - O valor padrão selecionado deve ser o `model_size` definido no `config.json`.

2.  **Backend**:
    - O valor selecionado para o tamanho do modelo deve ser passado através da camada de serviço até o `MusicGenEngine`.
    - Modificar o método `load_model()` no `MusicGenEngine` para que ele use o parâmetro `model_size` recebido para carregar a versão correta do modelo do Hugging Face.

### Fase 2: Implementação da Seleção de Tipo de Pipeline (Simples/Avançado)

1.  **Interface (Frontend)**:
    - Adicionar um componente `gr.Radio` no topo da interface com o rótulo "Tipo de pipeline" e as opções: `["Simples", "Avançado"]`. O padrão deve ser "Avançado".
    - **Lógica de Interatividade**:
        - Implementar um gatilho (`.change()`) para este componente de rádio.
        - Se o usuário selecionar **"Simples"**, a função do gatilho deve usar `gr.update(visible=False)` para ocultar todos os outros componentes de entrada do formulário (duração, nome da música, etc.) e as abas de configuração, deixando visível apenas o campo "Style Prompt" e o botão "Gerar".
        - Se o usuário selecionar **"Avançado"**, a função deve usar `gr.update(visible=True)` para reexibir todos os componentes ocultos.

2.  **Backend**:
    - **Roteamento no Serviço**: A função principal no `MusicGenerationService` receberá o novo parâmetro `pipeline_type`. Ela atuará como um roteador:
        - Se `pipeline_type` for "Avançado", ela chamará o `MusicPipeline` existente, como faz atualmente.
        - Se `pipeline_type` for "Simples", ela chamará um novo **Pipeline Simplificado**.
    - **Criação do Pipeline Simplificado**:
        - Criar um novo fluxo ou classe (ex: `SimpleMusicPipeline`).
        - Este pipeline receberá apenas o prompt de texto.
        - Ele irá gerar uma única faixa de curta duração (ex: 30 segundos), sem a complexidade de estrutura (intro/verso/refrão) ou continuação de áudio.
        - Essencialmente, ele fará uma única chamada ao `MusicGenEngine` com o prompt e salvará o resultado.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando:
1.  A lógica de interatividade no Gradio para ocultar/mostrar os campos.
2.  A estrutura do novo Pipeline Simplificado.
3.  Como o `MusicGenerationService` fará o roteamento entre os dois pipelines.
Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- Um seletor para "Tamanho do modelo" existe na UI e o valor escolhido é usado pelo backend.
- Um seletor para "Tipo de pipeline" está presente na UI.
- Ao selecionar "Simples", a UI é simplificada, mostrando apenas o campo de prompt.
- O fluxo "Simples" utiliza um pipeline de backend simplificado e gera música com sucesso.
- O fluxo "Avançado" continua funcionando exatamente como antes, sem nenhuma regressão.
- O comportamento padrão da aplicação ao iniciar é o fluxo "Avançado" com todos os campos visíveis.
