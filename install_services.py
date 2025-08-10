#!/usr/bin/env python3
import subprocess
import time

def run_command(command, description, check=True, background=False):
    """Run a shell command and print status."""
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

def wait_for_port(port, timeout=15):
    """Wait until a given TCP port is open."""
    for _ in range(timeout):
        result = subprocess.run(f"ss -ltn | grep ':{port} '", shell=True, stdout=subprocess.PIPE)
        if result.stdout:
            print(f"[✔] Port {port} is open")
            return True
        time.sleep(1)
    print(f"[✘] Port {port} not open within {timeout} seconds")
    return False

def main():
    # Update system
    run_command("dnf -y update", "Updating system packages")

    # Install Apache (httpd)
    run_command("dnf -y install httpd", "Installing Apache HTTPD")
    run_command("httpd -DFOREGROUND &", "Starting Apache HTTPD", background=True)
    wait_for_port(80)

    # Install MariaDB
    run_command("dnf -y install mariadb-server", "Installing MariaDB server")
    run_command("mysqld_safe --skip-networking=0 &", "Starting MariaDB server", background=True)
    wait_for_port(3306)

    print("\n[✔] Installation completed successfully!")
    print("Apache is running on port 80, MariaDB is running on port 3306.")

if __name__ == "__main__":
    main()
