import pytest
import socket
from unittest.mock import patch
import knocker

def test_perform_port_knocking_success():
    with patch("socket.create_connection") as mock_conn:
        # Mock successful connections
        mock_conn.return_value = True

        result = knocker.perform_port_knocking("127.0.0.1", [80, 443])

        assert result is True
        assert mock_conn.call_count == 2
        mock_conn.assert_any_call(("127.0.0.1", 80), timeout=0.01)
        mock_conn.assert_any_call(("127.0.0.1", 443), timeout=0.01)

def test_perform_port_knocking_timeout():
    with patch("socket.create_connection") as mock_conn:
        # Mock connection timeouts (typical for port knocking)
        mock_conn.side_effect = socket.timeout

        result = knocker.perform_port_knocking("127.0.0.1", [80, 443])

        assert result is True
        assert mock_conn.call_count == 2

def test_perform_port_knocking_exception():
    with patch("socket.create_connection") as mock_conn:
        # Mock broader exception
        mock_conn.side_effect = Exception("General error")

        result = knocker.perform_port_knocking("127.0.0.1", [80, 443])

        assert result is False
        assert mock_conn.call_count == 1  # Fails on the first try
