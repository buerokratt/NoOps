import subprocess

def run_playbooks(playbooks):
    # Iterate through the playbooks and run them one by one
    for playbook in playbooks:
        ansible_command = f"ansible-playbook {playbook} -i inventory.yml"
        result = subprocess.run(ansible_command, shell=True, capture_output=True, text=True)
        
        # Check if the playbook execution was successful
        if result.returncode == 0:
            print(f"Playbook {playbook} executed successfully.")
        else:
            print(f"Error running playbook {playbook}:")
            print(result.stdout)
            print(result.stderr)

# List of playbook files to run
playbooks = ["resources.yml"]
# Run the playbooks
run_playbooks(playbooks)
