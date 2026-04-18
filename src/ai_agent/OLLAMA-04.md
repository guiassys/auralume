# Prompt: Refatoração Auralume - Pipeline de Composição Musical Estruturada

Você é um Engenheiro de Software Sênior especialista em IA Generativa, Áudio Digital e LangChain. 

Sua missão é refatorar o projeto **Auralume** (localizado em `src/scripts/`) para que ele deixe de gerar áudio linear e passe a produzir músicas com estrutura narrativa real (Intro, Verso, Refrão e Outro), utilizando técnicas inspiradas em RAG para manter a coerência temática.

---

## 1. CONTEXTO TÉCNICO
O sistema atual utiliza o modelo `MusicGen` da Meta (Hugging Face) e um wrapper em LangChain. O problema central é que a geração atual é "monolítica" e sofre de amnésia musical, resultando em faixas que não têm progressão ou um final definido.

---

## 2. OBJETIVO DA REFATORAÇÃO
Implementar um **Hierarchical Music Pipeline** usando LangChain (LCEL) para organizar a geração em estágios lógicos, garantindo:

- **Estrutura de Música Real:** Divisão em seções com intensidades diferentes.
- **Coerência Temática:** O refrão e os versos devem compartilhar o mesmo DNA sonoro.
- **Código Limpo:** Separação clara entre a lógica de "O que compor" (Pipeline) e "Como renderizar" (Engine).
- **Alterações minimas:** Evite alterar o que já está funcional.
- **Idioma:** Comentários e mensagens de sistema devem ser no idioma Inglês.
- **Regra:** Não remova logs de sistema de forma indevida. É importante que o desenvolvedor possa acompanhar os logs para acompanhar o status do processamento.

### 🔥 Melhorias Avançadas (Extensão do Objetivo)

Além dos pontos acima, o sistema deve evoluir para incluir:

- **Embeddings de Áudio (RAG real):**
  - Gerar embeddings vetoriais das seções de áudio.
  - Permitir recuperação semântica entre trechos já gerados.
  
- **Memória Vetorial com FAISS:**
  - Indexar embeddings de áudio e descrições textuais.
  - Permitir reutilização de contexto musical entre seções.

- **Cache de Motivos Musicais:**
  - Identificar padrões recorrentes (melodia, ritmo, textura).
  - Reutilizar no refrão e variações ao longo da música.

- **Controle Harmônico (Key / Scale):**
  - Garantir consistência tonal entre as seções.
  - Permitir modulações controladas quando necessário.

- **Beat Alignment entre seções:**
  - Garantir que transições ocorram em múltiplos de compasso.
  - Evitar cortes fora do tempo (glitches rítmicos).

---

## 3. NOVA ARQUITETURA DO PIPELINE (LCEL)

O novo processo deve ser dividido nos seguintes `Runnables`:

### A. Stage 1: Music Architect (O Planejador)
- **Ação:** Recebe o prompt do usuário e a duração total.
- **Saída:** Um mapa de execução (JSON) que divide o tempo total em seções (ex: Intro 10%, Verso 40%, Refrão 35%, Outro 15%).
- **Lógica:** Deve injetar palavras-chave específicas para cada seção (ex: "buildup" na intro, "full energy" no refrão).

#### ➕ Extensões obrigatórias:
- Definir **BPM global** da faixa.
- Definir **Key/Scale (ex: C minor, A major)**.
- Incluir metadados estruturais que serão usados pelas próximas etapas.

---

### B. Stage 2: Contextual Engine (O Compositor)
- **Ação:** Gerar cada seção sequencialmente.

#### Técnica de Coerência (RAG):
- Implementar uma lógica onde o "prompt" de uma seção carrega referências da seção anterior para evitar mudanças bruscas de instrumentos.

#### ➕ Extensões obrigatórias:

- **RAG Multimodal (Texto + Áudio):**
  - Armazenar embeddings das seções já geradas.
  - Recuperar trechos semanticamente similares.

- **Integração com FAISS:**
  - Indexar embeddings para busca eficiente.
  - Permitir queries como:
    - "recuperar contexto semelhante ao refrão"

- **Cache de Motivos Musicais:**
  - Extrair características recorrentes
  - Reutilizar padrões no Chorus

- **Injeção de Contexto Harmônico:**
  - Garantir que prompts incluam:
    - key
    - scale
    - progressão consistente

---

### C. Stage 3: Audio Engineer (O Pós-Processamento)
- **Ação:** Realizar o crossfade inteligente entre as seções geradas, normalização de volume (Loudness) e aplicação de efeitos básicos (como um Fade-Out no final da seção 'Outro').

#### ➕ Extensões obrigatórias:

- **Beat Alignment:**
  - Ajustar cortes com base no BPM.
  - Garantir transições em:
    - múltiplos de 4 beats (compasso)
    - 8 ou 16 barras

- **Tratamento de Transições:**
  - Evitar sobreposição fora de fase
  - Sincronizar envelopes de volume

- **Efeitos inteligentes:**
  - Intro: fade-in
  - Chorus: leve saturação/boost
  - Outro: fade-out + decay

---

## 4. REQUISITOS DE IMPLEMENTAÇÃO

- **LangChain:** Usar `RunnableLambda` ou `SequentialChain` para orquestrar as etapas.
- **MusicGen Optimization:** Garantir que o modelo seja carregado na GPU (CUDA) uma única vez (Singleton) para evitar overhead.
- **Modularidade:** Manter o `MusicGenEngine` focado em tensores/inferência e o `MusicPipeline` focado em lógica de negócio/prompts.
- **Estilo de Código:** Pythonic, com Tipagem (Typing), Logging detalhado e tratamento de erros para falhas de memória (VRAM).

### ➕ Extensões Técnicas:

- Implementar camada de **Vector Store (FAISS)** para embeddings.
- Utilizar modelo de embeddings de áudio (ex: CLAP ou similar).
- Garantir baixo overhead na geração de embeddings.
- Estruturar código para futura expansão (memória musical persistente).

---

## 5. SAÍDA ESPERADA

Forneça a implementação completa para os seguintes arquivos:

1. `musicgen_engine.py`: Refatorado para suportar geração modular.
2. `musicgen_pipeline.py`: O coração da lógica de estrutura usando LangChain.
3. `generator.py`: A classe principal que orquestra o salvamento e a interface.
4. `music_service.py` : A classe de serviço que invoca o processamento.

---

## INSTRUÇÃO ADICIONAL: "REGRAS DE OURO"

- **Início:** Deve ser minimalista (menos instrumentos).
- **Meio (Refrão):** Deve ser a seção com mais camadas (layers) e energia.
- **Fim:** Deve conter termos como "fading out", "decay" ou "ending".

---

## INSTRUÇÃO ADICIONAL AVANÇADA

O sistema final deve se comportar como um compositor assistido por IA, sendo capaz de:

- Reutilizar ideias musicais ao longo da faixa
- Manter identidade sonora consistente
- Evoluir temas musicais
- Simular memória musical de curto e médio prazo (via embeddings)

---

**Gere agora o código completo, modular e pronto para produção.**