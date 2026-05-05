# This file is designed to fix a problem in WSL/Ubuntu when setting up Podman Networks

import argparse
import fileinput
import re
import platform

def replace_cniversion(line, old_version, new_version):
    match = re.search(r"\bcniVersion\b", line)
    if match:
        return line.replace(old_version, new_version)
    return line

def main():
    parser = argparse.ArgumentParser(description="Replace CNI version in a file.")
    parser.add_argument("file", help="The file to modify")
    parser.add_argument("--old-version", default="1.0.0", help="Old version to replace")
    parser.add_argument("--new-version", default="0.4.0", help="New version to replace with")
    args = parser.parse_args()

    with fileinput.input(files=args.file, inplace=True) as f:
        for line in f:
            new_line = replace_cniversion(line, args.old_version, args.new_version)
            print(new_line, end='')

if __name__ == "__main__":
    if (platform.system() == 'Linux') and ('WSL' in platform.uname().release):
        print ('Detected that the current machine is wsl, fixing cni version')
        main()
    else:
        print('WSL not detected, skipping cni version')

