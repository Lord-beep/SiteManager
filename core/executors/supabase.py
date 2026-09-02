import requests


class SupabaseExecutor:

    BASE_URL = "https://api.supabase.com/v1"

    def __init__(self, credentials: dict):
        self.credentials = credentials

    def execute(
        self,
        site=None,
        credentials=None
    ) -> dict:

        if credentials is None:
            credentials = self.credentials

        access_token = credentials.get("api_key")
        project_ref = credentials.get("domain")

        if not access_token:
            raise ValueError(
                "Personal Access Token do Supabase não configurado."
            )

        if not project_ref:
            raise ValueError(
                "Project Ref do Supabase não configurado."
            )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # =========================
        # VERIFICAR ESTADO
        # =========================

        try:

            response = requests.get(
                f"{self.BASE_URL}/projects/{project_ref}",
                headers=headers,
                timeout=30,
            )

        except requests.RequestException as error:

            raise RuntimeError(
                f"Não foi possível contactar o Supabase: {error}"
            ) from error

        if response.status_code != 200:

            raise RuntimeError(
                f"Supabase devolveu HTTP "
                f"{response.status_code}: {response.text}"
            )

        project = response.json()

        status = project.get("status")

        # =========================
        # JÁ ESTÁ ONLINE
        # =========================

        if status != "PAUSED":

            return {
                "success": True,
                "message": (
                    f"Projeto Supabase já está online. "
                    f"Estado: {status}"
                ),
            }

        # =========================
        # PROJETO PAUSADO
        # =========================

        try:

            response = requests.post(
                f"{self.BASE_URL}/projects/{project_ref}/resume",
                headers=headers,
                timeout=30,
            )

        except requests.RequestException as error:

            raise RuntimeError(
                f"Não foi possível contactar o Supabase: {error}"
            ) from error

        if response.status_code not in (200, 201, 202):

            raise RuntimeError(
                f"Supabase devolveu HTTP "
                f"{response.status_code}: {response.text}"
            )

        return {
            "success": True,
            "message": (
                "Projeto Supabase estava pausado "
                "e foi solicitado o reinício."
            ),
        }
