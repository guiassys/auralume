from src.generator import LofiGenerator


def main():
    gen = LofiGenerator()

    print("[START] Gerando música Lo-fi com IA...\n")

    try:
        duration = int(input("Informe a duração da musica. Ex (30 ou 180): "))
    except ValueError:
        duration = 180
        print("Valor inválido, usando 180 segundos.")

    path = gen.generate(duration=duration)

    print(f"\n[FINAL] Arquivo gerado: {path}")


if __name__ == "__main__":
    main()