# IPventur-Python-Curses
IPventur nmap frontend for Python3 and curses with nmap3 module

This is still beta v4 of IPventur-Python-1.0v4.

Requirements:

Python 3.8 or higher

python3-nmap
git clone https://github.com/wangoloj/python3-nmap.git
"pip3 install python3-nmap"

simplejson
"pip3 install simplejson"

for Windows 10 only
"pip3 install pywin32"

nmap
"sudo apt install nmap"
or
"sudo yum install nmap"


start program (best as root) with: "python IPventur-Python-1.0v4.py"

Open Issues:

1. check for correct IPv4 input format
2. cursor key right not working
3. nmap_os_detection for Windows 10 not working
4. some minor screen issues when you start it on a Windows machine

Note:
goal of the program was to write an easy to use frontend for nmap. Any feedback welcome.

Update v4 version:

- added IP format check
- added if nmap program exist

Still missing:
- ask after a complete scan for a new scan or leaving...
- restart program after wrong entered a wrong IP

