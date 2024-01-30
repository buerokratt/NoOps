import subprocess

def get_container_ports():
    result = subprocess.run(['docker', 'ps', '--format', '{{.ID}} {{.Ports}}'], capture_output=True, text=True)
    if result.returncode == 0:
        container_info = result.stdout.splitlines()
        return container_info
    else:
        raise RuntimeError(f"Error executing 'docker ps' command:\n{result.stderr}")

def check_port_conflicts(container_info):
    used_ports = set()
    conflicts = set()

    for info in container_info:
        container_id, ports_str = info.split(' ', 1)
        ports = ports_str.split(',')
        for port in ports:
            # Extract only the internal port part before the '/'
            internal_port = port.split('/')[0].strip()
            if internal_port:
                internal_port = int(internal_port)
                if internal_port in used_ports:
                    conflicts.add(internal_port)
                else:
                    used_ports.add(internal_port)

    return used_ports, conflicts

def print_port_info(used_ports, conflicts):
    if not used_ports:
        print("No containers are running.")
    else:
        print("Used ports:")
        for port in sorted(used_ports):
            print(f"  {port}")

        if conflicts:
            print("\nPort conflicts detected:")
            for port in conflicts:
                print(f"  Port {port} is used by multiple containers.")
        else:
            print("\nNo port conflicts detected.")

if __name__ == "__main__":
    try:
        container_info = get_container_ports()
        used_ports, conflicts = check_port_conflicts(container_info)
        print_port_info(used_ports, conflicts)
    except Exception as e:
        print(f"Error: {e}")
