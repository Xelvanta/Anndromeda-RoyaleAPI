# PowerShell Setup Script for Anndromeda RoyaleAPI
$repoUrl = "https://github.com/Xelvanta/Anndromeda-RoyaleAPI.git"
$installPath = Read-Host "Enter the installation path (default: $HOME\Anndromeda-RoyaleAPI)"
if (-not $installPath) {
    $installPath = "$HOME\Anndromeda-RoyaleAPI"  # Default to home directory if no input
}

Write-Host "Setting up Anndromeda RoyaleAPI..." -ForegroundColor Cyan

# Initialize flag to track if any program is missing
$allInstalled = $true

# Ensure Git is installed and check version
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Git is not installed! Please install it from https://git-scm.com/downloads" -ForegroundColor Red
    $allInstalled = $false
} else {
    $gitVersion = git --version
    Write-Host "[i] Git is installed: $gitVersion" -ForegroundColor Green
}

# Ensure Node.js is installed and check version
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Node.js is not installed! Please install it from https://nodejs.org/en" -ForegroundColor Red
    $allInstalled = $false
} else {
    $nodeVersion = node --version
    Write-Host "[i] Node.js is installed: $nodeVersion" -ForegroundColor Green
}

# Ensure npm is installed and check version
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "[X] npm is not installed! Please install it from https://nodejs.org/en" -ForegroundColor Red
    $allInstalled = $false
} else {
    $npmVersion = npm --version
    Write-Host "[i] npm is installed: $npmVersion" -ForegroundColor Green
}

# Ensure Python is installed and check version
try {
    # This handles 'python' being a valid shortcut even if not installed
    $pythonVersion = & python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
        Write-Host "[i] Python is installed: $($matches[0])" -ForegroundColor Green
    } else {
        Write-Host "[X] Python is not installed! Please install it from https://www.python.org/downloads/" -ForegroundColor Red
        $allInstalled = $false
    }
} catch {
    # This handles the case where 'python' isn't recognized
    Write-Host "[X] Python is not installed! Please install it from https://www.python.org/downloads/" -ForegroundColor Red
    $allInstalled = $false
}

# Ensure pip is installed and check version
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "[X] pip is not installed! Please install it from https://pip.pypa.io/en/stable/installation/" -ForegroundColor Red
    $allInstalled = $false
} else {
    $pipVersion = pip --version
    Write-Host "[i] pip is installed: $pipVersion" -ForegroundColor Green
}

# If any program is missing, indicate that the installation is incomplete
if (-not $allInstalled) {
    Write-Host "[X] Some programs are missing or not installed correctly. Please follow the instructions above to install them." -ForegroundColor Red
    exit 1
} else {
    Write-Host "[i] All programs are installed correctly!" -ForegroundColor Green
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
