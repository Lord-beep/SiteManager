SiteManager

Aplicação desktop para gerir e automatizar sites alojados em diferentes plataformas.

O SiteManager permite guardar vários sites, proteger as credenciais localmente e executar ações específicas para cada plataforma através de uma interface gráfica.

✨ Funcionalidades
🖥️ Interface gráfica com CustomTkinter
🌐 Gestão de vários sites
➕ Adicionar novos sites
✏️ Editar sites existentes
🗑️ Apagar sites
🟢 Ativar ou desativar sites
▶️ Executar ações manualmente
⏱️ Configuração de intervalos de execução
🔐 Proteção das credenciais através de encriptação
🔑 Proteção através de palavra-passe principal
💾 Base de dados SQLite local
🐍 Integração com PythonAnywhere
⚡ Integração com Supabase
📦 Possibilidade de criar uma versão portable
☁️ Plataformas suportadas
PythonAnywhere

Permite executar o reload de uma aplicação web através da API do PythonAnywhere.

São utilizadas:

Username
API Key
Domínio da aplicação
Supabase

Permite verificar o estado de um projeto Supabase e solicitar a sua reativação quando este estiver pausado.

São utilizados:

Personal Access Token
Project Ref
🔐 Segurança

As credenciais dos sites são armazenadas localmente numa base de dados SQLite e protegidas através de encriptação.

Os ficheiros locais que contêm dados privados não devem ser enviados para o GitHub.

Por isso, dados como:

data/
config/
logs/


estão excluídos através do .gitignore.

Nunca coloques API Keys, tokens, passwords ou chaves de encriptação diretamente no código ou no repositório.

🛠️ Tecnologias
Python
CustomTkinter
SQLite
Requests
PyInstaller
📁 Estrutura
SiteManager/
│
├── core/
│   ├── executors/
│   ├── platforms.py
│   ├── site_manager.py
│   └── models.py
│
├── gui/
│   ├── app.py
│   ├── add_site.py
│   ├── edit_site.py
│   └── sites_view.py
│
├── security/
│
├── database.py
├── paths.py
├── security.py
├── main.py
├── requirements.txt
└── .gitignore

🚀 Instalação

Clona o repositório:

git clone https://github.com/Lord-beep/SiteManager.git
cd SiteManager


Cria um ambiente virtual:

python -m venv .venv


Ativa o ambiente virtual no Windows:

.venv\Scripts\activate


Instala as dependências:

pip install -r requirements.txt

▶️ Executar

Com o ambiente virtual ativo:

python -m gui.app


Na primeira utilização, a aplicação irá criar os diretórios e ficheiros locais necessários.

📦 Versão Portable

O projeto pode ser compilado como um executável Windows utilizando PyInstaller:

pyinstaller --noconfirm --clean --windowed --onefile --name SiteManager .\gui\app.py


O executável será criado em:

dist/SiteManager.exe


Os dados locais da aplicação devem permanecer separados do executável.

🧪 Testes

O projeto inclui testes para diferentes componentes, incluindo:

Core
Base de dados
Encriptação
Segurança
Sessão
Supabase

Os testes podem ser executados com:

pytest

📌 Estado do projeto

O projeto encontra-se em desenvolvimento.

Novas plataformas e funcionalidades poderão ser adicionadas futuramente.

👤 Autor

Lord-beep

