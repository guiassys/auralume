# 🎧 Auralith

Auralith é um sistema de criação de conteúdo digital no estilo lo-fi, inspirado por experiências imersivas como as da Lofi Girl.

A plataforma permite a geração automatizada de músicas lo-fi combinadas com identidade visual, narrativa e personagens próprios.

---

# 🌙 Aelion

Aelion é o primeiro personagem criado dentro do universo Auralith.

Ele é um anjo solitário e contemplativo, frequentemente representado em cenários silenciosos e elevados, observando o mundo enquanto suas emoções são traduzidas em música.

Aelion funciona como uma âncora emocional do projeto, conectando o público à experiência sonora e visual.

---

# 🎯 Objetivo

Criar uma pipeline automatizada capaz de:

1. Gerar músicas lo-fi com IA
2. Criar atmosferas sonoras coerentes
3. Exportar em múltiplos formatos, incluindo áudio (`.wav`, `.mp3`) e musical (`.mid`)
4. Integrar identidade visual e narrativa
5. Produzir conteúdos multimídia prontos para publicação

---

# 🏗️ Arquitetura do Sistema

O Auralith foi projetado como um pipeline modular de geração de conteúdo multimídia baseado em IA.

## 🔹 Camadas do sistema

### 1. Camada de Geração Musical
- Utiliza modelos como MusicGen (Facebook/Meta)
- Responsável pela criação de áudio lo-fi a partir de prompts

### 2. Camada de Prompt Engine
- Define estilos musicais e variações criativas
- Permite geração aleatória ou guiada por temas

### 3. Camada de Orquestração
- `MusicGenerationService` e `TrackGenerator`
- Coordena a geração, o pós-processamento e a exportação dos arquivos.

### 4. Camada de Saída
- Exporta arquivos de áudio nos formatos **`.wav`** e **`.mp3`**.
- Exporta arquivos musicais no formato **`.mid`** para edição em DAWs (ex: LMMS).

## 🔄 Fluxo do sistema

Prompt → Pipeline de Geração → Pós-processamento → Arquivo de Áudio (`.wav` ou `.mp3`) + Arquivo MIDI (`.mid`)

---

# ⚙️ Como executar o projeto

## 1. Instalação do Ambiente Principal

Este ambiente é responsável pela geração de áudio e pela interface web.

```bash
# Navegue até o diretório do projeto
cd /path/to/auralith

# Crie e ative o ambiente virtual principal
python3 -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Instalação do Ambiente MIDI (Opcional)

Este ambiente secundário é **necessário apenas se você deseja gerar arquivos `.mid`**. Ele resolve um conflito de dependências complexo de forma isolada.

```bash
# Instale o Python 3.11 (se ainda não tiver)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv

# Crie o ambiente virtual para o transcritor MIDI
python3.11 -m venv .venv-midi

# Ative e instale as dependências do transcritor
source .venv-midi/bin/activate
pip install basic-pitch "tensorflow-cpu<2.15"
deactivate
```

## 3. Executando a Aplicação

Após a instalação, certifique-se de que o ambiente principal está ativo (`source .venv/bin/activate`) e inicie a interface web:

```bash
python run_web.py
```
Acesse: **http://localhost:7860**

### Usando a Interface Web:
- Preencha os campos de `Project Name` e `Style Prompt`.
- Na aba **"🎵 Track Definitions"**, você encontrará as novas opções:
  - **Audio Format**: Selecione `.wav` ou `.mp3`. O padrão é `.wav`.
  - **Generate MIDI File**: Marque esta caixa para gerar um arquivo `.mid` adicional.
- Clique em **"🚀 GENERATE"**.
- Acompanhe o progresso no console e baixe os arquivos gerados.

---

# 📁 Estrutura do Projeto

```
auralith/
├── .venv/                 # Ambiente virtual principal (Python 3.12)
├── .venv-midi/            # Ambiente virtual para MIDI (Python 3.11)
├── src/
│   ├── scripts/           # Pipeline de geração e transcrição
│   │   ├── generator.py
│   │   ├── musicgen_engine.py
│   │   └── transcribe.py  # <-- Novo script de transcrição
│   ├── services/          # Camada de aplicação
│   │   └── music_service.py
│   ├── web/               # Interface Web
│   │   └── app.py
│   └── ai_agent/          # Prompts e documentação
├── outputs/               # Arquivos gerados
├── docs/                  # Documentação de arquitetura e fixes
├── run_web.py             # Script de execução da interface Web
├── requirements.txt       # Dependências do ambiente principal
└── README.md
```

---

# 📦 Requisitos

- **Ambiente Principal**: Python 3.12+
- **Ambiente MIDI**: Python 3.11
- PyTorch, Transformers, Diffusers, Pydub, Gradio

---

# 🚧 Status do Projeto

✔ Geração de música lo-fi funcional  
✔ Pipeline modular com LangChain  
✔ Interface Web com Gradio  
✔ **Exportação para .wav, .mp3 e .mid implementada**  
🚧 Geração de vídeo (em desenvolvimento)  
🚧 Integração com personagem Aelion  
🚧 Rádio lo-fi contínua (em planejamento)  

---

# 🌌 Visão

Auralith é projetado como um sistema escalável de criação de universos criativos, onde música, narrativa e identidade visual coexistem.

---

# 📄 Licença

Este projeto é proprietário e confidencial.  
Todos os direitos reservados.
