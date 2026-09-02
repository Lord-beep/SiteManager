# 🚀 SiteManager

Desktop application for managing and automating websites hosted on different platforms.

SiteManager provides a simple graphical interface to manage websites, securely store credentials locally, and execute platform-specific actions.

---

## ✨ Features

- 🖥️ Graphical interface built with CustomTkinter
- 🌐 Manage multiple websites
  - ➕ Add websites
  - ✏️ Edit websites
  - 🗑️ Delete websites
  - 🟢 Enable / disable websites
- ▶️ Execute website actions manually
- ⏱️ Configure execution intervals
- 🔐 Encrypted credential storage
- 🔑 Master password protection
- 💾 Local SQLite database
- ☁️ PythonAnywhere integration
- ⚡ Supabase integration
- 📦 Windows portable version

---

## ☁️ Supported Platforms

### 🐍 PythonAnywhere

SiteManager uses the PythonAnywhere API to reload web applications.

**Required:**
- Username
- API Key
- Domain

### ⚡ Supabase

SiteManager uses the Supabase Management API to check the project status and request a resume when the project is paused.

**Required:**
- Personal Access Token
- Project Ref

---

## 🔐 Security

Sensitive credentials are encrypted before being stored locally.

Local data must never be uploaded to GitHub. The following directories are ignored by Git:

```
data/
config/
logs/
.venv/
build/
dist/
```

> ⚠️ **Never** commit passwords, API keys, access tokens, encryption keys, or other sensitive information to GitHub.

---

## 🛠️ Technologies

- Python
- CustomTkinter
- SQLite
- Requests
- PyInstaller

---

## 📁 Project Structure

```
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
```

---

## 🚀 Installation

### Requirements

- Windows
- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Lord-beep/SiteManager.git
cd SiteManager
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**PowerShell**
```powershell
.venv\Scripts\activate
```

**Git Bash**
```bash
source .venv/Scripts/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running

Start the application with:

```bash
python -m gui.app
```

The required local directories are created automatically.

---

## 📦 Portable Version

A Windows portable executable can be created using PyInstaller:

```bash
pyinstaller --noconfirm --clean --windowed --onefile --name SiteManager .\gui\app.py
```

The executable will be created in:

```
dist/
└── SiteManager.exe
```

The application uses external folders for persistent local data:

```
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
```

> These files contain local data and should not be uploaded to GitHub.

---

## 🧪 Tests

The project includes tests for:

- Core functionality
- Database
- Encryption
- Security
- Session management
- Supabase integration

Run the tests with:

```bash
pytest
```

---

## 🔄 Git Workflow

After making changes:

```bash
git status
git add .
git commit -m "Describe your changes"
git push
```

---

## 📌 Project Status

🚧 **Work in progress**

SiteManager is currently under development. More platforms, automation features, and improvements may be added in future versions.

---

## 👤 Author

**Lord-beep**


No license has been defined for this project yet.
