from core.executors.pythonanywhere import PythonAnywhereExecutor
from core.executors.supabase import SupabaseExecutor


PLATFORMS = {
    "PythonAnywhere": {
        "name": "PythonAnywhere",
        "status": "available",
    },
    "Supabase": {
        "name": "Supabase",
        "status": "available",
    },
}


def get_platform_names() -> list[str]:
    return list(PLATFORMS.keys())


def is_platform_supported(platform: str) -> bool:
    return platform in PLATFORMS


def get_platform(platform: str) -> dict:

    if platform not in PLATFORMS:
        raise ValueError(
            f"Plataforma não suportada: {platform}"
        )

    return PLATFORMS[platform]


def get_executor(
    platform: str,
    credentials: dict
):

    if platform == "PythonAnywhere":
        return PythonAnywhereExecutor(
            credentials
        )

    if platform == "Supabase":
        return SupabaseExecutor(
            credentials
        )

    raise ValueError(
        f"Executor não disponível para a plataforma: {platform}"
    )
