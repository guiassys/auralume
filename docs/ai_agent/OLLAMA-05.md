# Prompt: Evolução Auralume - Base de Conhecimento por Referência de Áudio

Você é um Engenheiro de Software Sênior especialista em IA Generativa, Áudio Digital e LangChain.

Sua missão é evoluir o projeto **Auralume** para incorporar uma **Base de Conhecimento de Áudio (Audio-RAG)**, permitindo que o sistema utilize arquivos de referência sonora fornecidos pelo usuário para guiar a identidade musical das composições geradas.

---

## 1. CONTEXTO TÉCNICO

O sistema atual utiliza o modelo `MusicGen` da Meta (via Hugging Face), com uma arquitetura modular baseada em:

- Interface Web com Gradio
- Service Layer (`MusicGenerationService`)
- Orquestrador (`LofiGenerator`)
- Pipeline com LangChain (LCEL)
- Engine de geração (`MusicGenEngine`)

### Problemas atuais:

- **Amnésia musical**: falta de continuidade entre seções
- **Falta de coerência estilística** ao longo da música
- **RAG fictício** baseado em embeddings aleatórios
- **Ausência de referência sonora real** para guiar a geração

---

## 2. OBJETIVO DA REFATORAÇÃO

Evoluir o sistema para suportar **Audio-RAG real**, permitindo que uma música de referência influencie diretamente a geração.

### Objetivos principais:

- 🎼 **Estrutura musical realista**
- 🎧 **Coerência estilística baseada em referência**
- 🧠 **Memória musical contextual**
- 🧩 **Separação clara de responsabilidades**
- ⚙️ **Preservação do que já funciona**

---

## 3. NOVA FEATURE (CRÍTICA)

### Upload de arquivo `.wav` na interface

A interface deve permitir que o usuário faça upload de um arquivo de áudio (`.wav`) que será utilizado como **fonte de conhecimento musical**.

### Requisitos dessa feature:

- O upload deve ser **opcional**
- Não deve quebrar o fluxo atual (fallback para modo sem referência)
- O arquivo deve ser propagado por toda a arquitetura:
  - `app.py` → `music_service.py` → `generator.py` → `pipeline`
- O sistema deve utilizar esse áudio para:
  - Extração de características (embedding, energia, etc.)
  - Alimentar o sistema de RAG real
  - Influenciar os prompts de geração

---

## 4. DIRETRIZ CRÍTICA

> ⚠️ **NÃO QUEBRAR O QUE JÁ FUNCIONA**

- O sistema atual já gera música corretamente
- O crossfade e chunking estão estáveis
- O controle de GPU via lock está correto

### Portanto:

- A nova feature deve ser **incremental**
- Código existente deve ser **preservado ao máximo**
- Alterações devem ser **mínimas e seguras**

---

## 5. NOVA ARQUITETURA DO PIPELINE (LCEL)

### Stage 1: Music Architect (Planejamento)

**Entrada:**
- Prompt textual
- Duração
- Estilo
- Caminho do áudio de referência (opcional)

**Responsabilidades:**
- Definir estrutura da música (intro, verso, etc.)
- Determinar como a referência será usada
- Preparar contexto inicial

---

### Stage 2: Contextual Engine (Composição com RAG)

**Responsabilidades:**

Substituir:

```python
embedding = np.random.rand(128)
```

Por:

- Extração real de embeddings do áudio (ex: CLAP, torchaudio, etc.)
- Indexação no vector store
- Recuperação contextual baseada na referência

**Objetivo:**
- Garantir consistência de:
  - Timbre
  - Instrumentação
  - Energia
  - Atmosfera

---

### Stage 3: Audio Engineer (Pós-processamento)

**Manter intacto:**
- Crossfade
- Merge de seções
- Normalização

---

## 6. IMPLEMENTAÇÃO DO AUDIO-RAG

### Requisitos técnicos:

- Criar pipeline de extração leve (não competir com VRAM do MusicGen)
- Converter áudio em representação vetorial
- Indexar no `SimpleVectorStore` (ou evolução dele)

### Comportamento esperado:

- Intro, verso e refrão compartilham identidade
- Evitar mudanças bruscas de estilo
- Reutilizar contexto ao longo da geração

---

## 7. INTEGRAÇÃO COM A INTERFACE (GRADIO)

### Adicionar:

```python
gr.File(file_types=[".wav"])
```

### Requisitos:

- O arquivo deve ser acessível no backend
- O estado deve ser mantido durante execução
- Deve aparecer no pipeline como `reference_audio_path`

---

## 8. SERVICE LAYER

### `MusicGenerationService`

Deve:

- Receber o caminho do áudio
- Incluir no `config`
- Garantir compatibilidade com chamadas antigas

---

## 9. GENERATOR (ORQUESTRADOR)

### `LofiGenerator`

Deve:

- Receber o áudio de referência
- Passar para o pipeline
- Garantir fallback seguro se não houver referência

---

## 10. QUALIDADE DE CÓDIGO

### Obrigatório:

- Tipagem completa (`typing`)
- Logging detalhado (em inglês)
- Código modular e limpo

### Proibido:

- Remover logs existentes no console web (user interface)
- Quebrar compatibilidade
- Introduzir dependências pesadas sem justificativa

---

## 11. MONITORAMENTO

A UI já possui um console de logs.

### Deve ser expandido para mostrar:

- Prompt enviado para o modelo de IA
- Etapas de análise do áudio
- Extração de embeddings
- Uso do RAG
- Decisões do pipeline
- Total de tempo consumido do incio ao fim do processo. Ex: total processing time: 00:01:48

---

## 12. SAÍDA ESPERADA

Forneça a implementação completa e integrada dos seguintes arquivos:

1. `app.py`
   - Adicionar upload `.wav`
   - Integrar ao fluxo existente

2. `music_service.py`
   - Transportar referência de áudio

3. `musicgen_pipeline.py`
   - Substituir RAG fake por real

4. `musicgen_engine.py`
   - Manter estável (mínimas mudanças)

5. `generator.py`
   - Integrar referência ao pipeline

   Fornece o codigo completo de novos scripts caso seja necessário cria-los.

---

## 13. RESUMO FINAL

Você deve:

- ✅ Adicionar suporte a áudio de referência (.wav)
- ✅ Implementar Audio-RAG real
- ✅ Melhorar coerência musical
- ✅ Manter estabilidade do sistema atual
- ❌ NÃO quebrar funcionalidades existentes

---

## 14. RESULTADO ESPERADO

O sistema deve evoluir de:

> "Gerador baseado em prompt"

Para:

> "Sistema inteligente guiado por referência sonora + prompt"

---

**Gere agora o código completo, modular e pronto para produção, seguindo rigorosamente essas diretrizes.**