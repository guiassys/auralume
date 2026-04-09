# Prompt: Refatoração Auralith - Pipeline de Composição Musical Estruturada

Você é um Engenheiro de Software Sênior especialista em IA Generativa, Áudio Digital e LangChain. 

Sua missão é refatorar o projeto **Auralith** (localizado em `src/scripts/`) para que ele deixe de gerar áudio linear e passe a produzir músicas com estrutura narrativa real (Intro, Verso, Refrão e Outro), utilizando técnicas inspiradas em RAG para manter a coerência temática.

---

## 1. CONTEXTO TÉCNICO
O sistema atual utiliza o modelo `MusicGen` da Meta (Hugging Face) e um wrapper em LangChain. O problema central é que a geração atual é "monolítica" e sofre de amnésia musical, resultando em faixas que não têm progressão ou um final definido.

## 2. OBJETIVO DA REFATORAÇÃO
Implementar um **Hierarchical Music Pipeline** usando LangChain (LCEL) para organizar a geração em estágios lógicos, garantindo:
- **Estrutura de Música Real:** Divisão em seções com intensidades diferentes.
- **Coerência Temática:** O refrão e os versos devem compartilhar o mesmo DNA sonoro.
- **Código Limpo:** Separação clara entre a lógica de "O que compor" (Pipeline) e "Como renderizar" (Engine).

---

## 3. NOVA ARQUITETURA DO PIPELINE (LCEL)

O novo processo deve ser dividido nos seguintes `Runnables`:

### A. Stage 1: Music Architect (O Planejador)
- **Ação:** Recebe o prompt do usuário e a duração total.
- **Saída:** Um mapa de execução (JSON) que divide o tempo total em seções (ex: Intro 10%, Verso 40%, Refrão 35%, Outro 15%).
- **Lógica:** Deve injetar palavras-chave específicas para cada seção (ex: "buildup" na intro, "full energy" no refrão).

### B. Stage 2: Contextual Engine (O Compositor)
- **Ação:** Gerar cada seção sequencialmente.
- **Técnica de Coerência:** Implementar uma lógica onde o "prompt" de uma seção carrega referências da seção anterior para evitar mudanças bruscas de instrumentos.

### C. Stage 3: Audio Engineer (O Pós-Processamento)
- **Ação:** Realizar o crossfade inteligente entre as seções geradas, normalização de volume (Loudness) e aplicação de efeitos básicos (como um Fade-Out no final da seção 'Outro').

---

## 4. REQUISITOS DE IMPLEMENTAÇÃO
- **LangChain:** Usar `RunnableLambda` ou `SequentialChain` para orquestrar as etapas.
- **MusicGen Optimization:** Garantir que o modelo seja carregado na GPU (CUDA) uma única vez (Singleton) para evitar overhead.
- **Modularidade:** Manter o `MusicGenEngine` focado em tensores/inferência e o `MusicPipeline` focado em lógica de negócio/prompts.
- **Estilo de Código:** Pythonic, com Tipagem (Typing), Logging detalhado e tratamento de erros para falhas de memória (VRAM).

---

## 5. SAÍDA ESPERADA

Forneça a implementação completa para os seguintes arquivos:
1. `musicgen_engine.py`: Refatorado para suportar geração modular.
2. `musicgen_pipeline.py`: O coração da lógica de estrutura usando LangChain.
3. `generator.py`: A classe principal que orquestra o salvamento e a interface.

---

## INSTRUÇÃO ADICIONAL: "REGRAS DE OURO"
- **Início:** Deve ser minimalista (menos instrumentos).
- **Meio (Refrão):** Deve ser a seção com mais camadas (layers) e energia.
- **Fim:** Deve conter termos como "fading out", "decay" ou "ending".

**Gere agora o código completo, modular e pronto para produção.**