#!/bin/bash
set -e

echo "Installing requirements..."
pip install -r requirements.txt

echo "Building executable with PyInstaller..."
pyinstaller --noconfirm --onedir --windowed --name "PortKnockingApp" "main.py"

echo "Build complete. Executable can be found in the dist/PortKnockingApp directory."
