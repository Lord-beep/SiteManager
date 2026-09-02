from database import initialize_database


def main():
    print("=" * 40)
    print("        SITE MANAGER")
    print("=" * 40)

    initialize_database()

    print()
    print("Base de dados pronta.")
    print("Programa iniciado!")


if __name__ == "__main__":
    main()
