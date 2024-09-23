import yaml
import sys
import os
import re

def is_valid_password(password):
    """Check if the password meets the requirements."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # Check for at least one capital letter
        return False
    if not re.search(r"\d", password):  # Check for at least one number
        return False
    return True

def replace_placeholders(yaml_content, replacements):
    """Replace placeholders in the YAML content with actual values from replacements."""
    changes_made = False
    for placeholder, actual_value in replacements.items():
        # Validate password if the placeholder contains '.password'
        if '.password' in placeholder and not is_valid_password(actual_value):
            print(f"Error: The password for '{placeholder}' does not meet the complexity requirements.")
            sys.exit(1)

        # Convert actual_value to string if it's not already
        if not isinstance(actual_value, str):
            actual_value = yaml.dump(actual_value).strip()

        new_content = yaml_content.replace(f"{{{{ {placeholder} }}}}", actual_value)
        if new_content != yaml_content:
            changes_made = True
            yaml_content = new_content

    return yaml_content, changes_made

def load_yaml(file_path):
    """Load a YAML file and return its content."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error reading the file {file_path}: {e}")
            sys.exit(1)

def find_files(directories):
    """Find all 'values.yaml' files and files with 'configmap' in their filename under the given list of directories."""
    target_files = []
    for base_dir in directories:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                # Look for 'values.yaml' files
                if file == "values.yaml":
                    target_files.append(os.path.join(root, file))
                # Look for files containing 'configmap' in their filename inside the /templates folder
                if "configmap" in file.lower() and file.endswith(".yaml") and "templates" in root.lower():
                    target_files.append(os.path.join(root, file))
                if "deployment" in file.lower() and file.endswith(".yaml") and "templates" in root.lower():
                    target_files.append(os.path.join(root, file))
                if "ingress" in file.lower() and file.endswith(".yaml") and "templates" in root.lower():
                    target_files.append(os.path.join(root, file))
                if "pv" in file.lower() and file.endswith(".yaml") and "templates" in root.lower():
                    target_files.append(os.path.join(root, file))
                if "job" in file.lower() and file.endswith(".yaml") and "templates" in root.lower():
                    target_files.append(os.path.join(root, file))
                if "modules" in file.lower() and file.endswith(".yaml"):
                    target_files.append(os.path.join(root, file))
                if "components" in file.lower() and file.endswith(".yaml"):
                    target_files.append(os.path.join(root, file))
                if "post-deploy" in file.lower() and file.endswith(".yaml"):
                    target_files.append(os.path.join(root, file))
    return target_files

def main():
    if len(sys.argv) != 2:
        print("Usage: python secrets.py <passwords_file>")
        sys.exit(1)

    passwords_file = sys.argv[1]
    passwords = load_yaml(passwords_file)

    # Directories to check for values.yaml and configmap files
    directories = [
        "./NoOps/Kubernetes/Components", 
        "./NoOps/Kubernetes/Modules", 
        "./NoOps/Kubernetes/Post-deploy",
        "./"
    ]

    target_files = find_files(directories)

    any_changes = False

    for target_file in target_files:
        print(f"Processing {target_file}...")

        # Load the YAML file
        with open(target_file, 'r') as tf:
            yaml_content = tf.read()

        # Replace placeholders with actual secrets
        updated_content, changes_made = replace_placeholders(yaml_content, passwords)

        if changes_made:
            with open(target_file, 'w') as tf:
                tf.write(updated_content)
            print(f"Updated {target_file} with values from {passwords_file}\n")
            any_changes = True
        else:
            print(f"No changes needed for {target_file}, skipping...\n")

    if not any_changes:
        print("No changes were made in any of the files.")

if __name__ == "__main__":
    main()
