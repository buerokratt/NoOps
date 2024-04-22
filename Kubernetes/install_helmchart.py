import os
import subprocess
from time import sleep
from releasenames import releasenames

def install_helm_charts(root_path, namespace):
    print("Starting Helm chart installation process...")
    for category in ["Modules", "Components", "Post-deploy"]:
        for release_name, directory_name in releasenames.items():
            if directory_name in category:
                chart_path = os.path.join(root_path, directory_name, "charts")
                values_yaml = os.path.join(root_path, directory_name, "values.yaml")
                print(f"Installing {release_name} from {chart_path}...")
                print(f"Command: helm install {release_name} {chart_path} -n {namespace} -f {values_yaml}")
                process = subprocess.Popen(f"helm install {release_name} {chart_path} -n {namespace} -f {values_yaml}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while True:
                    output = process.stdout.readline().decode().strip()
                    if not output and process.poll() is not None:
                        break
                    if output:
                        print(output)
                if process.poll() != 0:
                    print(f"Installation of {release_name} failed with exit code {process.poll()}")
                    return
                # Add a delay after installing the "pipeline" release in the "Post-deploy" category
                if category == "Post-deploy" and release_name == "pipeline":
                    print("Waiting for 5 minutes before installing the next release...")
                    sleep(300)
                # Add a delay after installing the last release in the "Modules" category
                if category == "Modules" and release_name == list(releasenames.keys())[-1]:
                    print("Waiting for 4 minutes before installing components...")
                    sleep(240)
    print("Helm chart installation process completed.")

if __name__ == "__main__":
    root_path = "./Buerokratt-NoOps/Kubernetes"
    namespace = "byrokratt"
    install_helm_charts(root_path, namespace)
