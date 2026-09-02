import requests


class PythonAnywhereExecutor:

    BASE_URL = "https://www.pythonanywhere.com/api/v0/user"

    def __init__(self, credentials: dict):
        self.credentials = credentials

    def execute(
        self,
        site=None,
        credentials=None
    ) -> dict:

        if credentials is None:
            credentials = self.credentials

        username = credentials.get("username")
        api_key = credentials.get("api_key")
        domain = credentials.get("domain")

        if not username:
            raise ValueError(
                "Username do PythonAnywhere não configurado."
            )

        if not api_key:
            raise ValueError(
                "API Key do PythonAnywhere não configurada."
            )

        if not domain:
            raise ValueError(
                "Domínio do PythonAnywhere não configurado."
            )

        url = (
            f"{self.BASE_URL}/"
            f"{username}/webapps/{domain}/reload/"
        )

        headers = {
            "Authorization": f"Token {api_key}"
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                timeout=30
            )

        except requests.RequestException as error:
            raise RuntimeError(
                f"Não foi possível contactar o PythonAnywhere: {error}"
            ) from error

        if response.status_code in (200, 201, 204):
            return {
                "success": True,
                "message": (
                    f"Site {domain} recarregado "
                    "com sucesso no PythonAnywhere."
                ),
            }

        try:
            details = response.json()

        except ValueError:
            details = response.text

        raise RuntimeError(
            f"PythonAnywhere devolveu HTTP "
            f"{response.status_code}: {details}"
        )
