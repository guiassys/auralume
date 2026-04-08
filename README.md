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
3. Integrar identidade visual e narrativa  
4. Produzir conteúdos multimídia prontos para publicação  
5. Expandir para vídeos e distribuição em plataformas digitais  

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
- Classe `LofiGenerator`
- Coordena geração, processamento e salvamento de áudio

### 4. Camada de Saída
- Exporta arquivos `.wav`
- Futuro suporte para MP3, vídeo e streaming

## 🔄 Fluxo do sistema

Prompt → Pipeline de prompt → MusicGenEngine → Processamento Tensor → Pós-processamento → Arquivo WAV

---

# ⚙️ Como executar o projeto

## Instalação desenvolvedor wsl + Ubuntu
```bash
cd ~/devtools/repos/auralith
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run_web.py
```


## Instalação rápida
```bash
python -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Via Terminal (CLI)
```bash
python -m src.scripts.generate_lofi_ai
```

## Via Interface Web (Gradio)
```bash
python run_web.py
```
Acesse: http://localhost:7860

**Interface Web:**
- Preencha o nome da música (opcional)
- Selecione a duração (30, 60, 90 ou 180 segundos)
- Digite o estilo musical desejado
- Clique em "Gerar Música"
- Acompanhe o progresso pelas notificações
- Baixe o arquivo gerado quando concluído

**Nota:** Este script pode ser executado de qualquer diretório e detecta automaticamente a localização do projeto.

## Resultado
O áudio será gerado automaticamente no diretório onde o comando for executado (CLI) ou em `outputs/` (Web).

## Exemplo programático
Veja `example.py` para uso programático do serviço de geração.

## Observações
- O pipeline de geração agora está implementado em `src/scripts/music_pipeline.py`.
- A classe `LofiGenerator` em `src/scripts/generator.py` usa o pipeline para criar um prompt final antes de acionar o modelo.
- A interface Web reutiliza o pipeline existente sem alterações.
- Um README adicional com detalhes do pipeline está disponível em `src/README.md`.

# 📁 Estrutura do Projeto

```
auralith/
├── src/
│   ├── scripts/          # Pipeline de geração musical
│   │   ├── generate_lofi_ai.py
│   │   ├── generator.py
│   │   ├── musicgen_engine.py
│   │   ├── music_pipeline.py
│   │   └── prompts.py
│   ├── services/         # Camada de aplicação
│   │   └── music_service.py
│   ├── web/              # Interface Web
│   │   ├── app.py
│   │   └── run_web.py
│   └── ai_agent/         # Prompts e documentação
├── outputs/              # Arquivos gerados
├── run_web.py            # Script de execução da interface Web
├── example.py            # Exemplo programático
├── requirements.txt      # Dependências
├── musicgen310/          # Ambiente virtual
└── README.md
```

---

# 📦 Requisitos

- Python 3.10+
- PyTorch
- Transformers (Hugging Face)
- SoundFile
- NumPy
- LangChain
- Gradio (para interface Web)

---

# 💰 Monetização (visão futura)

- Monetização via YouTube (lo-fi livestreams)
- Distribuição em plataformas de streaming
- Parcerias com marcas de bem-estar e produtividade
- Venda de conteúdos digitais e assets exclusivos

---

# 🚧 Status do Projeto

✔ Geração de música lo-fi funcional  
✔ Pipeline modular com LangChain  
✔ Interface Web com Gradio (funcionando)  
✔ Salvamento correto em diretórios  
✔ Execução via CLI e Web  
🚧 Geração de vídeo (em desenvolvimento)  
🚧 Integração com personagem Aelion  
🚧 Rádio lo-fi contínua (em planejamento)  

---

# 🌌 Visão

Auralith é projetado como um sistema escalável de criação de universos criativos, onde música, narrativa e identidade visual coexistem.

Personagens como Aelion são apenas o início de múltiplas possibilidades de mundos gerados por IA.

---

# 📄 Licença

Este projeto é proprietário e confidencial.  
Todos os direitos reservados.
