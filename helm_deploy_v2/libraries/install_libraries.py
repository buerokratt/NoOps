import json
import subprocess
import sys
import os

def install_packages_from_json(filename):
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Construct the full path to the requirements.json file
        json_file_path = os.path.join(script_dir, filename)
        
        # Open and load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: The JSON file is not valid.")
        sys.exit(1)

    # Get the packages list from the loaded data
    packages = data.get('libraries', [])
    
    if not packages:
        print("No packages to install.")
        return
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")

if __name__ == "__main__":
    install_packages_from_json('requirements.json')
