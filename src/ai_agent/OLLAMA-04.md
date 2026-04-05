# Prompt para melhoria do pipeline de geração musical

Você é um engenheiro de software especialista em Python, IA generativa, modelagem de prompts e pipelines com LangChain.

Sua tarefa é melhorar o sistema de geração musical do projeto Auralith para permitir que o usuário gere músicas com mais qualidade harmônica. O foco é fortalecer o mecanismo de prompts e o comportamento padrão da interface, sem comprometer a funcionalidade já existente.

---

## CONTEXTO

O projeto atual:

- já funciona e gera áudio via `facebook/musicgen-*`
- usa `src/scripts/generator.py`, `src/scripts/music_pipeline.py` e `src/scripts/prompts.py`
- possui interface Web em `src/web/app.py`
- depende de entradas do usuário: `nome_da_musica`, `duracao`, `prompt`

---

## OBJETIVO

Aprimorar o código para que:

1. o prompt gerado contenha instruções harmônicas claras
2. o sistema produza prompts mais musicais, detalhados e consistentes
3. a UI oriente o usuário a fornecer prompts com qualidade
4. o comportamento principal não seja quebrado

---

## ARQUIVOS IMPORTANTES

- `src/scripts/prompts.py`
- `src/scripts/music_pipeline.py`
- `src/scripts/generator.py`
- `src/web/app.py`

---

## ENTRADAS DO SISTEMA

Devem ser preservadas exatamente:

- `nome_da_musica` (string)
- `duracao` (int ou float)
- `prompt` (string)

---

## REQUISITOS

1. Melhore os prompts padrões e templates em `src/scripts/prompts.py`
   - inclua progressões de acordes explícitas (ex.: `Cmaj7 - Am7 - Dm7 - G7`, `ii-V-I`)
   - inclua tonalidade/escala (ex.: `em Dm`, `modo dórico`, `escala pentatônica`)
   - inclua harmonia rica (`acordes com sétima e nona`, `voicings jazz`)
   - inclua arranjo musical (ex.: `piano Rhodes`, `baixo elétrico melódico`, `pads analógicos`)
   - inclua atmosfera e textura (ex.: `chuva leve`, `textura de fita`, `ambiente aconchegante`)

2. Atualize `src/scripts/music_pipeline.py`
   - adicione uma etapa explícita de harmonia ou progressão de acordes
   - faça `final_prompt` conter instruções claras sobre centro tonal, coerência harmônica e estrutura musical
   - mantenha a separação entre `prompt`, `style` e `harmonia` sempre que fizer sentido

3. Atualize `src/web/app.py`
   - torne o prompt inicial mais orientado para qualidade musical
   - forneça um exemplo de prompt rico para guiar o usuário
   - mantenha a interface simples e compatível

4. Não reescreva a lógica de geração de áudio, apenas melhore a camada de prompt e guia ao usuário.

---

## EXEMPLO DE PROMPT FINAL DESEJADO

“Lo-fi hip hop suave com piano Rhodes, pad analógico e baixo elétrico melódico. Progressão de acordes Cmaj7 - Am7 - Dm7 - G7, melodia em modo dórico, groove relaxado, harmonia rica e ambiente de chuva leve. Mixagem suave com textura de fita vintage.”

---

## EXIGÊNCIAS FINAIS

- NÃO quebre o funcionamento atual do app
- NÃO altere a interface principal além de melhorar o prompt padrão
- NÃO introduza dependências novas desnecessárias