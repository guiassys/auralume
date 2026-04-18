# Prompt para Refatoração em Pipeline com LangChain

Você é um engenheiro de software especialista em Python, IA generativa e pipelines com LangChain.

Sua tarefa é refatorar um script Python já existente e funcional, localizado no diretório: C:\devtools\repo\auralume\src\scripts

Essa aplicação utiliza modelos da Hugging Face para gerar músicas. O objetivo é melhorar o desempenho e organizar o processo em um pipeline estruturado, sem quebrar a funcionalidade atual.

---

## CONTEXTO

O código atual:

- Já funciona corretamente  
- Gera música a partir do comando: python -m src.scripts.generate_lofi_ai e inputs do usuário  
- Está lento e monolítico (processo único)

---

## OBJETIVO

Transformar o processo em um pipeline modular utilizando LangChain, mantendo compatibilidade com o comportamento atual, mas melhorando:

- Performance  
- Organização  
- Reutilização de etapas  

---

## ENTRADAS DO SISTEMA

O pipeline deve continuar aceitando exatamente os seguintes inputs:

- `nome_da_musica` (string)  
- `duracao` (int ou float)  
- `prompt` (string com estilo musical, ex: "hip hop", "lo-fi", "rock")  

---

## REQUISITOS IMPORTANTES

- NÃO quebrar o funcionamento atual  
- Manter compatibilidade com o modelo Hugging Face já utilizado  
- Evitar mudanças desnecessárias na lógica existente  
- Melhorar performance (ex: paralelismo, execução assíncrona ou otimização de chamadas)  
- Código limpo, modular e bem organizado  

---

## NOVA ARQUITETURA (PIPELINE)

O processo deve ser dividido nas seguintes etapas:

### 1. Melodia musical
Responsável por gerar a estrutura melódica base  

### 2. Base rítmica
Define ritmo, batidas e BPM  

### 3. Faixa instrumental
Combina melodia + ritmo + estilo  

### 4. Mixagem
Ajuste final e refinamento da música  

---

## INSTRUÇÕES DE IMPLEMENTAÇÃO

- Usar LangChain (Chains ou SequentialChain)  
- Cada etapa deve ser uma função ou chain independente  
- Permitir fácil extensão futura  
- Se possível, aplicar paralelismo onde fizer sentido  
- Evitar recomputações desnecessárias  
- Reaproveitar resultados intermediários  

---

## SAÍDA ESPERADA

Forneça:

1. Código completo em Python  
2. Estrutura modular clara  
3. Pipeline usando LangChain  
4. Comentários explicando cada etapa  
5. Sugestões opcionais de otimização (ex: caching, async, batch)  

---

## IMPORTANTE

- NÃO reescreva tudo do zero se não for necessário  
- Preserve a lógica existente sempre que possível  
- Foque em refatoração e organização em pipeline  

---

## EXTRA (SE POSSÍVEL)

- Adicionar logging básico  
- Mostrar como executar o pipeline com um exemplo  

---

## RESULTADO FINAL

O código deve ser completo, funcional e pronto para uso, mantendo compatibilidade com o sistema atual e melhorando desempenho e organização.

**Gere o código completo e funcional.**
