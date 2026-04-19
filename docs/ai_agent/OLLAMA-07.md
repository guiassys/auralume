> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Refatoração da UI para uma Experiência de DAW Profissional

## 🌍 Contexto

- **Aplicação Alvo**: A interface web existente construída com Gradio.
- **Problema**: A interface atual é funcional, mas visualmente básica. Ela não reflete a sofisticação de uma ferramenta de produção musical.
- **Necessidade**: Redesenhar a UI para que ela se assemelhe a uma Digital Audio Workstation (DAW) profissional (ex: Ableton Live, FL Studio), melhorando a identidade visual e a organização dos controles.

## 🎯 Objetivo Principal

Refatorar completamente a interface Gradio para adotar uma estética de DAW, com um tema escuro industrial, acentos em neon e um layout hierárquico e organizado em abas. O objetivo é criar uma experiência de usuário mais imersiva e profissional, sem alterar a lógica de backend.

---

## 🚀 Plano de Implementação

1.  **Definição da Identidade Visual (Tema e Estilo)**:
    - Criar um `gr.Theme` customizado para implementar a estética "Industrial Dark Mode":
        - **Cores**: Fundos em tons de cinza grafite e preto fosco.
        - **Acentos**: Cores como verde neon ou azul elétrico para elementos ativos (botões, sliders, barras de progresso).
        - **Fontes**: Utilizar fontes sans-serif modernas para textos gerais e fontes monoespaçadas para dados numéricos e técnicos.

2.  **Reestruturação do Layout com Abas**:
    - Utilizar `gr.Blocks` como base e organizar a área de trabalho principal com `gr.Tabs`.
    - **Aba 1: "Definições da Faixa"**: Agrupar os controles principais de geração, como `Gênero`, `BPM`, `Tonalidade`, `Humor` e o `Prompt de Estilo`.
    - **Aba 2: "Ajustes de Estúdio"**: Adicionar sliders para futuros controles de pós-processamento, como `Reverb`, `Delay` e `Compressão`.
    - **Aba 3: "Console e Exportação"**: Manter o console de log e adicionar uma visualização de forma de onda (`gr.Waveform`) e as opções de exportação (WAV/MP3).

3.  **Implementação de Componentes Globais**:
    - **Header**: Criar uma seção no topo com o logo da Auralume e um indicador de status do sistema. Incluir uma barra de progresso persistente e fina que fica ativa durante a geração.
    - **Sidebar (Barra Lateral)**: Adicionar uma barra lateral à esquerda com ícones para navegação entre seções principais, como "Estúdio", "Sobre" e "Ajuda".

4.  **Lógica de Interação (UX)**:
    - Garantir que a navegação entre as abas e a barra lateral não seja bloqueada durante o processo de geração.
    - Implementar o bloqueio de estado (`interactive=False`) para os botões "Gerar" e "Limpar" apenas enquanto a música estiver sendo gerada, liberando-os ao final.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando a estrutura do `gr.Theme` customizado e como o layout com `gr.Blocks` e `gr.Tabs` será organizado. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- A interface Gradio utiliza um tema escuro customizado com acentos em neon.
- O layout está organizado em abas (Definições, Ajustes, Console).
- Componentes globais como Header e Sidebar estão implementados.
- A navegação na UI não é bloqueada durante a geração.
- Os botões de ação são devidamente bloqueados e desbloqueados.
- A nova UI está totalmente integrada com o backend existente, sem quebrar nenhuma funcionalidade.
