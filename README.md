# Port Knocking App

This is a Python GUI application built with Tkinter to perform Port Knocking. It allows you to define a host (IPv4, IPv6, or domain name) and a series of ports to "knock" in sequence. The application persists your last used configuration.

## Prerequisites

- Python 3.x
- Recommended: Virtual environment

## Setup & Running from Source

1. Clone the repository.
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Compiling as a Standalone Executable

You can compile this application into a standalone executable using [PyInstaller](https://pyinstaller.org/).

### Using the build script (Linux/macOS)

A helper bash script is included:

```bash
./build.sh
```

This script will:
1. Install requirements via `pip`.
2. Run `pyinstaller` to create a bundled app.

The final executable and resources will be located in the `dist/PortKnockingApp/` directory.

### Manual Compilation (Windows/Linux/macOS)

If you are on Windows or prefer to run PyInstaller manually:

```bash
pip install -r requirements.txt
pyinstaller --noconfirm --onedir --windowed --name "PortKnockingApp" "main.py"
```

The resulting executable will be generated inside the `dist/PortKnockingApp` folder.

## File Structure

- `main.py`: Entry point for the application.
- `gui.py`: Contains the Tkinter GUI implementation.
- `knocker.py`: Networking logic for performing the port knocking.
- `storage.py`: Handles saving and loading the configuration payload to the user's data directory.
- `requirements.txt`: Python package dependencies.
- `build.sh`: Bash script to quickly build the application using PyInstaller.
