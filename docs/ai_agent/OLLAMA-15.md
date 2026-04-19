> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Implementação de Upload de Áudio de Referência (Audio-to-Audio)

## 🌍 Contexto

- **Aplicação Alvo**: Plataforma de geração de música Auralume.
- **Problema de Negócio**: Atualmente, a geração de músicas é baseada apenas em texto (prompts) e parâmetros pré-definidos. Os usuários podem querer usar melodias, batidas ou trechos sonoros como base de inspiração (referência) para a inteligência artificial gerar a música.
- **Necessidade Estratégica**: Expandir as capacidades criativas da plataforma Auralume, permitindo ao usuário fazer o upload de um arquivo de áudio para ser utilizado como referência, promovendo maior controle e precisão no resultado gerado. A implementação deve focar em estabilidade e no uso eficiente do hardware de GPU.

## 🎯 Objetivo Principal

Criar um recurso opcional que permita o envio de um arquivo de música como referência durante o processo de criação. Esse novo elemento deve ser perfeitamente integrado à interface existente e fluir de maneira estável pelas pipelines de processamento (Simples e Avançada).

## 🚀 Plano de Implementação

1.  **Novo Campo de Upload de Áudio**:
    - Adicionar um componente de upload de arquivos restrito aos formatos `.wav` e `.mp3`.
    - Inserir o campo ao lado de "Style Prompt" na interface do usuário.
    - O campo **não deve ser obrigatório**.
    
2.  **Ajuste nas Pipelines**:
    - Modificar o fluxo de geração para processar o áudio de referência, se fornecido.
    - Integrar o áudio de referência com os demais parâmetros vigentes (prompts de estilo, tema, etc).
    
3.  **Alinhamento de GPU e Estabilidade**:
    - Assegurar a compatibilidade das matrizes flutuantes em execuções de precisão mista/quantizadas.
    - Preservar o gerenciamento seguro do hardware sem modificar pesos de forma insegura.

---

## 🎯 Definição de Concluído

- Novo componente de áudio posicionado ao lado do "Style Prompt".
- As pipelines de processamento (Simples e Avançada) utilizam o áudio enviado como ponto de partida (Audio-to-Audio).
- Operações na GPU rodam com estabilidade e sem erros, mesmo com configurações de quantização ativadas.
- O documento respeita a linguagem clara e concisa descrita em `@/docs/ai_agent/OLLAMA.md`.
