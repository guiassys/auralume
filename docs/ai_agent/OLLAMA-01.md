> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Refatoração de Script para Pipeline de Geração de Música

## 🌍 Contexto

- **Arquivo Alvo**: O script Python funcional, porém lento e monolítico, localizado em `src/scripts/generate_lofi_ai.py`.
- **Funcionalidade Atual**: O script gera música usando modelos da Hugging Face a partir de inputs do usuário (`nome_da_musica`, `duracao`, `prompt`).
- **Problema**: A execução é lenta e a estrutura do código dificulta a manutenção e reutilização.

## 🎯 Objetivo Principal

Refatorar o script `generate_lofi_ai.py` para um pipeline modular e performático utilizando LangChain, sem alterar a funcionalidade principal. O foco é melhorar a organização, performance e reutilização das etapas.

---

## 🚀 Plano de Implementação

A arquitetura do novo pipeline deve ser dividida em quatro etapas sequenciais, implementadas como `Chains` independentes no LangChain:

1.  **Geração de Melodia**: Cria a estrutura melódica base da música.
2.  **Criação da Base Rítmica**: Define o ritmo, as batidas e o BPM.
3.  **Adição da Faixa Instrumental**: Combina melodia, ritmo e o estilo musical definido no `prompt`.
4.  **Mixagem e Masterização**: Realiza o ajuste final e o refinamento da faixa de áudio.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura** detalhando como você pretende estruturar este pipeline com LangChain. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- O pipeline em LangChain está implementado e substitui a lógica do script monolítico.
- A funcionalidade de geração de música continua operando com os mesmos inputs e produzindo um resultado equivalente.
- O novo código está modular, com cada etapa do pipeline claramente definida.
- Um exemplo de como executar o novo pipeline é fornecido.
- Logging básico foi adicionado para monitorar a execução de cada etapa.
