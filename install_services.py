#!/usr/bin/env python3
import subprocess
import time

def run_command(command, description, check=True):
    """Run a shell command and print status."""
    print(f"\n[+] {description}...")
    try:
        subprocess.run(command, shell=True, check=check)
        print(f"[✔] {description} completed.")
    except subprocess.CalledProcessError as e:
        print(f"[✘] Error during {description}: {e}")
        if check:
            exit(1)

def wait_for_service(process_name, timeout=15):
    """Wait until a given process name is running."""
    for _ in range(timeout):
        result = subprocess.run(f"pgrep {process_name}", shell=True, stdout=subprocess.PIPE)
        if result.stdout:
            print(f"[✔] {process_name} is running")
            return True
        time.sleep(1)
    print(f"[✘] {process_name} did not start within {timeout} seconds")
    return False

def main():
    # Update system
    run_command("dnf -y update", "Updating system packages")

    # Install Apache (httpd)
    run_command("dnf -y install httpd", "Installing Apache HTTPD")
    run_command("systemctl enable --now httpd", "Starting Apache HTTPD")
    wait_for_service("httpd")

    # Install MariaDB
    run_command("dnf -y install mariadb-server", "Installing MariaDB server")
    run_command("systemctl enable --now mariadb", "Starting MariaDB server")
    wait_for_service("mariadbd") or wait_for_service("mysqld")

    # Firewall settings
    run_command("systemctl enable --now firewalld", "Starting firewalld service", check=False)
    run_command("firewall-cmd --permanent --add-service=http", "Opening HTTP port in firewall", check=False)
    run_command("firewall-cmd --permanent --add-service=https", "Opening HTTPS port in firewall", check=False)
    run_command("firewall-cmd --reload", "Reloading firewall rules", check=False)

    print("\n[✔] Installation completed successfully!")
    print("Apache is running on port 80, MariaDB is running on port 3306.")

if __name__ == "__main__":
    main()
