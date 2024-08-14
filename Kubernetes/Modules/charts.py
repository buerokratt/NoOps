#!/usr/bin/env python3
import os
import shutil
import yaml

# Function to update version in Chart.yaml
def update_version(chart_dir, version):
    chart_file = os.path.join(chart_dir, "Chart.yaml")
    if os.path.exists(chart_file):
        # Read the current version from the Chart.yaml file
        with open(chart_file, "r") as f:
            lines = f.readlines()
        
        current_version = None
        for line in lines:
            if line.startswith("version:"):
                current_version = line.strip().split(": ")[1]
                break
        
        # If version is not found, do not update
        if current_version is None:
            print(f"Version not found in {chart_file}. Skipping update.")
            return
        
        # Check if the current version matches the new version
        if current_version == version:
            print(f"Version in {chart_file} is already {version}. Skipping update.")
            return
        
        # Update the version
        with open(chart_file, "w") as f:
            for line in lines:
                if line.startswith("version:"):
                    f.write(f"version: {version}\n")
                else:
                    f.write(line)
        print(f"Updated version in {chart_file} to {version}")
    else:
        print(f"Chart.yaml not found in {chart_dir}")

# Function to get expected tarball filenames
def get_expected_tarballs(chart_dirs, chart_versions):
    expected_tarballs = []
    for chart_dir in chart_dirs:
        version = chart_versions.get(chart_dir)
        expected_tarball = f"{chart_dir}-{version}.tgz"
        expected_tarballs.append(expected_tarball)
    return expected_tarballs

# Function to package chart
def package_chart(chart_dir, version, expected_tarballs):
    base_dir = "./"
    full_chart_dir = os.path.join(base_dir, chart_dir)
    tarball = os.path.join(base_dir, "charts", f"{chart_dir}-{version}.tgz")
    if tarball in expected_tarballs:
        print(f"Tarball {chart_dir}-{version}.tgz already exists. Skipping packaging.")
    else:
        print(f"Packaging {chart_dir}...")
        shutil.make_archive(tarball[:-4], "gztar", full_chart_dir)
        print(f"Successfully packaged chart and saved it to: {tarball}")

# Main script
def main():
    chart_versions_file = "./chart_versions.yml"
    with open(chart_versions_file, "r") as f:
        CHART_VERSIONS = yaml.safe_load(f)
    
    # Update versions
    for chart_dir, version in CHART_VERSIONS.items():
        update_version(chart_dir, version)
    
    print("Version updated in all Chart.yaml files")
    
    # Get expected tarball filenames
    CHART_DIRS = [
        "Buerokratt-Chatbot",
        "Training-Module",
        "Service-Module",
        "Analytics-Module",
        "Authentication-Layer",
        "Widget"
    ]
    expected_tarballs = get_expected_tarballs(CHART_DIRS, CHART_VERSIONS)
    
    # Package charts
    for chart_dir in CHART_DIRS:
        version = CHART_VERSIONS.get(chart_dir)
        package_chart(chart_dir, version, expected_tarballs)
    
    print("All charts packaged successfully!")

if __name__ == "__main__":
    main()
