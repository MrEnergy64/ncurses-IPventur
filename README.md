# IPventur-Python-Curses
IPventur nmap frontend for Python3 and curses with nmap3 module

This is v5 of ncurses-IPventur-10v5.py

Requirements:

Python 3.8 or higher

python3-nmap:

git clone https://github.com/wangoloj/python3-nmap.git

for Windows:

"pip3 install -r requirements-win.txt"


for Linux:

"pip3 install -r requirements-linux.txt"


nmap:

"sudo apt install nmap"
or:
"sudo yum install nmap"


start program (best as root) with: "python ncurses-IPventur-10v5.py"

Note:
goal of the program was to write an easy to use frontend for nmap. Any feedback welcome.

Update v5 version:

- added IP format check
- added if nmap program exist
- restart program when IP address is wrong
- redesign window
- restructure oython code

Still missing:
- ask after a complete scan for a new scan or leaving... (will be soon in v6)



