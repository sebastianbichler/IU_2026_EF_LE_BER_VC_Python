from .generator import generate_dummy_data

def main():
    print("🐿️  Sammy Squirrels Secret Stash - Gruppe 02 (Clean src Layout)")
    print("-------------------------------------------------------------")

    # 1. Daten generieren
    my_stashes = generate_dummy_data(5)

    # 2. Daten anzeigen
    print("\n📦 Inventar-Check:")
    for stash in my_stashes:
        print(stash)

    print("\n✅ System läuft erfolgreich aus dem src-Ordner!")

if __name__ == "__main__":
    main()