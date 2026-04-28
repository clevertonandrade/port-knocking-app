import os
import json
import platform

def get_data_folder():
    if platform.system() == "Windows":
        base_dir = os.getenv("APPDATA")
    elif platform.system() == "Darwin":
        base_dir = os.path.expanduser("~/Library/Application Support")
    else:
        base_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))

    if not base_dir:
        base_dir = os.path.expanduser("~")

    return os.path.join(base_dir, "PortKnockingApp")

DATA_FOLDER = get_data_folder()
DATA_FILE = os.path.join(DATA_FOLDER, "port_knocking_data.json")

def save_data(host, ports):
    data = {"host": host, "ports": ports}

    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            data = {"host": "", "ports": [""]}

        if "host" not in data or not isinstance(data["host"], str):
            data["host"] = ""

        if "ports" not in data or not isinstance(data["ports"], list):
            data["ports"] = [""]
        else:
            data["ports"] = [str(p) for p in data["ports"]][:20]

    except (FileNotFoundError, json.JSONDecodeError):
        data = {"host": "", "ports": [""]}
    return data
