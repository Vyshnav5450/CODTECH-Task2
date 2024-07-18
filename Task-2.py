import nmap
import requests
from packaging import version

# Function to scan for open ports
def scan_open_ports(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024')  # Scan ports from 1 to 1024
    open_ports = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                if nm[host][proto][port]['state'] == 'open':
                    open_ports.append(port)
    return open_ports

# Function to check software versions
def check_software_versions(url):
    response = requests.get(url)
    headers = response.headers
    server_info = headers.get('Server', '')
    if server_info:
        return server_info
    return "Unknown"

# Function to check for outdated software
def is_outdated(software_version, latest_version):
    return version.parse(software_version) < version.parse(latest_version)

# Example usage
if __name__ == "__main__":
    target = input("Enter the target IP or URL: ")

    # Scan for open ports
    print("Scanning for open ports...")
    open_ports = scan_open_ports(target)
    if open_ports:
        print(f"Open ports: {open_ports}")
    else:
        print("No open ports found.")

    # Check software versions
    print("Checking software versions...")
    software_info = check_software_versions(f"http://{target}")
    print(f"Software info: {software_info}")

    # Example check for outdated software
    # This would usually be done by comparing against a known database of software versions
    if "Apache" in software_info:
        current_version = software_info.split('/')[1]
        latest_version = "2.4.48"  # Example latest version
        if is_outdated(current_version, latest_version):
            print(f"The software {software_info} is outdated. Please update to {latest_version}.")
        else:
            print(f"The software {software_info} is up-to-date.")
    else:
        print("Could not determine if software is outdated.")

    
