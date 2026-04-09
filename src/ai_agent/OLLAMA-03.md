# Prompt para Refatoração da Interface Web (Gradio)

Você é um engenheiro de software especialista em Python, IA generativa, pipelines com LangChain e desenvolvimento de interfaces Web com Gradio.

Sua tarefa é refatorar uma aplicação Python já existente e funcional, localizada no diretório: C:\devtools\repo\auralith\src\scripts

Essa aplicação utiliza modelos da Hugging Face e LangChain para gerar músicas. O objetivo é adicionar uma interface Web utilizando Gradio, sem quebrar a funcionalidade atual e mantendo compatibilidade total com o pipeline existente.

---

## CONTEXTO

A aplicação atual:

- Já funciona corretamente
- Recebe inputs do usuário via interface Web

---

## OBJETIVO

Melhorar o layout da aplicação de modo que fique mais profissional e com cara de aplicativo de studio musical.

A interface deve permitir que o usuário:

1. Preencha um formulário
2. Execute a geração de música
3. Acompanhe o progresso (se possível)
4. Faça download do arquivo gerado

⚠️ IMPORTANTE: A lógica de geração de música NÃO deve ser reescrita, apenas reutilizada.


## REQUISITOS FUNCIONAIS

### Layout
- Header com título: **Auralith AI Music Generator**

### Formulário
- Manter o formulário existente com os mesmos componentes.
- Adicionar validações de segurança para evitar que usuários mal intencionados;
- Botão para limpar o formulário para realizar uma nova geração de musica.

### Durante o processamento
 - Exibir informações do prompt que foi utilizado. Ex: [LOFI GEN] Prompt: instrumental; acustic guitar; lofi; Anjo da noite. Style: 40-60 BPM, warm, piano, soft drums, vinyl noise, jazz piano, no abrupt changes. smooth transitions. Duration: 180 seconds.
 - Bloquear o botão "Gerar Música" enquanto o processo estiver em andamento
 - Exibir o progresso do aplicativo como um terminal de log: Ex:
[LOFI GEN] Chunk 1/8
[LOFI GEN] Chunk 2/8
[LOFI GEN] Chunk 3/8
[LOFI GEN] Chunk 4/8
[LOFI GEN] Chunk 5/8
[LOFI GEN] Chunk 6/8
[LOFI GEN] Chunk 7/8
[LOFI GEN] Chunk 8/8

Reutilizar os logs que já estão em uso no script principal para geração da musica

### Pós-processamento
- Exibir status/progresso da geração (ex: loading, etapas do pipeline)
- Botão de download do arquivo gerado (visível apenas após conclusão)
- Exibir caminho ou nome do arquivo gerado

---

## REQUISITOS TÉCNICOS IMPORTANTES

### Arquitetura
- Separar claramente:
- Camada de UI (Gradio)
- Camada de aplicação (orquestração)
- Camada de domínio (pipeline existente)
- NÃO misturar lógica de negócio com interface

### Integração
- Reutilizar o pipeline LangChain existente
- Encapsular a execução em uma função clara (ex: `generate_music_service`)

### Performance
- Evitar recomputações desnecessárias
- Considerar execução assíncrona (async ou thread)
- Evitar travar a interface (non-blocking UI)

### Gerenciamento de arquivos
- Salvar músicas geradas em diretório definido (ex: `/outputs`)
- Garantir nomes únicos de arquivos (evitar sobrescrita)
- Retornar caminho do arquivo corretamente para download

### Estado da aplicação
- Garantir que múltiplos usuários não conflitem (isolamento básico)
- Evitar uso de variáveis globais perigosas

### UX (Experiência do usuário)
- Mostrar feedback durante processamento (loading ou mensagens)
- Desabilitar botão enquanto processa
- Tratar erros com mensagens amigáveis

### Tratamento de erros
- Capturar exceções
- Retornar mensagens claras na UI
- Não expor stacktrace sensível ao usuário

### Logging
- Adicionar logging básico (info, erro)
- Logar início/fim de geração

---

## INSTRUÇÕES DE IMPLEMENTAÇÃO

- Usar Gradio (Blocks ou Interface)
- Criar função principal que conecta UI → pipeline
- Modularizar código (ex: `web/`, `services/`, `pipeline/`)
- Garantir que a aplicação continue podendo ser executada via CLI

---

## SAÍDA ESPERADA

Forneça:

1. Código completo em Python
2. Estrutura de diretórios sugerida
3. Interface Web funcional com Gradio
4. Código comentado explicando decisões
5. Função principal de execução
6. Exemplo de execução local

---

## RESTRIÇÕES IMPORTANTES

- NÃO reescrever o pipeline existente
- NÃO alterar comportamento original
- NÃO introduzir dependências desnecessárias
- NÃO quebrar execução via terminal

---

## EXTRA (DESEJÁVEL)

- Barra de progresso ou status por etapa do pipeline
- Cache simples (se aplicável)
- Sugestão de deploy (ex: local ou Hugging Face Spaces)
- Estrutura pronta para futura API REST

---

## RESULTADO FINAL

O resultado deve ser uma aplicação Web funcional, modular e pronta para uso, mantendo compatibilidade total com o sistema atual e melhorando significativamente a experiência do usuário.

**Gere o código completo e funcional.**