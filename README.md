[🚀 SiteManager

SiteManager é uma aplicação desktop desenvolvida em Python para gerir e automatizar sites alojados em diferentes plataformas.

A aplicação permite adicionar, editar, ativar, desativar e executar ações nos sites através de uma interface gráfica simples, mantendo as credenciais protegidas localmente.

✨ Funcionalidades
🖥️ Interface gráfica moderna com CustomTkinter
🌐 Gestão de múltiplos sites
➕ Adicionar sites
✏️ Editar sites
🗑️ Apagar sites
🟢 Ativar / desativar sites
▶️ Executar ações manualmente
⏱️ Configurar intervalos de execução
🔐 Encriptação das credenciais
🔑 Sistema de palavra-passe principal
💾 Base de dados local com SQLite
☁️ Integração com PythonAnywhere
⚡ Integração com Supabase
📦 Suporte para criação de versão portable para Windows
☁️ Plataformas suportadas
🐍 PythonAnywhere

O SiteManager utiliza a API do PythonAnywhere para recarregar aplicações web.

São utilizadas as seguintes informações:

Campo	Utilização
Username	Identificação da conta
API Key	Autenticação na API
Domínio	Identificação da aplicação
⚡ Supabase

A integração com Supabase permite verificar o estado de um projeto e solicitar a sua reativação quando este estiver pausado.

São utilizadas:

Campo	Utilização
Personal Access Token	Autenticação na API
Project Ref	Identificação do projeto
🔐 Segurança

As credenciais dos sites são armazenadas localmente numa base de dados SQLite e protegidas através de encriptação.

Os dados privados são mantidos fora do código-fonte e devem permanecer fora do GitHub.

Ficheiros e diretórios locais ignorados pelo Git:

data/
config/
logs/
.venv/
dist/
build/


⚠️ Nunca publiques API Keys, tokens, passwords ou chaves de encriptação no GitHub.

🛠️ Tecnologias
🐍 Python
🎨 CustomTkinter
🗄️ SQLite
🌐 Requests
📦 PyInstaller
📁 Estrutura do projeto
SiteManager/
│
├── core/
│   ├── executors/
│   │   ├── pythonanywhere.py
│   │   └── supabase.py
│   │
│   ├── models.py
│   ├── platforms.py
│   └── site_manager.py
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
├── .gitignore
└── README.md

🚀 Instalação
1. Clonar o repositório
git clone https://github.com/Lord-beep/SiteManager.git


Entrar na pasta:

cd SiteManager

2. Criar o ambiente virtual
python -m venv .venv

3. Ativar o ambiente virtual

No Windows:

.venv\Scripts\activate

4. Instalar as dependências
pip install -r requirements.txt

▶️ Executar

Com o ambiente virtual ativo:

python -m gui.app


A aplicação irá criar os diretórios necessários para os dados locais.

📦 Criar versão Portable

O projeto pode ser compilado para um executável Windows utilizando PyInstaller.

pyinstaller --noconfirm --clean --windowed --onefile --name SiteManager .\gui\app.py


Depois da compilação:

dist/
└── SiteManager.exe

Dados locais

O executável utiliza diretórios externos para guardar os dados da aplicação:

SiteManager/
│
├── SiteManager.exe
│
├── data/
│   └── sites.db
│
└── config/
    ├── encryption.key
    └── master_password.dat


Estes ficheiros contêm dados locais e não devem ser publicados no GitHub.

🧪 Testes

O projeto inclui testes para diferentes componentes:

Core
Base de dados
Encriptação
Segurança
Gestão de sessão
Supabase

Para executar os testes:

pytest

🔄 Git

Para obter a versão mais recente:

git pull


Para enviar alterações:

git add .
git commit -m "Update SiteManager"
git push

📌 Estado do projeto

🚧 Em desenvolvimento

O SiteManager encontra-se em desenvolvimento e novas funcionalidades e plataformas poderão ser adicionadas no futuro.

👤 Autor

Lord-beep

GitHub:

https://github.com/Lord-beep

](https://github.com/Lord-beep/SiteManager faz o read me)
