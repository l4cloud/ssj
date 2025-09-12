import subprocess

def test_connection(host):
    """
    Tests the connectivity of a host using a non-interactive SSH command.

    Args:
        host: The hostname or IP address of the server to test.

    Returns:
        True if the connection is successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", host, "exit"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
