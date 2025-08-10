#!/usr/bin/env python3
import subprocess
import sys

def check_command(command, description):
    """Run a shell command and return True if it succeeds."""
    print(f"[+] {description}...")
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f"[✔] {description}")
        return True
    else:
        print(f"[✘] {description}")
        if result.stdout:
            print("    STDOUT:", result.stdout.decode().strip())
        if result.stderr:
            print("    STDERR:", result.stderr.decode().strip())
        return False

def main():
    failures = 0

    # 1. Check Apache installation
    if not check_command("rpm -q httpd", "Apache HTTPD installed"):
        failures += 1

    # 2. Check MariaDB installation
    if not check_command("rpm -q mariadb-server", "MariaDB installed"):
        failures += 1

    # 3. Check Apache running
    if not check_command("pgrep httpd", "Apache HTTPD process running"):
        failures += 1

    # 4. Check MariaDB running
    if not check_command("pgrep mysqld", "MariaDB process running"):
        failures += 1

    # 5. Check firewall rules for HTTP
    if not check_command("firewall-cmd --list-all | grep -q 'services:.*http'", "Firewall allows HTTP"):
        failures += 1

    # 6. Check firewall rules for HTTPS
    if not check_command("firewall-cmd --list-all | grep -q 'services:.*https'", "Firewall allows HTTPS"):
        failures += 1

    # 7. Check if Apache port 80 is listening
    if not check_command("ss -tuln | grep -q ':80 '", "Port 80 open (Apache)"):
        failures += 1

    # 8. Check if MariaDB port 3306 is listening
    if not check_command("ss -tuln | grep -q ':3306 '", "Port 3306 open (MariaDB)"):
        failures += 1

    print("\nValidation Summary:")
    if failures == 0:
        print("[✔] All checks passed successfully!")
    else:
        print(f"[✘] {failures} check(s) failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
