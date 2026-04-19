> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Refatoração para Pipeline de Composição Musical Estruturada

## 🌍 Contexto

- **Aplicação Alvo**: O pipeline de geração de música existente.
- **Problema**: A geração de áudio atual é linear e "monolítica", resultando em músicas sem uma estrutura narrativa clara (ex: introdução, verso, refrão) e com pouca coerência temática.
- **Tecnologia**: A solução deve usar LangChain (LCEL) para orquestrar as etapas e, opcionalmente, FAISS para busca vetorial de embeddings de áudio.

## 🎯 Objetivo Principal

Refatorar o pipeline para que ele gere músicas com uma estrutura musical real (Intro, Verso, Refrão, Outro), garantindo coerência temática entre as seções. A nova arquitetura deve separar claramente a lógica de composição ("o que compor") da renderização de áudio ("como renderizar").

---

## 🚀 Plano de Implementação

A nova arquitetura, chamada **Hierarchical Music Pipeline**, será implementada com `Runnables` do LangChain (LCEL) e dividida em três estágios principais:

1.  **Stage 1: Music Architect (O Planejador)**
    - **Ação**: Recebe o prompt do usuário e a duração total.
    - **Lógica**: Cria um "mapa de execução" (JSON) que define a estrutura da música, dividindo a duração total em seções (Intro, Verso, Refrão, Outro) e injetando palavras-chave para guiar a intensidade de cada uma (ex: "buildup" na intro, "full energy" no refrão). Este estágio também definirá o BPM e a escala/tonalidade (ex: C minor) globais da faixa.

2.  **Stage 2: Contextual Engine (O Compositor)**
    - **Ação**: Gera o áudio de cada seção sequencialmente, usando o mapa de execução como guia.
    - **Lógica de Coerência (RAG)**: Para manter a coerência, o prompt de cada nova seção será enriquecido com informações da seção anterior.
    - **Extensão Avançada (Opcional)**: Gerar embeddings de áudio (ex: CLAP) para cada seção e armazená-los em um Vector Store (FAISS). Isso permitirá uma busca semântica para garantir que o "DNA sonoro" do refrão, por exemplo, seja reutilizado nos versos.

3.  **Stage 3: Audio Engineer (O Pós-Processamento)**
    - **Ação**: Monta a faixa final, unindo as seções de áudio.
    - **Lógica**: Aplica `crossfade` inteligente entre as seções, alinhado ao beat (BPM) para evitar transições abruptas. Realiza a normalização de volume e aplica efeitos como `fade-in` na introdução e `fade-out` no final.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando como os `Runnables` do LCEL serão encadeados e como o "mapa de execução" (JSON) será estruturado para guiar o pipeline. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- O pipeline gera músicas com uma estrutura clara de Intro, Verso, Refrão e Outro.
- As seções da música são tematicamente coerentes.
- A lógica de composição (pipeline) está separada da lógica de renderização de áudio (engine).
- O modelo `MusicGen` é carregado apenas uma vez (padrão Singleton) para otimizar o uso de VRAM.
- O código está modularizado nos arquivos `musicgen_engine.py`, `musicgen_pipeline.py`, e `music_service.py`.
