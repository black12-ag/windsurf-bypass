#!/bin/bash
# One-liner script to download, install, and run Windsurf Bypass Tool on Linux

git clone https://github.com/black12-ag/windsurf-bypass.git "$HOME/windsurf-bypass-tool" && cd "$HOME/windsurf-bypass-tool" && pip3 install -r requirements.txt && python3 main.py