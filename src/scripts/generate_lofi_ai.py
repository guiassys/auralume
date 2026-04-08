"""Entrypoint para gerar música com o pipeline modular.

Execução:
    python -m src.scripts.generate_lofi_ai
"""

from src.scripts.generator import LofiGenerator
from src.scripts.prompts import LOFI_PROMPTS


DEFAULT_DURATION = 180
OUTPUT_DIR = "outputs"


def get_duration() -> int:
    """Solicita duração da música ao usuário."""
    try:
        return int(input("Informe a duração da musica em segundos. Ex (30 ou 180): "))
    except ValueError:
        print(f"Valor inválido, usando {DEFAULT_DURATION} segundos.")
        return DEFAULT_DURATION


def show_prompt_examples() -> None:
    """Exibe exemplos de prompts disponíveis."""
    print("\nExemplos de prompt:")
    for prompt_example in LOFI_PROMPTS:
        print(f" - {prompt_example}")


def get_music_prompt() -> str | None:
    """Coleta o prompt da música."""
    prompt = input(
        "\nInforme as características/prompt da música (ou pressione Enter para usar um prompt aleatório): "
    ).strip()

    return prompt if prompt else None


def get_song_name() -> str | None:
    """Coleta o nome da música."""
    song_name = input(
        "Informe um nome para a música (opcional, pressione Enter para nome automático): "
    ).strip()

    return song_name if song_name else None


def generate_music():
    """Executa o fluxo principal de geração de música."""
    gen = LofiGenerator(output_dir=OUTPUT_DIR)

    print("[START] Gerando música Lo-fi com IA...\n")

    duration = get_duration()
    show_prompt_examples()

    prompt = get_music_prompt()
    song_name = get_song_name()

    path = gen.generate(prompt=prompt, duration=duration, name=song_name)

    print(f"\n[FINAL] Arquivo gerado: {path}")


def main():
    generate_music()


if __name__ == "__main__":
    main()