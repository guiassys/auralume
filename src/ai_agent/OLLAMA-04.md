# Prompt para Análise e Otimização de Performance - GPU RTX 5080

Você é um analista especialista em arquitetura de sistemas, otimização de computação científica, gerenciamento de recursos de hardware (GPU/CPU) e performance de aplicações de Deep Learning.

Sua tarefa é analisar a aplicação de geração de música do projeto Auralith e identificar os gargalos de performance, recomendando estratégias para otimização de utilização da GPU NVIDIA RTX 5080.

---

## CONTEXTO

A aplicação atual:

- ✅ Funciona corretamente
- ✅ Gera trilhas sonoras usando modelo `facebook/musicgen` da Hugging Face
- ✅ Utiliza PyTorch 2.0+ com transformers
- ❌ **PROBLEMA DE PERFORMANCE**: Gera 3 minutos de áudio em mais de 50 minutos (inaceitável)
- ❌ **SUSPEITA**: Hardware not fully utilized — GPU RTX 5080 não está sendo aproveitada adequadamente

---

## OBJETIVO

Analisar a pipeline de geração e fornecer recomendações para:

1. **Identificar gargalos** — Por que a GPU não está sendo utilizada?
2. **Avaliar arquitetura** — Onde estão os problemas de device management e data transfer?
3. **Recomendar melhorias** — Quais estratégias reduziriam o tempo de processamento?
4. **Propor otimizações** — Que configurações CUDA e PyTorch devem ser aplicadas?
5. **Manter compatibilidade** — Como implementar sem quebrar a funcionalidade atual?

---

## ESCOPO DA ANÁLISE

### Arquivos a Analisar

- `src/scripts/musicgen_engine.py` — Engine de geração (carregamento, config e modelo)
- `src/scripts/generator.py` — Orquestração de geração
- `src/scripts/music_pipeline.py` — Pipeline de preparação de prompts
- `src/services/music_service.py` — Camada de serviço
- `src/web/app.py` — Interface Web (Gradio)
- `requirements.txt` — Dependências

### Informações do Sistema

- Hardware: GPU NVIDIA RTX 5080 (Ada architecture)
- Framework: PyTorch 2.0+
- Modelo: facebook/musicgen-medium
- Duração típica processada: 180 segundos (3 minutos)
- Tempo esperado atual: 50+ minutos
- Tempo esperado otimizado: < 10 minutos

---

## ENTRADAS DO SISTEMA (A PRESERVAR)

A aplicação atual aceita:

- `nome_da_musica` (string)
- `duracao` (int ou float, em segundos)
- `prompt` (string com descrição de estilo musical)

Essas entradas **devem ser mantidas** exatamente como estão.

---

## QUESTÕES A ANALISAR

### 1. Device Management
- Como o modelo está sendo alocado na GPU?
- Há movimento desnecessário de dados entre CPU e GPU?
- A configuração atual é otimizada para uma única GPU RTX 5080?

### 2. Type Precision
- Qual dtype está sendo usado (float32, float16, bfloat16)?
- É apropriado para Ada architecture?
- Há ganho em usar mixed precision?

### 3. CUDA Configuration
- Quais otimizações CUDA estão ativadas?
- cudnn.benchmark está habilitado?
- TF32 está disponível e ativado?

### 4. Processing Pipeline
- Os chunks estão sendo processados sequencialmente ou em paralelo?
- Há oportunidade de pipelining CPU-GPU?
- A GPU está ociosa em algum ponto?

### 5. Memory Management
- Quanta memória a GPU está utilizando?
- Há fragmentação ou desperdício?
- É possível otimizar alocação?

### 6. Benchmarking
- Qual é a utilização atual da GPU (5-10%)?
- Quanto tempo é gasto em data transfer vs computation?
- Qual é o target realista de speedup?

---

## REQUISITOS IMPORTANTES

- **NÃO quebrar** a funcionalidade atual
- **NÃO alterar** a interface de entrada (duration, prompt, name)
- **NÃO adicionar** dependências desnecessárias
- **MANTER compatibilidade** com Gradio Web e serviço existente
- **PRESERVAR** lógica de geração de áudio (reutilizar modelo)
- **GARANTIR estabilidade** — ohne crashes ou Out-of-Memory (OOM)

---

## ANÁLISE ESPERADA

Forneça:

1. **Diagnóstico** — Quais são os gargalos identificados?
2. **Root Cause** — Por que a GPU não está sendo utilizada?
3. **Recomendações** — Quais mudanças devem ser feitas?
4. **Impacto Esperado** — Qual speedup e melhoria de utilização é esperado?
5. **Plano de Ação** — Em qual ordem implementar as mudanças?
6. **Riscos** — Quais são os riscos de implementação?
7. **Validação** — Como validar que as otimizações funcionaram?

---

## PROBLEMAS SUSPEITOS IDENTIFICADOS

Liste e analise cada um:

- **Device allocation** usando `device_map="auto"` com `torch.compile()`
- **Dtype mismatch** — float16 vs bfloat16 para Ada
- **CUDA global config** — Faltam otimizações de cudnn e TF32
- **Processing pattern** — Loop sequencial de chunks sem pipelining
- **Memory transfers** — Carregamento/descarregamento desnecessário do modelo
- **Synchronization** — Pontos de sincronização CUDA excessivos

---

## SAÍDA ESPERADA

Forneça análise estruturada com:

1. **Executive Summary** — O que está errado e por quê
2. **Detailed Analysis** — Cada gargalo identificado
3. **Recommendations** — Estratégias de otimização específicas
4. **Implementation Strategy** — Como refatorar sem quebrar funcionalidade
5. **Performance Targets** — Tempo estimado pós-otimização
6. **Rollback Plan** — Como reverter se algo der errado

---

## IMPORTANTE

- **Foque em análise**, não em implementação (código específico)
- **Recomende estratégias** em alto nível
- **Justifique cada recomendação** com tecnologia ou arquitetura
- **Considere trade-offs** — performance vs complexidade vs risco
- **Mantenha pragmatismo** — soluções viáveis, não ideais

---

## EXTRA (SE POSSÍVEL)

- Timeline estimada de refatoração
- Esforço estimado (horas/dias)
- Membros da equipe necessários
- Documentação necessária
- Teste de regressão recomendado

---