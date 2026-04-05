"""Entrypoint para gerar música com o pipeline modular.

Execução:
    python -m src.scripts.generate_lofi_ai
"""

from src.scripts.generator import LofiGenerator
from src.scripts.prompts import LOFI_PROMPTS


def main():
    gen = LofiGenerator(output_dir="outputs")

    print("[START] Gerando música Lo-fi com IA...\n")

    try:
        duration = int(input("Informe a duração da musica em segundos. Ex (30 ou 180): "))
    except ValueError:
        duration = 180
        print("Valor inválido, usando 180 segundos.")

    print("\nExemplos de prompt:")
    for prompt_example in LOFI_PROMPTS:
        print(f" - {prompt_example}")

    prompt = input("\nInforme as características/prompt da música (ou pressione Enter para usar um prompt aleatório): ").strip()
    if not prompt:
        prompt = None

    song_name = input("Informe um nome para a música (opcional, pressione Enter para nome automático): ").strip()
    if not song_name:
        song_name = None

    path = gen.generate(prompt=prompt, duration=duration, name=song_name)

    print(f"\n[FINAL] Arquivo gerado: {path}")


if __name__ == "__main__":
    main()