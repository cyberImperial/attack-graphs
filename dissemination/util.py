import socket

def get_host_ip():
    """Bind the process to a socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    ip = s.getsockname()[0]
    s.close()

    return ip
