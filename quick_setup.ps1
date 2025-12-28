# Windows Quick Setup for Shopina (Frontend + Backend)
# - Initializes submodules
# - Sets up Python venv, installs backend deps, runs migrations
# - Installs frontend deps
# - Launches backend and frontend in separate PowerShell windows

$ErrorActionPreference = "Stop"

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[OK]   $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "[ERR]  $msg" -ForegroundColor Red }

$root     = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend  = Join-Path $root "code source\shopina-env\backend"
$frontend = Join-Path $root "code source\front"

Write-Info "Root: $root"
Write-Info "Backend: $backend"
Write-Info "Frontend: $frontend"

# 1) Submodules
Write-Info "Updating submodules (frontend)"
try {
    Push-Location $root
    git submodule update --init --recursive | Out-Null
    Pop-Location
    Write-Ok "Submodules ready"
} catch {
    Write-Warn "Submodule update failed: $_"
}

# 2) Backend setup
Write-Info "Setting up backend (Python venv, deps, migrations)"

$venvDir  = Join-Path $backend ".venv"
$pyExe    = Join-Path $venvDir "Scripts\python.exe"

# Ensure venv
if (-not (Test-Path $pyExe)) {
    Write-Info "Creating Python venv at $venvDir"
    Push-Location $backend
    python -m venv .venv
    Pop-Location
} else {
    Write-Info "Python venv already exists"
}

# Install requirements
Write-Info "Installing backend requirements"
Push-Location $backend
& $pyExe -m pip install --upgrade pip
& $pyExe -m pip install -r (Join-Path $backend "requirements.txt")

# Migrations
Write-Info "Applying migrations"
& $pyExe (Join-Path $backend "manage.py") migrate
Pop-Location
Write-Ok "Backend ready"

# 3) Frontend setup
Write-Info "Setting up frontend (npm deps)"
Push-Location $frontend

# Ensure .env.local
$envLocal = Join-Path $frontend ".env.local"
if (-not (Test-Path $envLocal)) {
    Write-Info "Creating .env.local"
    "VITE_API_URL=http://localhost:8000/api" | Out-File -Encoding UTF8 $envLocal
}

npm install
Pop-Location
Write-Ok "Frontend deps installed"

# 4) Launch servers in separate windows
Write-Info "Starting backend server (new window)"
Start-Process -FilePath "powershell" -WorkingDirectory $backend -ArgumentList (
    "-NoExit -Command `"& `"""$pyExe""" manage.py runserver`""
)

Write-Info "Starting frontend dev server (new window)"
Start-Process -FilePath "powershell" -WorkingDirectory $frontend -ArgumentList (
    "-NoExit -Command `"npm run dev`""
)

Write-Ok "All set! Backend at http://127.0.0.1:8000, Frontend at http://localhost:3000"