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

Prompt → MusicGenEngine → Processamento Tensor → Pós-processamento → Arquivo WAV

---

# ⚙️ Como executar o projeto
```bash
python -m venv musicgen310
musicgen310\activate
pip install torch
pip install numpy transformers
pip install soundfile
python -m src.scripts.generate_lofi_ai
```
## Resultado
O áudio será gerado automaticamente na raiz do projeto:


# 📁 Estrutura do Projeto

```
auralith/
├── src/
└── README.md
```

---

# 📦 Requisitos

- Python 3.10+
- PyTorch
- Transformers (Hugging Face)
- SoundFile
- NumPy

---

# 💰 Monetização (visão futura)

- Monetização via YouTube (lo-fi livestreams)
- Distribuição em plataformas de streaming
- Parcerias com marcas de bem-estar e produtividade
- Venda de conteúdos digitais e assets exclusivos

---

# 🚧 Status do Projeto

✔ Geração de música lo-fi funcional  
✔ Pipeline local executando em CPU  
✔ Exportação de áudio WAV  
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
