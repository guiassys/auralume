> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Refatoração Holística para Qualidade e Coerência Musical

## 🌍 Contexto

- **Aplicação Alvo**: A aplicação Auratune como um todo.
- **Problema Crítico**: A aplicação sofre de **perda de contexto** em músicas longas (acima de 30 segundos). A estratégia de "chunking" (dividir em pedaços) é ingênua, gerando cada segmento de forma independente, o que resulta em uma faixa sem identidade musical, com quebras abruptas de estilo e melodia.
- **Causa Raiz**: Existência de dois pipelines de geração: um simples e problemático (`TrackGenerator`) e um avançado, porém inativo (`MusicPipeline`). A perda de contexto ocorre porque o pipeline simples é o que está em uso.

## 🎯 Objetivo Principal

Realizar uma refatoração holística para resolver os problemas de qualidade e coerência, permitindo a geração de faixas de alta qualidade com até 3 minutos de duração. Os objetivos são: unificar a arquitetura em torno do pipeline avançado, implementar uma estratégia de **continuação de áudio** para manter o contexto, otimizar a performance e garantir que o código siga as melhores práticas.

---

## 🚀 Plano de Implementação

### Fase 1: Ativação do Pipeline Avançado com Continuação de Áudio

1.  **Unificação da Arquitetura**:
    - **Desativar o Pipeline Simples**: Remover a lógica de geração em loop do `TrackGenerator`. Esta classe será renomeada para `MusicGenEngine` e sua única responsabilidade será gerar um **único** segmento de áudio a partir de um prompt.
    - **Ativar o Pipeline Avançado**: Modificar o `MusicGenerationService` para que ele utilize exclusivamente o `MusicPipeline` (com seus componentes `MusicArchitect` e `MusicComposer`) como o motor principal de geração.

2.  **Implementação da Continuação de Áudio (Audio Priming)**:
    - Esta é a solução central para a perda de contexto. A lógica será implementada no `MusicComposer`.
    - **Mecanismo**:
        1.  O primeiro "chunk" (ex: 0-30s) é gerado a partir do prompt de texto.
        2.  Um pequeno trecho do final deste chunk (ex: os últimos 2 segundos) é extraído como um "primer" de áudio.
        3.  O próximo chunk é gerado usando tanto o prompt de texto original (para manter o estilo) quanto o "primer" de áudio (para garantir a continuidade musical).
        4.  O novo segmento gerado é "costurado" ao anterior, e o processo se repete.
    - **Configuração**: Este comportamento será controlado via `config.json` com as novas chaves: `use_continuation: true` e `continuation_primer_s: 2`.

### Fase 2: Otimização de Performance

1.  **Lazy Loading do Modelo**:
    - Modificar o `MusicGenEngine` para que o modelo de IA não seja carregado na VRAM na inicialização da aplicação. O carregamento (`AutoModel.from_pretrained(...)`) ocorrerá apenas na primeira vez que o usuário solicitar a geração de uma música, garantindo um startup rápido e menor consumo de recursos.

2.  **Suporte a Quantização**:
    - Adicionar uma opção `quantization` no `config.json` (ex: `"quantization": "8bit"`) para permitir o carregamento do modelo com precisão reduzida. Isso diminui significativamente o uso de VRAM, viabilizando a geração de faixas mais longas em hardware com menos recursos.

### Fase 3: Polimento Final

1.  **Ajustes na UI e Configuração**:
    - Adicionar na aba "Configurações" da UI os controles para as novas funcionalidades: um checkbox para `use_continuation`, um slider para `continuation_primer_s` e um dropdown para `quantization`.
    - Tornar a barra de progresso mais precisa, baseando seu cálculo no número total de "chunks" a serem gerados, que é definido pelo `MusicArchitect`.

2.  **Validação de Configuração**:
    - Implementar uma função `validate_config()` que é chamada na inicialização para verificar se todas as chaves necessárias (incluindo as novas) existem no `config.json`, garantindo a robustez do sistema.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando como o `MusicComposer` implementará a estratégia de continuação de áudio e como o `MusicGenEngine` será modificado para suportar lazy loading e quantização. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- A aplicação utiliza exclusivamente o `MusicPipeline` com a estratégia de continuação de áudio.
- É possível gerar músicas coerentes de até 3 minutos.
- O modelo de IA é carregado apenas sob demanda (lazy loading).
- A quantização do modelo é uma opção configurável na UI e no `config.json`.
- A continuação de áudio é uma opção configurável na UI e no `config.json`.
- A barra de progresso reflete com precisão o andamento da geração.
- O código está limpo, modular e totalmente configurável via `config.json`.
