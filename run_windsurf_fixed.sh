#!/bin/bash

# Windsurf Bypass Tool - All-in-One Script for macOS
# This script downloads, installs, and runs the Windsurf Bypass Tool

echo "🚀 Windsurf Bypass Tool - All-in-One Installer"
echo "============================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS only"
    exit 1
fi

echo "🍎 macOS detected"

# Create installation directory in user's home folder
INSTALL_DIR="$HOME/windsurf-bypass-tool"
echo "📁 Installation directory: $INSTALL_DIR"

# Remove existing installation if it exists
if [ -d "$INSTALL_DIR" ]; then
    echo "🗑️ Removing existing installation..."
    rm -rf "$INSTALL_DIR"
fi

# Download the latest version from GitHub
echo "📥 Downloading Windsurf Bypass Tool..."
git clone https://github.com/black12-ag/windsurf-bypass.git "$INSTALL_DIR"

# Check if download was successful
if [ $? -ne 0 ]; then
    echo "❌ Failed to download the tool"
    exit 1
fi

# Change to installation directory
cd "$INSTALL_DIR"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Installation completed successfully!"
    
    # Ask user if they want to run the tool now or just install it
    echo ""
    read -p "Do you want to run the tool now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Running Windsurf Bypass Tool..."
        echo "=================================="
        python3 main.py
    else
        echo "💡 To run the tool later:"
        echo "   cd $INSTALL_DIR"
        echo "   python3 main.py"
        echo ""
        echo "💡 To make it even easier, add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):" 
        echo "   alias windsurf-bypass='cd $INSTALL_DIR && python3 main.py'"
        echo ""
        echo "🌟 Then you can simply run 'windsurf-bypass' from anywhere!"
    fi
else
    echo "❌ Installation failed"
    echo "Please check the error messages above"
    exit 1
fi