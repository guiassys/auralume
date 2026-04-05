# Auralith - Pipeline de Geração Musical

Este README descreve o fluxo de geração de música no diretório `src` do projeto Auralith.

## O que há aqui

- `src/scripts/generate_lofi_ai.py` - entrypoint principal para gerar música Lo-fi por linha de comando.
- `src/scripts/generator.py` - classe `LofiGenerator` que gerencia a geração, o prompt e o salvamento do áudio.
- `src/scripts/musicgen_engine.py` - engine que carrega o modelo MusicGen e gera o áudio em chunks.
- `src/scripts/music_pipeline.py` - pipeline modular baseado em `langchain_core` com etapas:
  - melodia musical
  - base rítmica
  - faixa instrumental
  - mixagem
- `src/scripts/prompts.py` - prompts de exemplo para geração Lo-fi.

## Como usar

1. Ative o ambiente virtual do projeto:

```powershell
cd c:\devtools\repo\auralith
.\musicgen310\Scripts\Activate.ps1
```

2. Execute o gerador:

```powershell
python -m src.scripts.generate_lofi_ai
```

3. Siga as instruções na tela:
- Informe a duração em segundos
- Informe um prompt de estilo musical (por exemplo, `hip hop`, `lo-fi`, `rock`)
- Opcionalmente, informe um nome para o arquivo

## Arquitetura do pipeline

A geração musical usa um pipeline modular para transformar o prompt inicial em um prompt final otimizado para o modelo.

1. `MusicPipeline._melody_stage`: cria a ideia de melodia base.
2. `MusicPipeline._rhythm_stage`: escolhe BPM e descreve a base rítmica.
3. `MusicPipeline._combine_stage`: une melodia e ritmo.
4. `MusicPipeline._instrument_stage`: define instrumentos e timbres.
5. `MusicPipeline._mix_stage`: produz o prompt final que é enviado ao `MusicGenEngine`.

## Requisitos básicos

- Python 3.10+
- `torch`
- `transformers`
- `soundfile`
- `numpy`
- `langchain`

## Observações

- O pipeline preserva a lógica existente do gerador.
- `MusicPipeline` permite extensão futura com etapas adicionais.
- A engine atual usa chunks de 30 segundos para gerar áudio de forma incremental.

## Exemplo de uso rápido

```python
from src.scripts.generator import LofiGenerator

gen = LofiGenerator()
path = gen.generate(prompt="hip hop chill, piano suave", duration=60, name="minha_musica")
print(path)
```
