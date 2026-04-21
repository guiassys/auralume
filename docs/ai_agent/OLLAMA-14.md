> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Otimização da Experiência do Usuário e Identidade Visual da Plataforma

## 🌍 Contexto

- **Aplicação Alvo**: Plataforma de geração de música Auratune.
- **Problema de Negócio**: A interface atual da plataforma carece de uma identidade visual profissional e apresenta uma usabilidade confusa. Elementos cruciais estão mal posicionados, o feedback de progresso é intrusivo e a aparência genérica não inspira confiança ou criatividade, o que pode afastar usuários que esperam uma experiência similar à de um software de produção musical (DAW).
- **Necessidade Estratégica**: Para posicionar a Auratune como uma ferramenta séria e intuitiva no mercado, é essencial refinar a experiência do usuário (UX) e implementar uma identidade visual (UI) coesa e profissional, que remeta ao universo da produção musical.

## 🎯 Objetivo Principal

Transformar a interface da Auratune em uma experiência de usuário mais profissional, intuitiva e esteticamente alinhada a um software de áudio, com foco em três pilares:

1.  **Implementar uma Identidade Visual Profissional**:
    - **Diretriz**: A interface deve abandonar o tema padrão e adotar uma paleta de cores escura (dark theme), inspirada em DAWs populares. O design deve ser limpo, com bom contraste e uma aparência que transmita profissionalismo e foco na criatividade.
    - **Impacto Esperado**: Aumentar a percepção de valor da ferramenta e criar um ambiente mais imersivo para o usuário.

2.  **Otimizar o Fluxo de Geração de Música**:
    - **Feedback de Progresso**: O indicador de progresso da geração deve ser sutil e informativo, mostrando um ícone de atividade e a porcentagem, sem poluir a tela. Ele deve estar logicamente associado aos controles que iniciam a tarefa.
    - **Organização Lógica**: A área de download dos arquivos gerados deve aparecer somente após a conclusão do processo e estar localizada em uma área de "finalização", como o menu lateral de ações, abaixo do botão "Gerar".
    - **Clareza na Ação**: Ao iniciar uma nova geração, a interface deve ser limpa automaticamente, removendo os resultados da geração anterior para evitar qualquer ambiguidade.

3.  **Garantir a Estabilidade da Aplicação**:
    - **Correção de Erros**: A aplicação deve iniciar de forma estável, sem erros ou alertas de compatibilidade relacionados à biblioteca de interface.

---

## 🎯 Definição de Concluído

- A aplicação apresenta uma nova identidade visual com um tema escuro, profissional e coeso, inspirado em softwares de produção musical.
- O indicador de progresso é discreto, exibe um ícone e a porcentagem, e está localizado de forma visível mas não intrusiva na área de controle da geração.
- A seção de download de arquivos só se torna visível após a conclusão da geração e está posicionada logicamente no menu de ações.
- Iniciar uma nova geração limpa automaticamente os resultados da geração anterior.
- A aplicação inicia e opera de forma estável, sem erros de interface.
- Todas as diretrizes de alto nível definidas em `@/docs/ai_agent/OLLAMA.md` foram respeitadas.
