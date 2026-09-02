from database import initialize_database
from core.site_manager import SiteManager


MASTER_PASSWORD = "MinhaPasswordMestre123!"


initialize_database()

manager = SiteManager()

site_id = manager.add_site(
    name="Site de Teste",
    platform="PythonAnywhere",
    interval_minutes=60,
    username="teste",
    password="password_falsa",
    api_key="API_KEY_FALSA",
    master_password=MASTER_PASSWORD,
)

print("Site criado:", site_id)

print("\nSites existentes:")

sites = manager.list_sites()

for site in sites:
    print(site)
