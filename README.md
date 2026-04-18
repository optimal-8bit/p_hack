# pHack Template App

Standard starter setup for fast hackathon development with minimal merge conflicts.

## Backend Quick Start (FastAPI)

Open a terminal in the `py_server` folder first:

```bash
cd py_server
```

### 1) Create Virtual Environment

#### Windows (PowerShell)

```powershell
python -m venv .venv
```

#### macOS

```bash
python3 -m venv .venv
```

#### Ubuntu

```bash
python3 -m venv .venv
```

### 2) Activate Virtual Environment

#### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

If scripts are blocked, run once in PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

#### macOS

```bash
source .venv/bin/activate
```

#### Ubuntu

```bash
source .venv/bin/activate
```

### 3) Install Python Modules

```bash
pip install -r requirements.txt
```

### 4) Configure Environment

```bash
cp .env.example .env
```

Set these values in `.env`:

- `MONGO_URI`
- `MONGO_DB_NAME`
- `JWT_SECRET_KEY`
- `GOOGLE_CLIENT_ID`

### 5) Run FastAPI Backend

From `py_server` with venv active:

```bash
uvicorn app.main:app --reload
```

For full backend module conventions and API details, see `py_server/README.md`.

