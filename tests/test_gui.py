import sys
from unittest.mock import MagicMock

# Mock tkinter and validators before importing gui to avoid headless environment errors
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()

import gui

def test_validate_port_entry_valid_ports():
    assert gui.PortKnockingApp.validate_port_entry(None, "80") is True
    assert gui.PortKnockingApp.validate_port_entry(None, "443") is True
    assert gui.PortKnockingApp.validate_port_entry(None, "65535") is True
    assert gui.PortKnockingApp.validate_port_entry(None, "1") is True
    assert gui.PortKnockingApp.validate_port_entry(None, " 80 ") is True

def test_validate_port_entry_empty():
    assert gui.PortKnockingApp.validate_port_entry(None, "") is True

def test_validate_port_entry_invalid_ports():
    assert gui.PortKnockingApp.validate_port_entry(None, "0") is False
    assert gui.PortKnockingApp.validate_port_entry(None, "-1") is False
    assert gui.PortKnockingApp.validate_port_entry(None, "65536") is False

def test_validate_port_entry_non_numeric():
    assert gui.PortKnockingApp.validate_port_entry(None, "abc") is False
    assert gui.PortKnockingApp.validate_port_entry(None, "80a") is False
