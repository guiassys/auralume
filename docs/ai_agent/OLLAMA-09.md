> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Geração de Animação de Respiração a Partir de Imagem Única

## 🌍 Contexto

- **Aplicação Alvo**: Um pipeline de geração de vídeo baseado em difusão, utilizando AnimateDiff para movimento e IP-Adapter para condicionamento de imagem.
- **Entrada**: Uma única imagem de alta qualidade de um anjo em estilo anime sentado em uma borda, com uma cidade noturna ao fundo.
- **Necessidade**: Gerar uma animação curta e de alta fidelidade que simule um movimento sutil de respiração no personagem, preservando completamente a identidade visual, a composição e o estilo da imagem original.

## 🎯 Objetivo Principal

Produzir uma animação de alta qualidade que simule um ciclo de respiração natural e sutil. O movimento deve ser fisicamente plausível, temporalmente suave e manter fidelidade absoluta à imagem de origem, sem introduzir artefatos, deformações ou movimentos de câmera.

---

## 🚀 Plano de Implementação

1.  **Configuração do Pipeline de Animação**:
    - Carregar o checkpoint base do Stable Diffusion 1.5.
    - Integrar o AnimateDiff para gerar a dinâmica temporal (movimento).
    - Integrar o IP-Adapter para garantir que a imagem de entrada condicione fortemente cada frame gerado, preservando a identidade visual.

2.  **Engenharia de Prompt para Movimento Sutil**:
    - Criar um prompt de texto que descreva o movimento de respiração de forma semântica e natural. Ex: *"subtle breathing, chest and shoulders rising and falling gently, slow and calm rhythm"*.
    - Definir um prompt negativo para proibir movimentos indesejados. Ex: *"camera movement, zoom, pan, shaking, large motion, flickering, distortion"*.

3.  **Controle de Intensidade e Foco do Movimento**:
    - Ajustar a intensidade do AnimateDiff (`motion_scale`) para um valor baixo, garantindo que o movimento seja sutil e não cause deformação.
    - O foco principal do movimento deve ser no peito e ombros. Movimentos secundários e sincronizados podem ser aplicados às asas e à postura da cabeça, mas com amplitude ainda menor.

4.  **Geração e Pós-processamento**:
    - Executar o pipeline para gerar a sequência de frames.
    - Validar a consistência temporal e a ausência de "flickering" ou mudanças de identidade entre os frames.
    - Exportar a sequência de frames como um arquivo de vídeo de alta qualidade (ex: MP4).

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando como o pipeline do `diffusers` será configurado, combinando AnimateDiff e IP-Adapter, e qual será a estratégia de prompt para alcançar o movimento de respiração sutil. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- A animação final exibe um ciclo de respiração natural, contínuo e sutil.
- A identidade do personagem, a pose e o estilo da imagem original são perfeitamente preservados em todos os frames.
- Não há distorção, "flickering" ou qualquer tipo de movimento de câmera.
- O resultado é um arquivo de vídeo de alta qualidade, esteticamente agradável e pronto para uso.
