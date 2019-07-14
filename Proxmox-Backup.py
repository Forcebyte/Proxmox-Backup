#!/usr/bin/env python
import os
import glob
import subprocess

#Git Clone this repository and CD into said repo to grab the filelist
git_fetch = subprocess.call(["git", "clone","http://git.shikata.xyz:3000/root/Proxmox-Backup.git"])

#Get lines of the Git Script to parse through Container List
try:
    ImportFile = open("./Proxmox-Backup/Container-List.txt",'r')
except IOError:
    print("Error: File not found!")
    exit(1)
except IndexError:
    print("Error: No Argument Given")
    exit(1)
ImportFile_Lines = ImportFile.read().splitlines()
ImportFile.close()

#Ensure that we remove all lines that are commented out
Uncommented_ImportFile = []
for line in ImportFile_Lines:
    if "#" not in line:
        Uncommented_ImportFile.append(line)

#Add the CT-ID to use in the command
Filtered_ImportFile = []
for line in Uncommented_ImportFile:
    Filtered_ImportFile.append(line[:3])

#Remove each previous Proxmox container backup
for container in Filtered_ImportFile:
    filename = "/var/lib/vz/dump/vzdump-lxc-" + str(container) + "*"
    for file in glob.glob(filename):
        os.remove(file)

#Grab each Proxmox Container ID from the list - backup each portion
# --remove 1 specifies the maximum amount of backups allowed
for container in Filtered_ImportFile:
    backupcmd = subprocess.call(["vzdump", str(container), "--mode" ,"snapshot", "--compress", "lzo", "--node", "pve", "--storage", "local", "--remove", "1"])
    if backupcmd == 0:
        print("Backup of Container ID " + str(container) + " successful!")
    else:
        print("Error Backing up Container - see syslog for details")

#Remove Git Repo after execution
git_remove = subprocess.call(["rm", "-rf", "Proxmox-Backup"])
if git_remove == 0:
    print("Git Repo Removal Successful!")
else:
    print("Error Restarting DNS Service")