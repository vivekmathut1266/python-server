#!/usr/bin/env python3
import subprocess

def run_command(command, description):
    """Run a shell command and print status."""
    print(f"\n[+] {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"[✔] {description} completed.")
    except subprocess.CalledProcessError as e:
        print(f"[✘] Error during {description}: {e}")
        exit(1)

def main():
    # Update system
    run_command("dnf -y update", "Updating system packages")

    # Install Apache (httpd)
    run_command("dnf -y install httpd", "Installing Apache HTTPD")
    run_command("httpd -k start", "Starting Apache HTTPD")

    # Install MySQL (MariaDB is default in AlmaLinux 8)
    run_command("dnf -y install mariadb-server", "Installing MariaDB server")
    run_command("mysqld_safe --skip-networking=0 &", "Starting MariaDB server")

    # Firewall settings (optional — firewalld may not be running in CI)
    try:
        run_command("firewall-cmd --permanent --add-service=http", "Opening HTTP port in firewall")
        run_command("firewall-cmd --permanent --add-service=https", "Opening HTTPS port in firewall")
        run_command("firewall-cmd --reload", "Reloading firewall rules")
    except SystemExit:
        print("[!] Skipping firewall config — likely not running in CI environment.")

    print("\n[✔] Installation completed successfully!")
    print("Apache is running on port 80, MariaDB is running on port 3306.")

if __name__ == "__main__":
    main()
