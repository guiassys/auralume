> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Reformulação do Backend para Geração de Trilhas Sonoras de Alta Fidelidade

## 🌍 Contexto

- **Aplicação Alvo**: O backend de geração de música (`MusicGenEngine`, `LofiGenerator`, etc.).
- **Problema**: A qualidade do áudio gerado é baixa. As faixas são fragmentadas, não possuem uma estrutura musical discernível (intro, meio, fim), as transições entre segmentos são abruptas e o resultado final frequentemente ignora o prompt do usuário.
- **Necessidade**: Arquitetar e implementar um novo pipeline de geração no backend que produza faixas musicalmente estruturadas, coesas e de alta fidelidade, comparáveis a uma stream de música lofi profissional.

## 🎯 Objetivo Principal

Redesenhar o pipeline de geração de áudio para resolver os problemas de coesão, estrutura e aderência ao prompt. O foco é criar uma experiência auditiva contínua e agradável, implementando técnicas avançadas de condicionamento de modelo, costura de áudio (stitching) e pós-processamento. **Nenhuma alteração deve ser feita na interface do usuário (Gradio)**.

---

## 🚀 Plano de Implementação

1.  **Análise de Causa Raiz e Proposta de Arquitetura (Primeira Etapa)**:
    - Conforme o mandato de execução, a primeira ação será analisar os arquivos (`music_service.py`, `generator.py`, `musicgen_engine.py`, `musicgen_pipeline.py`) para identificar as falhas arquitetônicas que causam a baixa qualidade do áudio.
    - Com base na análise, será proposta uma nova arquitetura de pipeline que resolva os problemas identificados.

2.  **Implementação da Geração Estruturada e Coesa**:
    - **Estrutura Musical**: O novo pipeline irá gerar a música em seções claras: `Intro -> Desenvolvimento -> Outro`.
    - **Costura Contínua (Stitching)**: Para eliminar cortes abruptos, a geração será baseada em "chunks" (segmentos) com sobreposição.
        - **Overlap & Crossfade**: Gerar segmentos de áudio que se sobrepõem (ex: 1-2 segundos) e aplicar um `crossfade` (ex: `constant power`) para criar uma transição musicalmente imperceptível.
        - **Continuidade Harmônica**: Garantir que a tonalidade, o BPM e o humor sejam consistentes entre as transições.
    - **Finalização Suave**: Implementar uma resolução musical na seção "Outro" e um `fade-out` no nível de DSP para evitar finais abruptos.

3.  **Melhoria na Aderência ao Prompt**:
    - **Engenharia de Prompt**: Desenvolver uma etapa que enriquece o prompt simples do usuário em uma entrada de condicionamento detalhada para o MusicGen. (Ex: `"lofi"` -> `"A calm, instrumental lofi track, 90 bpm, C minor key."`).
    - **Condicionamento Consistente**: Assegurar que todas as seções da música sejam geradas a partir deste prompt enriquecido e consistente.

4.  **Pipeline de Pós-Processamento**:
    - Adicionar uma etapa final de processamento de áudio para polir a faixa, incluindo `fade-in/fade-out`, corte de silêncio e, opcionalmente, normalização de volume (LUFS).

5.  **Correção de Armadilhas Técnicas (Audio Conditioning)**:
    - Garantir o tratamento correto dos tensores de áudio, incluindo a forma (`.squeeze(0)`), o tipo de dado (`.to(model.dtype)`) e o dispositivo (`.to(device)`) antes de passá-los para o modelo MusicGen, evitando erros comuns de incompatibilidade.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta DEVE ser a **Análise de Causa Raiz** e a **Proposta de Arquitetura**. Aguarde a confirmação antes de prosseguir com a implementação completa.

---

## 🎯 Definição de Concluído

- O sistema gera uma faixa de 2-3 minutos que soa como uma peça musical única e intencional.
- Não há cliques, estalos ou mudanças abruptas audíveis entre as seções.
- A música possui uma estrutura clara de início, meio e fim.
- O resultado sonoro reflete com precisão o gênero, humor e instrumentação solicitados pelo usuário.
- Todas as alterações foram feitas no backend, sem impactar a UI ou as APIs existentes.
