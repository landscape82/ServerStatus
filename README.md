# Server Status

## Summary

GUI tool to check the SSH status of many Linux servers at once with diagnostic information. Written in Python 2.

## Description

This GUI program takes a list of servers to check from servers_to_check.py. Copy servers_to_check.py.sample to
servers_to_check.py and fill with your own servers. Use a label and a hostname.

Click "Check All" and it will create an SSH connection to each server.

During the check the labels will appear yellow. They will turn green or red when finished.

You can click on any label and it will open a new window with server information.

It uses your ~/.ssh/id_rsa.pub key to authenticate. It should? use your ~/.ssh/config

It ignores unknown remote hosts and auto adds key as known host.

These are some of the command it returns:

- uptime
- users
- uname -a
- w
- who
- df -h
- cat /etc/hosts
- free -h
- iostat
- vmstat
- last
- ps aux
- vmstat -stats
- netstat -l
- netstat -t
- netstat -u
- netstat -x
- lscpu
- ls ~

## Screenshots

Server list after starting the program

![Server List](/screenshots/server_status1.png "Server List")

Servers turning green after connecting with "Check All"

![Server Check](/screenshots/server_status2.png "Server Check")

Server details after clicking on the name label

![Server Details](/screenshots/server_status3.png "Server Details")

## Contact

nanodano@devdungeon.com

www.devdungeon.com