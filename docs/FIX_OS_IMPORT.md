# Correção - Importação do módulo 'os'

## Problema
Erro `NameError: name 'os' is not defined` ao tentar salvar arquivos de áudio.

## Causa
O módulo `os` foi usado em `save_audio()` mas não foi importado no arquivo `src/scripts/generator.py`.

## Solução
Adicionado `import os` no topo do arquivo junto com os outros imports.

## Arquivos Modificados
- `src/scripts/generator.py`: Adicionado `import os`

## Status
✅ Corrigido - arquivos agora serão salvos corretamente no diretório `outputs/`