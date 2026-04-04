from src.generator import LofiGenerator


def main():
    gen = LofiGenerator()

    print("[START] Gerando música Lo-fi com IA...\n")

    path = gen.generate(duration=30)

    print(f"\n[FINAL] Arquivo gerado: {path}")


if __name__ == "__main__":
    main()