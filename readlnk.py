#!/usr/bin/env python3

# DEPENDENCIES
# pip3 install LnkParse3

import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(__file__), "readlnk"))
import LnkParse3
import subprocess
import re

def open_file(filename):
	if sys.platform == "win32":
		print("opening "+filename+" on startfile (win32)")
		os.startfile(filename)
	else:
		opener ="open" if sys.platform == "darwin" else "xdg-open"
		print("opening "+filename+" on subprocess: " + opener)
		subprocess.call([opener, filename])


if len(sys.argv) < 2 or len(sys.argv) > 2:
	print("Usage:  lnkread.py linkfile.lnk")
	sys.exit(0)
    
indata = open(sys.argv[1], 'rb')
x = LnkParse3.lnk_file(indata)

sourcedirectory = os.path.dirname(os.path.realpath(sys.argv[1])) 

# --- GET TARGET

target = x.get_command()

if not target: # Might be samba link or something like that
	target = x.extraBlocks['ENVIRONMENTAL_VARIABLES_LOCATION_BLOCK']['target_unicode']
	
# --- REPLACE PATH SYNTAX AND DEFINITIONS

target = target.replace("\\\\", "smb://")

target = target.replace("\\", "/") # Replace backslash with forwardslash
target = target.replace("C:", "")

# --- OPEN TARGET

if (target.startswith("smb")):
	print("appears to be samba link: "+target)
	subprocess.Popen(['xdg-open', target])
else:
	subprocess.Popen(['xdg-open', target], cwd=sourcedirectory)

print(sourcedirectory+" -> "+target)
