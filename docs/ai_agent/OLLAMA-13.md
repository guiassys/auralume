> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Evolução da Plataforma para Suportar Múltiplos Modos de Geração Musical

## 🌍 Contexto

- **Aplicação Alvo**: Plataforma de geração de música Auralume.
- **Problema de Negócio**: A plataforma atual oferece um único modo de geração "Avançado", que, embora poderoso, é complexo para usuários iniciantes. Além disso, não há flexibilidade para o usuário escolher a performance do modelo de IA, impactando a experiência de uso.
- **Necessidade Estratégica**: Para ampliar a base de usuários e melhorar a experiência, precisamos introduzir um modo de geração "Simples" e permitir que os usuários selecionem o modelo de IA que melhor se adapta às suas necessidades de velocidade e qualidade.

## 🎯 Objetivo Principal

Evoluir a plataforma Auralume para se tornar um sistema modular de geração musical, implementando duas novas features de alto valor para o usuário:

1.  **Modo de Geração "Simples"**: Oferecer uma experiência de "um clique" onde o usuário insere apenas uma ideia (prompt) e recebe uma música curta e de alta qualidade, ideal para loops e experimentação rápida.
2.  **Seleção de Performance do Modelo**: Permitir que o usuário escolha o "tamanho" do modelo de IA (ex: "Pequeno", "Médio", "Grande"), balanceando entre velocidade de geração e complexidade musical.

---

## 💡 Diretriz Arquitetural: Pipelines como Plugins

A implementação desta e de futuras funcionalidades de geração deve seguir um modelo de **arquitetura de pipelines modulares**.

- **Visão**: Cada "modo de geração" (como "Simples" e "Avançado") deve ser tratado como um **plugin independente e autônomo**.
- **Isolamento**: Cada pipeline é uma feature completa e isolada. Ele define seus próprios parâmetros, seu próprio fluxo de geração e não deve ter conhecimento ou dependência de outros pipelines.
- **Orquestração Central**: O sistema principal (`MusicGenerationService`) atuará como um **orquestrador**. Sua única responsabilidade é identificar qual pipeline o usuário selecionou e rotear a solicitação para o plugin correto.
- **Configuração Centralizada**: Todos os parâmetros configuráveis para **todos** os pipelines devem ser definidos no arquivo `/config.json`, permitindo fácil ajuste e manutenção a partir de uma única tela de "Settings".

Esta abordagem garante que a plataforma seja **escalável**, permitindo que novos modos de geração (ex: "Geração por Acordes", "Remix de Áudio") sejam adicionados no futuro como novos plugins, sem impactar as funcionalidades existentes.

---

## 🚀 Plano de Implementação

### Fase 1: Implementação do Pipeline "Simples" como um Plugin

1.  **Interface do Usuário (UI)**:
    - No topo da tela, adicionar um seletor de "Modo de Geração" com as opções: `["Simples", "Avançado"]`.
    - O modo "Simples" deve ser o **padrão**.
    - Ao selecionar "Simples", a interface deve ser minimalista, exibindo apenas os controles essenciais: o campo de prompt e o seletor de tamanho do modelo. Todos os outros controles avançados devem ser ocultados.
    - Ao selecionar "Avançado", a interface deve reexibir todos os controles, restaurando a experiência completa.

2.  **Backend (Orquestração e Plugin)**:
    - O Orquestrador (`MusicGenerationService`) receberá a escolha do usuário e ativará o pipeline correspondente.
    - Criar o novo plugin `SimpleMusicPipeline`, que será responsável por:
        - Receber o prompt do usuário.
        - Gerar uma única faixa de música de 30 segundos, otimizada para ser usada como um loop contínuo (sem fade-out).
        - Utilizar o modelo de IA e a configuração de performance (quantização) selecionados pelo usuário para garantir a melhor experiência em seu hardware.

### Fase 2: Implementação da Seleção de Performance do Modelo

1.  **Interface do Usuário (UI)**:
    - Na área principal (visível em ambos os modos), adicionar um seletor de "Tamanho do Modelo".
    - As opções (`["small", "medium", "large"]`) e o valor padrão devem ser carregados do `/config.json`.

2.  **Backend (Motor de IA)**:
    - O motor de IA (`MusicGenEngine`) deve ser capaz de carregar e descarregar modelos dinamicamente com base na seleção do usuário, incluindo o tamanho e a configuração de performance (quantização), para otimizar o uso de hardware (CPU/GPU).

---

## 🎯 Definição de Concluído

- A aplicação inicia no modo "Simples" por padrão, com uma interface limpa.
- O usuário pode alternar para o modo "Avançado", que restaura todas as funcionalidades anteriores sem regressão.
- O modo "Simples" gera uma música de 30 segundos, com alta qualidade, que respeita a intenção do prompt do usuário e pode ser usada em loop.
- A geração no modo "Simples" é visivelmente rápida, utilizando o hardware do usuário (GPU) de forma eficiente.
- O usuário pode selecionar o tamanho do modelo em ambos os modos, e a escolha é respeitada pelo backend, impactando a velocidade e a qualidade da geração.
- A arquitetura de pipelines está implementada, com o `SimpleMusicPipeline` e o `MusicPipeline` (avançado) funcionando como módulos independentes orquestrados pelo `MusicGenerationService`.
