# OSSECUtils
Scripts to enhance and support OSSEC.  Created by Gabriel Bentley and licensed under GPLv3.

TroubledAgentsCheck.py - Script that accepts either disconnected or dead as arguments to generate an email report of disconnected or dead agents (depending on the command line argument).  The SMTP mail configuration is within the script itself, so it is necessary to modify the script after downloading it.

authd-systemd.py - This script is a startup script for the ossec-authd process for Linux systems.  Tested successfully for systemd on Ubuntu 16.04 LTS.
