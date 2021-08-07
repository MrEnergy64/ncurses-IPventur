# IPventur-Python-Curses
IPventur nmap frontend for Python3 and curses with nmap3 module

This is v6 of ncurses-IPventur-10v6.py

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


start program (best as root) with: "python ncurses-IPventur-10v6.py"

Note:
goal of the program was to write an easy to use frontend for nmap. Any feedback welcome.

Update v5 version:

- added IP format check
- added if nmap program exist
- restart program when IP address is wrong
- redesign windows design
- restructure python code

Still missing:
- ask after a complete scan for a new scan or leaving... (will be soon in v6)

Update v6 version:

- added terminal window size check of 34 x 111, otherwise program will not starts
- added restart menu after a completed scan
- some minor design changes

