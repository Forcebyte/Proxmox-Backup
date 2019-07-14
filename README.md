# Proxmox Backup

### Brief / Overview
This is a pretty basic Python script I wrote to automate backups through jenkins. In general the script attempts to clone itself from a local Gitlab server in my Homelab, executes itself using a Container list, and rotates backups. 

In Jenkins; I have this script running using the following CronJob
```
H 1 * * 0
```
Which will run
```
sudo ssh root@pve.shikata.xyz python < ./Proxmox-Backup.py
```

### General Function

As is, the script does the following
* Grabs a Python script from a local Git (git.shikata.xyz)
* Tabulates each container into a list, parsing for correct Container List format
* Runs a tabbed Proxmox backup command for each container list
* Cleans up older backups such that only x amount of backups exist

### Requirements
- SSH Key access to Proxmox server (Preferrably root)
- Jenkins Server to run job on a timed basis
