> Este prompt herda todas as diretrizes e restrições do template principal: `@/docs/ai_agent/OLLAMA.md`.

# 🚀 Adição de Seleção de Formato de Áudio e Geração de MIDI

## 🌍 Contexto

- **Aplicação Alvo**: O sistema de geração de música existente, que atualmente produz apenas arquivos no formato `.wav`.
- **Necessidade**: Oferecer aos usuários mais flexibilidade no formato de saída, permitindo a escolha entre `.wav` e `.mp3`, e opcionalmente gerar um arquivo `.mid` para edição posterior em uma Digital Audio Workstation (DAW).
- **Requisito**: A integração deve ser incremental, sem interromper o fluxo de trabalho atual.

## 🎯 Objetivo Principal

Estender o sistema de geração de música para permitir que os usuários selecionem o formato de áudio de saída e optem pela geração de um arquivo MIDI. As novas funcionalidades devem ser integradas à interface do usuário e implementadas no backend, mantendo o comportamento padrão do sistema inalterado se nenhuma nova opção for selecionada.

---

## 🚀 Plano de Implementação

1.  **Alterações na Interface (Frontend)**:
    - Adicionar um grupo de botões de rádio ou um dropdown para a seleção do formato de áudio.
        - **Opções**: `.wav`, `.mp3`.
        - **Padrão**: `.wav`.
    - Adicionar uma caixa de seleção (checkbox) para a geração de arquivo MIDI.
        - **Rótulo**: "Gerar arquivo MIDI".
        - **Padrão**: Desmarcado (Não).

2.  **Adaptação da Camada de Serviço (Backend)**:
    - Modificar a camada de serviço para aceitar os novos parâmetros da interface (ex: `audio_format`, `generate_midi`).
    - **Lógica de Formato de Áudio**:
        - Se `audio_format` for `.mp3`, o sistema deve primeiro gerar o arquivo `.wav` como de costume e, em seguida, convertê-lo para `.mp3` usando uma biblioteca como `pydub`. O arquivo final disponibilizado para download será o `.mp3`.
    - **Lógica de Geração de MIDI**:
        - Se `generate_midi` for `true`, o sistema deve invocar um novo módulo responsável por analisar a melodia ou os acordes da música gerada e criar um arquivo `.mid` correspondente. Este arquivo deve ser salvo junto com o arquivo de áudio.

👉 **Mandato de Execução**: Conforme o template principal, sua primeira resposta deve ser a **Proposta de Arquitetura**, detalhando como os novos parâmetros serão passados do frontend para o backend e como a lógica de conversão para `.mp3` e a geração de MIDI serão implementadas e integradas ao serviço existente. Aguarde a confirmação antes de gerar o código.

---

## 🎯 Definição de Concluído

- O usuário pode selecionar o formato de áudio (`.wav` ou `.mp3`) na interface.
- O usuário pode optar por gerar um arquivo MIDI através de uma caixa de seleção.
- O sistema gera corretamente os arquivos nos formatos selecionados.
- Se nenhuma opção for alterada, o comportamento padrão (gerar apenas `.wav`) é mantido.
- As novas funcionalidades estão integradas e funcionais, sem quebrar o processo existente.
