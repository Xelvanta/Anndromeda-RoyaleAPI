# PowerShell Setup Script for Anndromeda RoyaleAPI
$repoUrl = "https://github.com/Xelvanta/Anndromeda-RoyaleAPI.git"
$installPath = Read-Host "Enter the installation path (default: $HOME\Anndromeda-RoyaleAPI)"
if (-not $installPath) {
    $installPath = "$HOME\Anndromeda-RoyaleAPI"  # Default to home directory if no input
}

Write-Host "Setting up Anndromeda RoyaleAPI..." -ForegroundColor Cyan

# Ensure Git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Git is not installed! Please install it from https://git-scm.com/downloads" -ForegroundColor Red
    Pause
    exit 1
}

# Ensure Node.js is installed
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Node.js is not installed! Please install it from https://nodejs.org/en" -ForegroundColor Red
    Pause
    exit 1
}

# Ensure npm is installed
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "[X] npm is not installed! Please install it from https://nodejs.org/en" -ForegroundColor Red
    Pause
    exit 1
}

# Ensure Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Python is not installed! Please install it from https://www.python.org/downloads/" -ForegroundColor Red
    Pause
    exit 1
}

# Ensure pip is installed
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "[X] pip is not installed! Please install it from https://pip.pypa.io/en/stable/installation/" -ForegroundColor Red
    Pause
    exit 1
}

# Clone the repository into Documents
Write-Host "Cloning repository into $installPath..."
if (Test-Path $installPath) {
    Write-Host "[!] Folder already exists! Pulling latest changes..."
    Set-Location $installPath
    git pull
} else {
    git clone $repoUrl $installPath
    Set-Location $installPath
}

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..."
npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth

# Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

Write-Host "[i] Installation complete!"
Write-Host "[i] To start the API, run: cd $installPath && quart run" -ForegroundColor Green
