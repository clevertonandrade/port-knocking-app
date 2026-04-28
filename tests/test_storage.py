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
