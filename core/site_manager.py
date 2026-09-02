from datetime import datetime, timezone

from database import get_connection
from core.models import Site


class SiteManager:

    # =========================
    # ADICIONAR SITE
    # =========================

    def add_site(
        self,
        name: str,
        platform: str,
        interval_minutes: int,
        username: str | None,
        password: str | None,
        api_key: str | None,
        domain: str | None,
        encryption,
    ) -> int:

        from database import add_site as database_add_site

        return database_add_site(
            name=name,
            platform=platform,
            interval_minutes=interval_minutes,
            username=username,
            password=password,
            api_key=api_key,
            domain=domain,
            encryption=encryption,
        )

    # =========================
    # LISTAR SITES
    # =========================

    def list_sites(self) -> list[Site]:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                platform,
                domain,
                interval_minutes,
                active,
                last_execution
            FROM sites
            ORDER BY id
        """)

        rows = cursor.fetchall()

        connection.close()

        return [
            Site(
                id=row[0],
                name=row[1],
                platform=row[2],
                domain=row[3],
                interval_minutes=row[4],
                active=bool(row[5]),
                last_execution=row[6],
            )
            for row in rows
        ]

    # =========================
    # OBTER SITE
    # =========================

    def get_site(
        self,
        site_id: int
    ) -> Site | None:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                platform,
                domain,
                interval_minutes,
                active,
                last_execution
            FROM sites
            WHERE id = ?
        """, (site_id,))

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return Site(
            id=row[0],
            name=row[1],
            platform=row[2],
            domain=row[3],
            interval_minutes=row[4],
            active=bool(row[5]),
            last_execution=row[6],
        )

    # =========================
    # ATIVAR / DESATIVAR
    # =========================

    def set_active(
        self,
        site_id: int,
        active: bool
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE sites
            SET active = ?
            WHERE id = ?
        """, (
            1 if active else 0,
            site_id,
        ))

        connection.commit()
        connection.close()

    # =========================
    # APAGAR SITE
    # =========================

    def delete_site(
        self,
        site_id: int
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM sites
            WHERE id = ?
        """, (site_id,))

        connection.commit()
        connection.close()

    # =========================
    # OBTER CREDENCIAIS DO SITE
    # =========================

    def get_site_credentials(
        self,
        site_id: int,
        encryption
    ):

        from database import get_credentials

        return get_credentials(
            site_id,
            encryption
        )

    # =========================
    # EDITAR SITE
    # =========================

    def update_site(
        self,
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

        from database import update_site as database_update_site

        database_update_site(
            site_id=site_id,
            name=name,
            platform=platform,
            interval_minutes=interval_minutes,
            username=username,
            password=password,
            api_key=api_key,
            domain=domain,
            encryption=encryption,
        )

    # =========================
    # EXECUTAR SITE
    # =========================

    def execute_site(
        self,
        site_id: int,
        encryption
    ):

        from database import get_credentials
        from core.platforms import get_executor

        # =========================
        # OBTER SITE
        # =========================

        site = self.get_site(site_id)

        if site is None:
            raise ValueError(
                "Site não encontrado."
            )

        if not site.active:
            raise ValueError(
                "Este site está desativado."
            )

        # =========================
        # OBTER CREDENCIAIS
        # =========================

        credentials = get_credentials(
            site_id,
            encryption
        )

        # O domínio/project ref está
        # guardado na tabela sites.
        credentials["domain"] = site.domain

        # =========================
        # OBTER EXECUTOR
        # =========================

        executor = get_executor(
            site.platform,
            credentials
        )

        # =========================
        # EXECUTAR
        # =========================

        result = executor.execute(
            site=site,
            credentials=credentials
        )

        # =========================
        # REGISTAR EXECUÇÃO
        # =========================

        execution_time = datetime.now(
            timezone.utc
        ).astimezone().isoformat(
            timespec="seconds"
        )

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE sites
            SET last_execution = ?
            WHERE id = ?
        """, (
            execution_time,
            site_id,
        ))

        connection.commit()
        connection.close()

        # =========================
        # RESULTADO
        # =========================

        return {
            "message": result.get(
                "message",
                "Site executado com sucesso."
            ),
            "execution_time": execution_time,
        }
