# 🚀 Windsurf Bypass Tool

**Cross-platform Python tool for Windsurf AI Editor: Reset machine identity & manage accounts**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/black12-ag/windsurf-bypass)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/black12-ag/windsurf-bypass)
[![License](https://img.shields.io/badge/license-Educational-yellow.svg)](LICENSE.md)

**Author: Munir** | **Customized by Munir - Ready to use!**

---

## 🎯 What is This?

Windsurf Bypass provides tools to manage your Windsurf AI Editor identity:
- 🔄 **Reset Machine ID** - Reset device fingerprint while keeping settings
- ✅ **Register New Account** - Automated account creation with temporary email
- 🔄 **Total Reset** - Complete fresh start (recommended)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (pre-installed on macOS/Linux)
- Git installed
- Admin privileges (recommended)

### Installation

**Windows (PowerShell)**
```powershell
# First Time Installation
git clone https://github.com/black12-ag/windsurf-bypass.git "$env:USERPROFILE\windsurf-bypass"
cd "$env:USERPROFILE\windsurf-bypass"
pip install -r requirements.txt
python main.py

# Already Installed? Run This Instead
cd "$env:USERPROFILE\windsurf-bypass"
git pull
pip install -r requirements.txt --upgrade
python main.py
```

**macOS / Linux**
```bash
# First Time Installation
git clone https://github.com/black12-ag/windsurf-bypass.git ~/windsurf-bypass
cd ~/windsurf-bypass
pip3 install -r requirements.txt
python3 main.py

# Already Installed? Run This Instead
cd ~/windsurf-bypass
git pull
pip3 install -r requirements.txt --upgrade
python3 main.py
```

> **💡 Tip:** If you get "directory already exists" error, use the "Already Installed" commands instead.

---

## 💻 Usage

When you run the tool, you'll see this menu:

```
  ███╗   ███╗██╗   ██╗███╗   ██╗██╗██████╗ 
  ████╗ ████║██║   ██║████╗  ██║██║██╔══██╗
  ██╔████╔██║██║   ██║██╔██╗ ██║██║██████╔╝
  ██║╚██╔╝██║██║   ██║██║╚██╗██║██║██╔══██╗
  ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║██║  ██║
  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝

       Pro Version Activator v1.0.0
              Author: Munir

📋 Available Options:
0. ❌ Exit Program
1. 🔄 Reset Machine ID
2. ✅ Register Windsurf with Custom Email
3. 🔄 Totally Reset Windsurf
```

### What Each Option Does

| Option | What It Does | When to Use |
|--------|--------------|-------------|
| **Option 1** | Reset Machine ID only | Quick reset, keeps settings |
| **Option 2** | Register new account | Need fresh account |
| **Option 3** | Complete reset (BEST) | Full clean slate, **recommended** |

**Recommended:** Use **Option 3** for the best results! 🌟

---

## ✨ Features

### 🎯 Core Functionality
- **🔄 Machine ID Reset** - Instantly reset your Windsurf machine identifiers
- **📧 Smart Registration** - Two registration modes for maximum flexibility
- **🔐 Secure Account Management** - Safe handling of credentials and tokens
- **⚡ Cross-Platform** - Works seamlessly on Windows, macOS, and Linux

### 🎨 Registration Modes

#### 🤖 Automatic Mode
- Fully automated browser control
- Auto-generates temporary email
- Automatic verification code retrieval
- Zero manual intervention required
- Perfect for quick setups

#### 👤 Manual Mode
- Generates temporary email for you
- You control the registration in your browser
- Displays verification code when it arrives
- No browser automation - you're in full control
- Perfect for troubleshooting or custom workflows

---

## 🔧 Troubleshooting

### Common Issues & Quick Fixes

#### **"Python not found"**
**Solution:** Install Python 3.8+ from [python.org](https://www.python.org/downloads/)

#### **"Git not found"**
**Solution:** 
- **Windows:** Install [Git for Windows](https://git-scm.com/download/win)
- **macOS:** Run `xcode-select --install`
- **Linux:** Run `sudo apt install git` or `sudo yum install git`

#### **"Permission denied" (macOS/Linux)**
**Solution:** Run with sudo:
```bash
sudo python3 main.py
```

#### **"Directory already exists"**
**Solution:** Use the "Already Installed" command instead of first-time installation.

#### **"Module not found" error**
**Solution:** Reinstall dependencies:
```bash
pip3 install -r requirements.txt --force-reinstall
```

---

## 📋 System Requirements

| OS | Architecture | Status |
|---|---|---|
| Windows 10/11 | x64, x86 | ✅ Fully Supported |
| macOS 10.15+ | Intel, Apple Silicon | ✅ Fully Supported |
| Linux (Ubuntu, Debian, Arch, etc.) | x64, ARM64 | ✅ Fully Supported |

---

## 📝 Project Structure

```
windsurf-bypass/
├── main.py                      # Main entry point
├── windsurf_register_manual.py  # Registration logic
├── reset_machine_manual.py      # Machine ID reset
├── totally_reset_windsurf.py    # Complete reset
├── simple_tempmail.py           # Temporary email service
├── config.py                    # Configuration management
├── logo.py                      # ASCII art logo
├── locales/                     # Language translations
│   └── en.json
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## ⚠️ Important Notes

- **Educational Purpose Only** - This tool is for educational and research purposes
- **Use Responsibly** - Users are responsible for complying with Windsurf's Terms of Service
- **No Warranty** - Use at your own risk
- **Backup First** - Consider backing up your Windsurf settings before using

---

## 📄 License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

See [LICENSE.md](LICENSE.md) for details.

---

## 🙏 Acknowledgments

- Original project inspiration from the Windsurf community
- All contributors who helped improve this tool
- Users who provided feedback and suggestions
- **Munir** for customization and maintenance of this version

---

<div align="center">

### Made with ❤️ by Munir

**Version 1.0.0** | [GitHub](https://github.com/black12-ag/windsurf-bypass) | [Issues](https://github.com/black12-ag/windsurf-bypass/issues)

⭐ **Star this repo if you find it helpful!** ⭐

**Maintained and Customized by Munir**

</div>
