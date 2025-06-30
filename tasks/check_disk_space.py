import subprocess


def main():
    """Return disk usage information via `df -h`."""
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()
