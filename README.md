# ncurses-IPventur.py
IPventur nmap frontend for Python3 and curses with nmap3 module

This is v8 of ncurses-IPventur.py

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


start program (best as root) with: "python ncurses-IPventur.py"

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

Update v7 version:

- resolved json format saving bug
- added actual screen size, to windows size error message
- minor design change

Update v8 version:

- added notes that some nmap scan options are not valid for Windows OS yet
- added some new menu points
- changed some minor style issues

Note: new features will be added son! stay tune.
