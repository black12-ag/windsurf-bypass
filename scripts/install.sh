#!/bin/bash

# Windsurf Bypass Tool Installation Script for macOS/Linux

echo "🚀 Windsurf Bypass Tool Installation"
echo "====================================="

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 macOS detected"
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Linux detected"
    OS="Linux"
else
    echo "❌ Unsupported operating system"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

echo "✅ Python 3 found"

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$PYTHON_VERSION < 3.8" | bc -l) -eq 1 ]]; then
    echo "❌ Python version $PYTHON_VERSION is too old"
    echo "Please upgrade to Python 3.8 or higher"
    exit 1
fi

echo "✅ Python version $PYTHON_VERSION is supported"

# Create installation directory
INSTALL_DIR="$HOME/windsurf-bypass-tool"
echo "📁 Creating installation directory: $INSTALL_DIR"
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Download the latest version from GitHub
echo "📥 Downloading Windsurf Bypass Tool..."
if command -v git &> /dev/null; then
    # Use git if available
    git clone https://github.com/black12-ag/windsurf-bypass.git "$INSTALL_DIR"
else
    # Fallback to curl if git is not available
    echo "⚠️ Git not found, using curl for download"
    curl -fsSL https://github.com/black12-ag/windsurf-bypass/archive/main.tar.gz | tar -xz -C "$INSTALL_DIR" --strip-components=1
fi

# Change to installation directory
cd "$INSTALL_DIR"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Installation completed successfully!"
    echo ""
    echo "📝 To run the tool:"
    echo "   cd $INSTALL_DIR"
    echo "   python3 main.py"
    echo ""
    echo "💡 For easy access, add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
    echo "   alias windsurf-bypass='cd $INSTALL_DIR && python3 main.py'"
    echo ""
    echo "🌟 Enjoy using Windsurf Bypass Tool!"
else
    echo "❌ Installation failed"
    echo "Please check the error messages above and try again"
    exit 1
fi