import requests


PROJECT_REF = "lrccdnvqjwfosmrwqjoh"

TOKEN = input("Cola o teu PAT do Supabase: ").strip()

response = requests.get(
    f"https://api.supabase.com/v1/projects/{PROJECT_REF}",
    headers={
        "Authorization": f"Bearer {TOKEN}",
    },
    timeout=30,
)

print("HTTP:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("Nome:", data.get("name"))
    print("Estado:", data.get("status"))
    print("Project Ref:", data.get("ref"))

else:
    print(response.text)
