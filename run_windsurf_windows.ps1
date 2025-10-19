# Windsurf Bypass Tool - All-in-One Script for Windows
# This script downloads, installs, and runs the Windsurf Bypass Tool

Write-Host "🚀 Windsurf Bypass Tool - All-in-One Installer" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check if running on Windows
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "❌ PowerShell version is too old" -ForegroundColor Red
    Write-Host "Please upgrade to PowerShell 5.0 or higher" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PowerShell version is supported" -ForegroundColor Green

# Create installation directory in user's home folder
$installDir = "$env:USERPROFILE\windsurf-bypass-tool"
Write-Host "📁 Installation directory: $installDir" -ForegroundColor Cyan

# Remove existing installation if it exists
if (Test-Path $installDir) {
    Write-Host "🗑️ Removing existing installation..." -ForegroundColor Yellow
    Remove-Item -Path $installDir -Recurse -Force
}

# Download the latest version from GitHub
Write-Host "📥 Downloading Windsurf Bypass Tool..." -ForegroundColor Cyan
git clone https://github.com/black12-ag/windsurf-bypass.git $installDir

# Check if download was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to download the tool" -ForegroundColor Red
    exit 1
}

# Change to installation directory
Set-Location $installDir

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Check if installation was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Installation completed successfully!" -ForegroundColor Green
    
    # Ask user if they want to run the tool now or just install it
    Write-Host ""
    $runNow = Read-Host "Do you want to run the tool now? (y/n)"
    if ($runNow -match "^[Yy]$") {
        Write-Host "🚀 Running Windsurf Bypass Tool..." -ForegroundColor Green
        Write-Host "==================================" -ForegroundColor Green
        python main.py
    } else {
        Write-Host "💡 To run the tool later:" -ForegroundColor Cyan
        Write-Host "   cd $installDir" -ForegroundColor White
        Write-Host "   python main.py" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 To make it even easier, create a batch file with this content:" -ForegroundColor Cyan
        Write-Host "   @echo off" -ForegroundColor White
        Write-Host "   cd /d $installDir" -ForegroundColor White
        Write-Host "   python main.py" -ForegroundColor White
        Write-Host ""
        Write-Host "🌟 Then you can simply run the batch file from anywhere!" -ForegroundColor Green
    }
} else {
    Write-Host "❌ Installation failed" -ForegroundColor Red
    Write-Host "Please check the error messages above" -ForegroundColor Red
    exit 1
}