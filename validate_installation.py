#!/usr/bin/env python3
import subprocess
import socket

failed = 0

def check_process(desc, cmd):
    global failed
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(f"[✔] {desc}")
    except subprocess.CalledProcessError as e:
        print(f"[✘] {desc}\n    STDERR: {e.output.decode().strip()}")
        failed += 1

def check_port(desc, port):
    global failed
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex(("127.0.0.1", port))
    s.close()
    if result == 0:
        print(f"[✔] {desc}")
    else:
        print(f"[✘] {desc}")
        failed += 1

# Checks
check_process("Apache HTTPD process running", ["pgrep", "httpd"])
check_process("MariaDB process running", ["pgrep", "mariadbd"])
check_port("Port 80 open (Apache)", 80)
check_port("Port 3306 open (MariaDB)", 3306)

print("\nValidation Summary:")
if failed > 0:
    print(f"[✘] {failed} check(s) failed.")
    exit(1)
else:
    print("[✔] All checks passed.")
