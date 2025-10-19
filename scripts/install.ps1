# Windsurf Bypass Tool Installation Script for Windows

Write-Host "🚀 Windsurf Bypass Tool Installation" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if running on Windows
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "❌ PowerShell version is too old" -ForegroundColor Red
    Write-Host "Please upgrade to PowerShell 5.0 or higher" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PowerShell version is supported" -ForegroundColor Green

# Check if Python is installed
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher and try again" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python found" -ForegroundColor Green

# Check Python version
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python ([0-9]+)\.([0-9]+)") {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "❌ Python version $major.$minor is too old" -ForegroundColor Red
        Write-Host "Please upgrade to Python 3.8 or higher" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Python version $major.$minor is supported" -ForegroundColor Green
} else {
    Write-Host "⚠️ Could not determine Python version, continuing anyway..." -ForegroundColor Yellow
}

# Create installation directory
$installDir = "$env:USERPROFILE\windsurf-bypass-tool"
Write-Host "📁 Creating installation directory: $installDir" -ForegroundColor Cyan
if (Test-Path $installDir) {
    Remove-Item -Path $installDir -Recurse -Force
}
New-Item -ItemType Directory -Path $installDir | Out-Null

# Change to installation directory
Set-Location $installDir

# Download the latest version from GitHub
Write-Host "📥 Downloading Windsurf Bypass Tool..." -ForegroundColor Cyan

# Check if git is available
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if ($gitCmd) {
    # Use git if available
    git clone https://github.com/black12-ag/windsurf-bypass-tool.git .
} else {
    # Fallback to direct download if git is not available
    Write-Host "⚠️ Git not found, using direct download" -ForegroundColor Yellow
    # This would require implementing a fallback method for downloading without git
    Write-Host "❌ Git is required for Windows installation" -ForegroundColor Red
    Write-Host "Please install Git for Windows and try again" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Check if installation was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Installation completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 To run the tool:" -ForegroundColor Cyan
    Write-Host "   cd $installDir" -ForegroundColor White
    Write-Host "   python main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 For easy access, create a batch file with this content:" -ForegroundColor Cyan
    Write-Host "   @echo off" -ForegroundColor White
    Write-Host "   cd /d $installDir" -ForegroundColor White
    Write-Host "   python main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "🌟 Enjoy using Windsurf Bypass Tool!" -ForegroundColor Green
} else {
    Write-Host "❌ Installation failed" -ForegroundColor Red
    Write-Host "Please check the error messages above and try again" -ForegroundColor Red
    exit 1
}