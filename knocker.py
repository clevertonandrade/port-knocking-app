import socket

def perform_port_knocking(host, ports):
    """
    Attempts to connect to a list of ports on the given host.
    Returns True if the process completed successfully (even if individual ports timeout, as is typical for port knocking),
    and False if a broader exception occurs.
    """
    try:
        for port in ports:
            try:
                socket.create_connection((host, port), timeout=0.01)
            except socket.timeout:
                continue
        return True
    except Exception:
        return False
