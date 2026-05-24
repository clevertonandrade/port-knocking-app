import pytest
import os
import json
import storage

@pytest.fixture
def temp_data_file(tmp_path):
    # Temporarily override DATA_FILE and DATA_FOLDER
    original_folder = storage.DATA_FOLDER
    original_file = storage.DATA_FILE

    test_folder = tmp_path / "test_data"
    test_folder.mkdir()
    test_file = test_folder / "test_data.json"

    storage.DATA_FOLDER = str(test_folder)
    storage.DATA_FILE = str(test_file)

    yield test_file

    # Restore original values
    storage.DATA_FOLDER = original_folder
    storage.DATA_FILE = original_file

def test_load_data_file_not_found(temp_data_file):
    data = storage.load_data()
    assert data == {"host": "", "ports": [""]}

def test_load_data_invalid_json(temp_data_file):
    with open(temp_data_file, "w") as f:
        f.write("{invalid json")

    data = storage.load_data()
    assert data == {"host": "", "ports": [""]}

def test_load_data_not_dict(temp_data_file):
    with open(temp_data_file, "w") as f:
        json.dump(["not", "a", "dict"], f)

    data = storage.load_data()
    assert data == {"host": "", "ports": [""]}

def test_load_data_invalid_host_type(temp_data_file):
    with open(temp_data_file, "w") as f:
        json.dump({"host": 123, "ports": ["80"]}, f)

    data = storage.load_data()
    assert data == {"host": "", "ports": ["80"]}

def test_load_data_invalid_ports_type(temp_data_file):
    with open(temp_data_file, "w") as f:
        json.dump({"host": "localhost", "ports": "not_a_list"}, f)

    data = storage.load_data()
    assert data == {"host": "localhost", "ports": [""]}

def test_load_data_enforce_port_limit(temp_data_file):
    with open(temp_data_file, "w") as f:
        json.dump({"host": "localhost", "ports": [str(i) for i in range(30)]}, f)

    data = storage.load_data()
    assert data["host"] == "localhost"
    assert len(data["ports"]) == 20
    assert data["ports"] == [str(i) for i in range(20)]

def test_get_data_folder_windows(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    monkeypatch.setenv("APPDATA", "C:\\Users\\TestUser\\AppData\\Roaming")
    assert storage.get_data_folder() == os.path.join("C:\\Users\\TestUser\\AppData\\Roaming", "PortKnockingApp")

def test_get_data_folder_darwin(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    original_expanduser = os.path.expanduser
    monkeypatch.setattr("os.path.expanduser", lambda p: "/Users/TestUser/Library/Application Support" if p == "~/Library/Application Support" else original_expanduser(p))
    assert storage.get_data_folder() == os.path.join("/Users/TestUser/Library/Application Support", "PortKnockingApp")

def test_get_data_folder_linux_xdg(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setenv("XDG_CONFIG_HOME", "/home/testuser/.config/custom")
    assert storage.get_data_folder() == os.path.join("/home/testuser/.config/custom", "PortKnockingApp")

def test_get_data_folder_linux_default(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    original_expanduser = os.path.expanduser
    monkeypatch.setattr("os.path.expanduser", lambda p: "/home/testuser/.config" if p == "~/.config" else original_expanduser(p))
    assert storage.get_data_folder() == os.path.join("/home/testuser/.config", "PortKnockingApp")
