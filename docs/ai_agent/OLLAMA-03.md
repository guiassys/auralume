> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Melhoria da Interface Web com Gradio

## 🌍 Contexto

- **Aplicação Alvo**: A interface web existente construída com Gradio.
- **Necessidade**: Aprimorar a experiência do usuário (UX) com um layout mais profissional, feedback de progresso detalhado e melhorias de usabilidade.
- **Funcionalidade Atual**: A interface já permite a geração de músicas, mas a experiência do usuário é básica.

## 🎯 Objetivo Principal

Refatorar a interface Gradio para incorporar um layout com tema de estúdio musical, exibir o progresso da geração de música em tempo real como um log de terminal e adicionar funcionalidades de usabilidade, como um botão para limpar o formulário.

---

## 🚀 Plano de Implementação

1.  **Melhoria do Layout e Estilo**:
    - Atualizar o título principal para **"Auralume AI Music Generator"**.
    - Aplicar um tema escuro (`theme='dark'`) ao `gr.Blocks` para uma aparência de estúdio.
    - Organizar os componentes de entrada e saída em `gr.Row` e `gr.Column` para uma melhor estrutura visual.

2.  **Feedback de Progresso em Tempo Real**:
    - Adicionar um componente `gr.Textbox` configurado como um terminal de log (ex: `label="Log de Geração"`).
    - Modificar a camada de serviço para que ela utilize `yield` para transmitir os logs de progresso (ex: `[AURALITH GEN] Chunk 1/8`) do pipeline para a interface.
    - A interface do Gradio irá capturar esses logs e anexá-los ao terminal de log em tempo real.

3.  **Aprimoramentos de Usabilidade**:
    - Implementar um botão "Limpar" que reseta os campos do formulário para seus valores padrão.
    - Garantir que o botão "Gerar Música" seja desabilitado durante o processamento para evitar múltiplas submissões.
    - Exibir o prompt completo utilizado para a geração no início do log para que o usuário tenha um registro claro do que foi solicitado.

4.  **Validação de Segurança**:
    - Implementar validações básicas nos campos de entrada para evitar inputs maliciosos, conforme as diretrizes de segurança do prompt principal.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando como a função de serviço será modificada para usar `yield` e como a interface Gradio será reestruturada para exibir os logs e o novo layout. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- A interface Gradio possui um layout escuro e profissional.
- O progresso da geração é exibido em tempo real em um componente de log.
- O botão "Gerar Música" é desabilitado durante o processamento.
- Um botão "Limpar" foi adicionado e está funcional.
- O prompt utilizado é exibido no log de geração.
- Validações de segurança básicas foram implementadas.
