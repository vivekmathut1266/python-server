#!/usr/bin/env python3
import subprocess
import time

def run_command(command, description, check=True, background=False):
    print(f"\n[+] {description}...")
    try:
        if background:
            subprocess.Popen(command, shell=True)
        else:
            subprocess.run(command, shell=True, check=check)
        print(f"[✔] {description} completed.")
    except subprocess.CalledProcessError as e:
        print(f"[✘] Error during {description}: {e}")
        if check:
            exit(1)

def wait_for_port(port, timeout=30):
    """Wait until a port is open or timeout reached."""
    for _ in range(timeout):
        result = subprocess.run(
            f"ss -ltn | grep ':{port} '", shell=True, stdout=subprocess.PIPE
        )
        if result.stdout:
            print(f"[✔] Port {port} is open")
            return True
        time.sleep(1)
    print(f"[✘] Port {port} not open within {timeout} seconds")
    return False

def main():
    # Update system
    run_command("dnf -y update", "Updating system packages")

    # Install Apache
    run_command("dnf -y install httpd", "Installing Apache HTTPD")
    run_command("httpd -k start", "Starting Apache HTTPD", background=False)
    wait_for_port(80)

    # Install Redis
    run_command("dnf -y install redis", "Installing Redis server")
    run_command("redis-server --daemonize yes", "Starting Redis server", background=False)
    wait_for_port(6379, timeout=30)

    print("\n[✔] Installation completed successfully!")
    print("Apache is running on port 80, Redis is running on port 6379.")

if __name__ == "__main__":
    main()
