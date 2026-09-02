import sqlite3

from paths import DATABASE_PATH, initialize_directories


def get_connection():
    initialize_directories()

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # =========================
    # SITES
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            domain TEXT,
            interval_minutes INTEGER NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            last_execution TEXT
        )
    """)

    # =========================
    # MIGRAÇÃO DA BASE EXISTENTE
    # =========================

    cursor.execute("PRAGMA table_info(sites)")

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "domain" not in columns:

        cursor.execute("""
            ALTER TABLE sites
            ADD COLUMN domain TEXT
        """)

    # =========================
    # CREDENCIAIS
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_id INTEGER NOT NULL,
            username_encrypted BLOB,
            password_encrypted BLOB,
            api_key_encrypted BLOB,
            FOREIGN KEY (site_id) REFERENCES sites(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


# ==========================================================
# ADICIONAR SITE
# ==========================================================

def add_site(
    name: str,
    platform: str,
    interval_minutes: int,
    username: str | None,
    password: str | None,
    api_key: str | None,
    domain: str | None,
    encryption,
) -> int:

    username_encrypted = None
    password_encrypted = None
    api_key_encrypted = None

    # =========================
    # ENCRIPTAR CREDENCIAIS
    # =========================

    if username:

        username_encrypted = encryption.encrypt(
            username
        )

    if password:

        password_encrypted = encryption.encrypt(
            password
        )

    if api_key:

        api_key_encrypted = encryption.encrypt(
            api_key
        )

    # =========================
    # GUARDAR SITE
    # =========================

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO sites (
            name,
            platform,
            domain,
            interval_minutes,
            active
        )
        VALUES (?, ?, ?, ?, 1)
    """, (
        name,
        platform,
        domain,
        interval_minutes,
    ))

    site_id = cursor.lastrowid

    # =========================
    # GUARDAR CREDENCIAIS
    # =========================

    cursor.execute("""
        INSERT INTO credentials (
            site_id,
            username_encrypted,
            password_encrypted,
            api_key_encrypted
        )
        VALUES (?, ?, ?, ?)
    """, (
        site_id,
        username_encrypted,
        password_encrypted,
        api_key_encrypted,
    ))

    connection.commit()
    connection.close()

    return site_id


# ==========================================================
# OBTER CREDENCIAIS
# ==========================================================

def get_credentials(
    site_id: int,
    encryption,
):
    """
    Recupera e desencripta as credenciais
    e o domínio de um site.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Primeiro obtemos o domínio
    cursor.execute("""
        SELECT domain
        FROM sites
        WHERE id = ?
    """, (site_id,))

    site_row = cursor.fetchone()

    if site_row is None:

        connection.close()

        raise ValueError(
            "Site não encontrado."
        )

    domain = site_row[0]

    # Depois obtemos as credenciais
    cursor.execute("""
        SELECT
            username_encrypted,
            password_encrypted,
            api_key_encrypted
        FROM credentials
        WHERE site_id = ?
    """, (site_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:

        raise ValueError(
            "Credenciais não encontradas."
        )

    username_encrypted = row[0]
    password_encrypted = row[1]
    api_key_encrypted = row[2]

    username = None
    password = None
    api_key = None

    # =========================
    # DESENCRIPTAR
    # =========================

    if username_encrypted:

        username = encryption.decrypt(
            username_encrypted
        )

    if password_encrypted:

        password = encryption.decrypt(
            password_encrypted
        )

    if api_key_encrypted:

        api_key = encryption.decrypt(
            api_key_encrypted
        )

    return {
        "username": username,
        "password": password,
        "api_key": api_key,
        "domain": domain,
    }

def update_site(
    site_id: int,
    name: str,
    platform: str,
    interval_minutes: int,
    username: str | None,
    password: str | None,
    api_key: str | None,
    domain: str | None,
    encryption,
):
    """
    Atualiza os dados do site e as credenciais encriptadas.
    """

    username_encrypted = None
    password_encrypted = None
    api_key_encrypted = None

    if username:
        username_encrypted = encryption.encrypt(
            username
        )

    if password:
        password_encrypted = encryption.encrypt(
            password
        )

    if api_key:
        api_key_encrypted = encryption.encrypt(
            api_key
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE sites
        SET
            name = ?,
            platform = ?,
            domain = ?,
            interval_minutes = ?
        WHERE id = ?
    """, (
        name,
        platform,
        domain,
        interval_minutes,
        site_id,
    ))

    cursor.execute("""
        UPDATE credentials
        SET
            username_encrypted = ?,
            password_encrypted = ?,
            api_key_encrypted = ?
        WHERE site_id = ?
    """, (
        username_encrypted,
        password_encrypted,
        api_key_encrypted,
        site_id,
    ))

    connection.commit()
    connection.close()

# ==========================================================
# TESTE / INICIALIZAÇÃO
# ==========================================================

if __name__ == "__main__":

    initialize_database()

    print(
        "Base de dados inicializada com sucesso!"
    )

    print(
        f"Localização: {DATABASE_PATH}"
    )
