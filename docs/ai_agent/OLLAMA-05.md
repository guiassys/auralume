> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Evolução para Audio-RAG com Referência Sonora

## 🌍 Contexto

- **Aplicação Alvo**: O pipeline de composição musical estruturada.
- **Problema**: A geração atual, embora estruturada, carece de uma identidade sonora forte e consistente, pois o sistema de RAG (Retrieval-Augmented Generation) é baseado em dados simulados (`np.random.rand`) e não em uma referência musical real.
- **Necessidade**: Permitir que o usuário forneça uma música de referência (`.wav`) para guiar o estilo, o timbre e a atmosfera da composição gerada.

## 🎯 Objetivo Principal

Evoluir o sistema para implementar um **Audio-RAG real**. Isso envolve adicionar um campo de upload de arquivo na interface Gradio e refatorar o pipeline para extrair embeddings do áudio de referência, usando-os para garantir coerência estilística em toda a música gerada.

---

## 🚀 Plano de Implementação

1.  **Atualização da Interface (Gradio)**:
    - Adicionar um componente `gr.File` na interface `app.py` para permitir o upload de um arquivo `.wav`. Este campo será opcional.

2.  **Adaptação da Camada de Serviço e Orquestração**:
    - Modificar o `MusicGenerationService` para receber o caminho do arquivo de áudio de referência (se fornecido).
    - Propagar este caminho através do orquestrador (`LofiGenerator`) até o pipeline.

3.  **Refatoração do Pipeline (LCEL) para Audio-RAG**:
    - **No `Stage 1: Music Architect`**: O pipeline receberá o caminho do áudio de referência.
    - **No `Stage 2: Contextual Engine`**:
        - **Substituir o RAG Fictício**: A lógica que gera embeddings aleatórios (`np.random.rand`) será substituída por um processo real.
        - **Extração de Embeddings**: Implementar uma função para extrair embeddings do áudio de referência usando um modelo apropriado (ex: CLAP).
        - **Indexação e Recuperação**: Indexar os embeddings no `SimpleVectorStore` (ou similar) e usá-los para enriquecer os prompts de cada seção da música, garantindo que a geração subsequente (verso, refrão) seja estilisticamente consistente com a referência.

4.  **Melhoria no Logging**:
    - Expandir o console de logs na UI para exibir informações sobre o processo de Audio-RAG, como "Analisando áudio de referência...", "Embeddings extraídos com sucesso", e o tempo total de processamento.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando como o arquivo de áudio será propagado pelas camadas da aplicação e como o `Contextual Engine` será modificado para substituir o RAG fictício pelo processo de extração e uso de embeddings reais. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- A interface Gradio permite o upload opcional de um arquivo `.wav`.
- O sistema funciona corretamente com e sem um áudio de referência.
- O pipeline extrai embeddings do áudio de referência e os utiliza para guiar a geração.
- A música gerada possui uma identidade sonora consistente e alinhada com a referência.
- O log da interface informa o usuário sobre as etapas do Audio-RAG e o tempo total de processamento.
- As alterações são incrementais e não quebram a funcionalidade existente.
