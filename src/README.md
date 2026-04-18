# Auralume - Pipeline de Geração Musical

Este README descreve o fluxo de geração de música no diretório `src` do projeto Auralume.

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
- `src/services/music_service.py` - serviço que encapsula a lógica de geração para reutilização.
- `src/web/app.py` - interface Web usando Gradio.
- `src/web/run_web.py` - script para executar a interface Web.

## Como usar

### Via Terminal
1. Ative o ambiente virtual do projeto:
```powershell
cd c:\devtools\repo\auralume
.\musicgen310\Scripts\Activate.ps1
```

2. Execute o gerador:
```powershell
python -m src.scripts.generate_lofi_ai
```

### Via Interface Web
1. Instale Gradio:
```bash
pip install gradio
```

2. Execute a interface (do diretório raiz do projeto):
```bash
python src/web/run_web.py
```

3. Acesse: http://localhost:7860

**Importante:** Execute sempre a partir do diretório raiz do projeto (`auralume/`) para que os imports Python funcionem corretamente.

## Arquitetura do pipeline

A geração musical usa um pipeline modular para transformar o prompt inicial em um prompt final otimizado para o modelo.

1. `MusicPipeline._melody_stage`: cria a ideia de melodia base.
2. `MusicPipeline._rhythm_stage`: escolhe BPM e descreve a base rítmica.
3. `MusicPipeline._combine_stage`: une melodia e ritmo.
4. `MusicPipeline._instrument_stage`: define instrumentos e timbres.
5. `MusicPipeline._mix_stage`: produz o prompt final que é enviado ao `MusicGenEngine`.

## Diretórios de saída

- **CLI**: Arquivos salvos no diretório atual (raiz do projeto)
- **Web**: Arquivos salvos em `outputs/` (relativo à raiz do projeto)
- **Programático**: Depende do parâmetro `output_dir` passado para `MusicGenerationService`

## Requisitos básicos

- Python 3.10+
- `torch`
- `transformers`
- `soundfile`
- `numpy`
- `langchain`
- `gradio` (para interface Web)

## Observações

- O pipeline preserva a lógica existente do gerador.
- `MusicPipeline` permite extensão futura com etapas adicionais.
- A engine atual usa chunks de 30 segundos para gerar áudio de forma incremental.
- A interface Web reutiliza o pipeline sem modificá-lo.

```
