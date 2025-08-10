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
    run_command("systemctl enable --now httpd", "Enabling & starting Apache service")

    # Install MySQL (MariaDB)
    run_command("dnf -y install mariadb-server", "Installing MariaDB server")
    run_command("systemctl enable --now mariadb", "Enabling & starting MariaDB service")

    # Firewall settings
    run_command("firewall-cmd --permanent --add-service=http", "Opening HTTP port in firewall")
    run_command("firewall-cmd --permanent --add-service=https", "Opening HTTPS port in firewall")
    run_command("firewall-cmd --reload", "Reloading firewall rules")

    print("\n[✔] Installation completed successfully!")
    print("Run 'mysql_secure_installation' to secure the database.")

if __name__ == "__main__":
    main()
