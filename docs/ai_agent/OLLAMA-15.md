> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Implementação de Upload de Áudio de Referência (Audio-to-Audio)

## 🌍 Contexto

- **Aplicação Alvo**: Plataforma de geração de música Auralume.
- **Problema de Negócio**: Atualmente, a geração de músicas é baseada apenas em texto (prompts) e parâmetros pré-definidos. Os usuários podem querer usar melodias, batidas ou trechos sonoros como base de inspiração (referência) para a inteligência artificial gerar a música. Além disso, identificou-se que durante a geração de áudio (especialmente de arquivos longos ou com referência), a interface de usuário deixa de atualizar a barra de progresso após um determinado ponto (ex: travando em 95% e omitindo os logs subjacentes do motor de inferência), passando uma falsa sensação de travamento.
- **Necessidade Estratégica**: Expandir as capacidades criativas da plataforma Auralume, permitindo ao usuário fazer o upload de um arquivo de áudio para ser utilizado como referência, promovendo maior controle e precisão no resultado gerado. A implementação deve focar em estabilidade, uso eficiente do hardware de GPU e feedback visual contínuo e responsivo na interface.

## 🎯 Objetivo Principal

Criar um recurso opcional que permita o envio de um arquivo de música como referência durante o processo de criação, melhorando simultaneamente o monitoramento de logs e a atualização da barra de progresso na interface para que os usuários acompanhem ativamente todas as etapas do motor de inferência.

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
    
4.  **Feedback Visual e Monitoramento (Logs & Progresso)**:
    - Integrar um mecanismo de callback (*streamer* ou inspetor de geração) no motor de inferência que reporte ativamente as etapas em andamento (por exemplo, contagem de tokens gerados ou percentual da geração do *chunk* de áudio).
    - Otimizar a comunicação entre os logs do backend e a interface (`app.py`), garantindo que o progresso não fique "preso" e atualize de forma fluida, refletindo as etapas reais de inferência do áudio, desde o "step 1/1" até a conclusão do trim e conversão do arquivo final.

---

## 🎯 Definição de Concluído

- Novo componente de áudio posicionado ao lado do "Style Prompt".
- As pipelines de processamento (Simples e Avançada) utilizam o áudio enviado como ponto de partida (Audio-to-Audio).
- Operações na GPU rodam com estabilidade e sem erros, mesmo com configurações de quantização ativadas.
- O componente de progresso na interface de usuário atualiza continuamente e os logs acompanham ativamente as etapas de predição/renderização da engine, erradicando congelamentos visuais.
- O documento respeita a linguagem clara e concisa descrita em `@/docs/ai_agent/OLLAMA.md`.
